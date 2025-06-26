from collections import deque
from datetime import datetime
from typing import List, Optional, Deque
import asyncio

from app.models.missions import (
    ClassifiedFlowControlMission,
    CompletedFlowControlMission,
    MissionRepository,
    FlowControlMission,
)
from app.models.actuators import SolenoidValve
from app.services.actuators.solenoid import SolenoidService
from app.services.sensors.flowmeter import FlowmeterService
from app.utils.config import settings
from app.utils.logger import logger
from app.utils.websocket_manager import WebSocketManager
from app.utils.influx_client import influx_connector


class FlowMissionRepository(MissionRepository):
    """
    Implementation of MissionRepository for flow control missions.
    Manages a queue of missions and handles their execution.
    """

    def __init__(
        self,
        actuator_service: SolenoidService,
        sensor_service: FlowmeterService,
        flow_sensor_id: int,
    ) -> None:
        """
        Initialize the FlowMissionRepository.

        Args:
            actuator_service: Service to control valves
            sensor_service: Service to control flow sensors
            flow_sensor_id: ID of the flow sensor to control
        """
        self.active = True
        self.mission_queue: Deque[FlowControlMission] = deque()
        self.current_mission: Optional[FlowControlMission] = None
        self.mission_task: Optional[asyncio.Task] = None
        self.solenoid_service = actuator_service
        self.flowmeter_service = sensor_service
        self.flow_sensor_id = flow_sensor_id
        self.last_mission: Optional[ClassifiedFlowControlMission] = None
        self.completed_mission_ws = WebSocketManager()
        self.classified_mission_ws = WebSocketManager()

    def add_to_queue(self, missions: List[FlowControlMission]) -> None:
        for mission in missions:
            logger.debug("Adding mission to queue")
            self.mission_queue.append(mission)
        if self.mission_task is None:
            logger.debug("Starting to execute mission queue")
            self.mission_task = asyncio.create_task(self._execute_next_mission())

    def get_current_mission(self) -> Optional[FlowControlMission]:
        return self.current_mission

    def get_next_mission(self) -> Optional[FlowControlMission]:
        return self.mission_queue[0] if self.mission_queue else None

    def get_last_mission(self) -> Optional[ClassifiedFlowControlMission]:
        return self.last_mission

    async def post_last_mission(self, mission):
        self.last_mission = mission
        await self.classified_mission_ws.broadcast(0, mission.model_dump_json())

    def get_queue_length(self) -> int:
        return len(self.mission_queue)

    def get_active(self):
        return self.active

    def set_active(self, active):
        logger.debug(f"Setting Mission Repo active to {active}")
        self.active = active

        if not active and self.mission_task:
            self.mission_task.cancel()
        elif active and self.mission_task is None:  # Only if no task is running
            logger.debug("Starting new mission task")
            self.mission_task = asyncio.create_task(self._execute_next_mission())

        return self.active

    async def connect_completed_mission_websocket(self, websocket):
        await self.completed_mission_ws.connect(0, websocket)

    def disconnect_completed_mission_websocket(self, websocket):
        self.completed_mission_ws.disconnect(0, websocket)

    async def connect_classified_mission_websocket(self, websocket):
        await self.classified_mission_ws.connect(0, websocket)
        if self.last_mission:
            await websocket.send_text(
                self.last_mission.model_dump_json()
            )

    def disconnect_classified_mission_websocket(self, websocket):
        self.classified_mission_ws.disconnect(0, websocket)

    async def _execute_next_mission(self) -> None:
        if not self.active or not self.mission_queue:
            self.current_mission = None
            self.mission_task = None
            return
        try:
            while self.mission_queue and self.active:
                self.current_mission = self.mission_queue.popleft()
                await self._execute_mission(self.current_mission)
                await asyncio.sleep(settings.MISSION_WAIT_SECONDS)
        except asyncio.CancelledError:
            logger.info("Mission task cancelled")
            self.current_mission = None
        except Exception as e:
            logger.error("Error executing mission: %s", e)
            self.current_mission = None
        finally:
            self.mission_task = None
            self.current_mission = None

    async def _execute_mission(self, mission: FlowControlMission) -> None:
        """
        Execute a single flow control mission.

        Args:
            mission: The mission to execute
        """
        logger.debug("Executing mission: %s", mission.model_dump_json(indent=2))
        # Open the valve
        valve = SolenoidValve(id=mission.valve_id, state=True)
        await self.solenoid_service.set_state(valve)

        # Execute each trajectory point
        start_ts = datetime.now()
        try:
            previous_time = 0
            for point in mission.flow_trajectory:
                # Set new flow setpoint
                await self.flowmeter_service.post_setpoint(
                    self.flow_sensor_id, point.flow_rate
                )
                # Calculate wait time from previous point
                wait_time = point.time - previous_time
                if wait_time > 0:
                    await asyncio.sleep(wait_time)

                previous_time = point.time

            # Reset flow setpoint
            await self.flowmeter_service.post_setpoint(self.flow_sensor_id, None)

            # Close the valve
            valve.state = False
            await self.solenoid_service.set_state(valve)

        except asyncio.CancelledError:
            logger.info("Current mission cancelled")
            # Optionally, reset or clean up
            await self.flowmeter_service.post_setpoint(self.flow_sensor_id, None)
            valve.state = False
            await self.solenoid_service.set_state(valve)

        finally:
            end_ts = datetime.now()
            self.last_mission = CompletedFlowControlMission(
                flow_control_mission=mission, start_ts=start_ts, end_ts=end_ts
            )
            await self.completed_mission_ws.broadcast(
                0, self.last_mission.model_dump_json()
            )
            influx_connector.write_completed_flow_control_mission(self.last_mission)
            self.current_mission = None
