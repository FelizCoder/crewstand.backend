from abc import ABC, abstractmethod
from datetime import time
from enum import Enum
from typing import NamedTuple, Optional
from fastapi import WebSocket
from pydantic import BaseModel, Field, field_validator


class TrajectoryPoint(NamedTuple):
    """
    Represents a single point in a flow trajectory.

    :param time: Time in seconds since the start of the mission.
    :param flow_rate: The desired flow rate until the specified time is reached.
    """

    time: float
    flow_rate: float


class EndUseType(str, Enum):
    """Enumeration of possible end use types for simulations"""

    SHOWER = "Shower"
    TOILET = "Toilet"
    FAUCET = "Faucet"
    CLOTHES_WASHER = "ClothesWasher"
    DISHWASHER = "Dishwasher"
    BATHTUB = "Bathtub"
    OTHER = "other"


class FlowControlMission(BaseModel):
    """
    A class representing a flow control mission for a specific valve.

    This class defines a mission that controls the flow rate of a specified valve over time
    by following a predefined trajectory of time and flow rate points.

    Parameters
    ----------
    valve_id : int
        The ID of the valve to control.
    flow_trajectory : list of TrajectoryPoint
        A list of TrajectoryPoint instances, each specifying a time and the desired flow rate
        until that time is reached.

    Raises
    ------
    ValueError
        If the flow trajectory is empty, contains negative time or flow rate values,
        or if the time values are not in strictly ascending order.

    Examples
    --------
    >>> from app.models.missions import FlowControlMission, TrajectoryPoint
    >>> mission = FlowControlMission(
    ...     valve_id=1,
    ...     flow_trajectory=[
    ...         TrajectoryPoint(time=10, flow_rate=22.2),
    ...         TrajectoryPoint(time=20, flow_rate=11.1)
    ...     ]
    ... )
    >>> print(mission.valve_id)
    1
    """

    valve_id: int = Field(
        ..., description="ID of the valve to steer", ge=-1, examples=[1, 2, 3]
    )
    flow_trajectory: list[TrajectoryPoint] = Field(
        ...,
        description="Definition of the Flow Trajectory. A list of TrajectoryPoint instances, where each point defines the flow rate until a specific time",
        examples=[[(10, 22.2), (20, 11.1)]],
    )
    # Optional simulation details
    actual_end_use: Optional[EndUseType] = Field(
        None, description="The actual end use type for simulation purposes"
    )
    actual_duration: Optional[float] = Field(
        None,
        description="The actual duration of the simulated event in seconds",
        ge=0,
        examples=[3600, 30],
    )
    actual_start_time: Optional[time] = Field(
        None,
        description="The time of day when the simulated event starts (HH:MM:SS)",
        examples=[time(11, 11, 11), time(16, 2, 42)],
    )

    @field_validator("flow_trajectory")
    @classmethod
    def _validate_trajectory(cls, trajectory):
        if not trajectory:
            raise ValueError("Flow trajectory must not be empty")

        # Validate each trajectory point
        for i, (time, flow_rate) in enumerate(trajectory):
            if time < 0:
                raise ValueError(f"Time must be non-negative at index {i}: {time}")
            if flow_rate < 0:
                raise ValueError(
                    f"Flow rate must be non-negative at index {i}: {flow_rate}"
                )

        # Ensure that time values are in ascending order
        previous_time = -1
        for time, _ in trajectory:
            if time <= previous_time:
                raise ValueError("Time values must be in strictly ascending order.")
            previous_time = time

        return trajectory


class CompletedFlowControlMission(BaseModel):
    """
    Represents a completed flow control mission.

    Attributes:
    -----------
    flow_control_mission : FlowControlMission
        The completed FlowControlMission.
    start_ns : int
        The timestamp the mission started with nanosecond precision.
    end_ns : int
        The timestamp the mission was completed with nanosecond precision.
    """

    flow_control_mission: FlowControlMission
    start_ts: datetime = Field(
        ...,
        description="The timestamp the mission started with nanosecond precision",
    )
    end_ns: int = Field(
        ...,
        description="The timestamp the mission was completed with nanosecond precision",
    )


class MissionRepository(ABC):
    """
    Abstract base class for mission repository implementations.
    Defines the interface for managing mission queue operations.
    """

    @abstractmethod
    def add_to_queue(self, mission: FlowControlMission) -> None:
        """
        Add a mission to the queue.

        Args:
            mission: The FlowControlMission to be added to the queue
        """

    @abstractmethod
    def get_current_mission(self) -> FlowControlMission:
        """
        Retrieve the current active mission.

        Returns:
            FlowControlMission: The current active mission
        """

    @abstractmethod
    def get_next_mission(self) -> Optional[FlowControlMission]:
        """
        Retrieve the next mission in the queue.

        Returns:
            Optional[FlowControlMission]: The next mission if available, None otherwise
        """

    @abstractmethod
    def get_queue_length(self) -> int:
        """
        Get the current length of the mission queue.

        Returns:
            int: The number of missions in the queue
        """

    @abstractmethod
    async def connect_completed_mission_websocket(self, websocket: WebSocket) -> None:
        """
        Connect a WebSocket to receive notifications about completed missions.
        """

    @abstractmethod
    def disconnect_completed_mission_websocket(self, websocket: WebSocket) -> None:
        """
        Disconnect a WebSocket from receiving notifications about completed missions.
        """
