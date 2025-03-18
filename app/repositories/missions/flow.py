from collections import deque
from datetime import datetime
from typing import Optional, Deque
import asyncio

from app.models.missions import (
    CompletedFlowControlMission,
    MissionRepository,
    FlowControlMission,
)
from app.models.actuators import SolenoidValve
from app.services.actuators.solenoid import SolenoidService
from app.services.sensors.flowmeter import FlowmeterService
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
        self.mission_queue: Deque[FlowControlMission] = deque()
        self.current_mission: Optional[FlowControlMission] = None
        self.mission_task: Optional[asyncio.Task] = None
        self.solenoid_service = actuator_service
        self.flowmeter_service = sensor_service
        self.flow_sensor_id = flow_sensor_id
        self.completed_mission_ws = WebSocketManager()

    def add_to_queue(self, mission: FlowControlMission) -> None:
        """Add a new mission to the queue."""
        self.mission_queue.append(mission)
        if not self.current_mission:
            asyncio.create_task(self._execute_next_mission())

    def get_current_mission(self) -> Optional[FlowControlMission]:
        """Get the currently executing mission."""
        return self.current_mission

    def get_next_mission(self) -> Optional[FlowControlMission]:
        """Get the next mission in the queue without removing it."""
        return self.mission_queue[0] if self.mission_queue else None

    def get_queue_length(self) -> int:
        """Get the current length of the mission queue."""
        return len(self.mission_queue)

    async def connect_completed_mission_websocket(self, websocket):
        await self.completed_mission_ws.connect(0, websocket)

    def disconnect_completed_mission_websocket(self, websocket):
        self.completed_mission_ws.disconnect(0, websocket)

    async def _execute_next_mission(self) -> None:
        """Execute the next mission in the queue."""
        if not self.mission_queue:
            return

        self.current_mission = self.mission_queue.popleft()
        try:
            await self._execute_mission(self.current_mission)
        except Exception as e:
            logger.error(f"Error executing mission: {e}")
        finally:
            self.current_mission = None
            if self.mission_queue:
                await self._execute_next_mission()

    async def _execute_mission(self, mission: FlowControlMission) -> None:
        """
        Execute a single flow control mission.

        Args:
            mission: The mission to execute
        """
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

        finally:
            end_ts = datetime.now()
            completed_mission = CompletedFlowControlMission(
                flow_control_mission=mission, start_ts=start_ts, end_ts=end_ts
            )
            await self.completed_mission_ws.broadcast(
                0, completed_mission.model_dump_json()
            )
            influx_connector.write_completed_flow_control_mission(completed_mission)
