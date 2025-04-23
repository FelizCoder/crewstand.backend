from abc import ABC, abstractmethod
from datetime import datetime, time
from enum import Enum
from typing import List, NamedTuple, Optional
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


class FlowClassifierFeatures(BaseModel):
    """
    A Pydantic BaseModel class representing features used to classify flow control missions.

    Parameters
    ----------
    Volume : float
        Total volume of water consumed in liters during the mission.
    Mean : float
        Mean flow rate in liters per minute during the mission.
    Peak : float
        Peak flow rate in liters per minute observed during the mission.
    Duration : float
        Duration of the flow in seconds.
    Hour : float
        The hour of the day [0, 24[ when the mission was initiated, representing the start time in terms of
        a 24-hour clock format, useful for temporal pattern analysis.

    Raises
    ------
    ValueError
        If the values of any parameter do not conform to their expected data types and constraints.

    Notes
    -----
    This class is intended to serve as a structured data container for feeding into a machine learning model
    that predicts flow control mission end use based on extracted features. The `Hour` feature additionally
    supports time-of-day factors which might affect some classifications like residential water usage patterns.

    The fields have been annotated with descriptions for improved documentation and validation.
    """

    Volume: float = Field(..., description="Total volume of water consumed in liters")
    Mean: float = Field(..., description="Mean flow rate in liters per minute")
    Peak: float = Field(..., description="Peak flow rate in liters per minute")
    Duration: float = Field(..., description="Duration of the flow in seconds")
    Hour: float = Field(..., description="Hour of the day [0,24[")


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

        duration_scaling_factor : Optional[int]
            The scaling factor of the event simulation. For example, a simulation with a factor of 2 and a duration of 45 s represents an original event of 90 s. This parameter helps to simulate events with different durations without changing the original trajectory.

        actual_end_use : Optional[EndUseType]
            The actual end use type for simulation purposes.

        actual_start_time : Optional[time]
            The time of day when the simulated event starts (HH:MM:SS).

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
    ...     ],
    ...     duration_scaling_factor=2,  # The demo mission has a scaling factor of 2.
    ...     actual_end_use=EndUseType.SHOWER,
    ...     actual_start_time=time(11, 11, 11)
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
    duration_scaling_factor: Optional[int] = Field(
        None,
        description="The scaling factor of the event simulation. e.g. A simulation with a factor = 2 and a duration of 45 s represents an original event of 90 s",
        ge=1,
        examples=[2, 1],
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

    flow_control_mission: FlowControlMission = Field(
        ...,
        description="The completed FlowControlMission",
    )
    start_ts: datetime = Field(
        ...,
        description="The timestamp the mission started",
    )
    end_ts: datetime = Field(
        ...,
        description="The timestamp the mission was completed",
    )


class ClassifiedFlowControlMission(CompletedFlowControlMission):
    """
    Represents a flow control mission which has been classified based on its features.

    Parameters
    ----------
    features : FlowClassifierFeatures
        An instance of `FlowClassifierFeatures` used for classifying the mission.
    predicted_end_use : EndUseType
        The predicted end use for this mission as determined by the classifier.

    Attributes
    ----------
    features : FlowClassifierFeatures
        Features of the mission used for classification.
    predicted_end_use : EndUseType
        The end use category that the mission's features suggest it matches.

    Methods
    -------
    None defined specifically for this subclass. It relies on the methods implemented in the superclass.

    Raises
    ------
    ValueError
        If the provided `predicted_end_use` is not a valid instance of `EndUseType`.
    TypeError
        If the provided `features` is not an instance of `FlowClassifierFeatures`.

    Notes
    -----
    This class extends `CompletedFlowControlMission` and is intended to handle missions that have been completed
    and classified according to their flow characteristics and other features. The classification algorithm
    typically utilizes Machine Learning models to predict the `end_use` based on the provided `features`.
    """

    features: FlowClassifierFeatures
    predicted_end_use: EndUseType


class MissionRepository(ABC):
    """
    Abstract base class for mission repository implementations.
    Defines the interface for managing mission queue operations.
    """

    @abstractmethod
    def add_to_queue(self, missions: List[FlowControlMission]) -> None:
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
    def get_last_mission(self) -> Optional[ClassifiedFlowControlMission]:
        """
        Retrieve the last completed mission.

        Returns:
            Optional[CompletedFlowControlMission]: The last completed mission if available, None otherwise
        """

    @abstractmethod
    async def post_last_mission(self, mission: ClassifiedFlowControlMission) -> None:
        """
        Posts or records the provided `ClassifiedFlowControlMission` as the latest mission.

        Parameters:
        -----------
        mission : ClassifiedFlowControlMission
            The `ClassifiedFlowControlMission` object that represents the mission to be recorded as the latest one.
            Ensure that this mission is indeed a completed mission that has been already classified.
        """

    @abstractmethod
    def get_queue_length(self) -> int:
        """
        Get the current length of the mission queue.

        Returns:
            int: The number of missions in the queue
        """

    @abstractmethod
    def get_active(self) -> bool:
        """
        Get the active state of the mission repository.
        """

    @abstractmethod
    def set_active(self, active: bool) -> bool:
        """
        Set the active state of the mission repository.
        As long as active the repository will execute missions in the queue.
        If inactive the repository will not execute missions.

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

    @abstractmethod
    async def connect_classified_mission_websocket(self, websocket):
        """
        Connect a WebSocket to receive notifications about classified missions.
        """

    @abstractmethod
    def disconnect_classified_mission_websocket(self, websocket):
        """
        Disconnect a WebSocket from receiving notifications about classified missions.
        """
