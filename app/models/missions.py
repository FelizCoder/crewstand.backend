from typing import NamedTuple
from pydantic import BaseModel, Field, field_validator


class TrajectoryPoint(NamedTuple):
    """
    Represents a single point in a flow trajectory.

    :param time: Time in seconds since the start of the mission.
    :param flow_rate: The desired flow rate until the specified time is reached.
    """

    time: float
    flow_rate: float


class FlowControlMission(BaseModel):
    valve_id: int = Field(
        ..., description="ID of the valve to steer", ge=-1, examples=[1, 2, 3]
    )
    flow_trajectory: list[TrajectoryPoint] = Field(
        ...,
        description="Definition of the Flow Trajectory. A list of TrajectoryPoint instances, where each point defines the flow rate until a specific time",
        examples=[[(10, 22.2), (20, 11.1)]],
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
