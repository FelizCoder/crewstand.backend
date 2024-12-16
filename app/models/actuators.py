from typing import Generic, List, Literal, TypeVar
from enum import Enum
from pydantic import BaseModel, Field


class ActuatorEnum(str, Enum):
    """Enumeration for different types of actuators."""

    SOLENOID = "solenoid valve"
    PROPORTIONAL = "proportional valve"
    PUMP = "pump"


class Actuator(BaseModel):
    """Base model for an actuator."""

    type: ActuatorEnum
    id: int = Field(..., ge=-1, examples=[0, 1, 2])


class SolenoidValve(Actuator):
    """Model representing a solenoid valve actuator."""

    type: Literal[ActuatorEnum.SOLENOID] = ActuatorEnum.SOLENOID
    state: bool


class ProportionalValve(Actuator):
    """Model representing a proportional valve actuator."""

    type: Literal[ActuatorEnum.PROPORTIONAL] = ActuatorEnum.PROPORTIONAL
    state: float = Field(..., ge=0, le=100)


class Pump(Actuator):
    """Model representing a pump actuator."""

    type: Literal[ActuatorEnum.PUMP] = ActuatorEnum.PUMP
    state: bool


T = TypeVar("T", bound=Actuator)


class ActuatorRepository(Generic[T]):
    """Repository for managing actuator records."""

    item_type: T
    count: int

    def get_all(self) -> List[T]:
        """Retrieve all actuators of type T."""
        raise NotImplementedError

    def get_by_id(self, actuator_id: int) -> T:
        """Retrieve an actuator by its ID."""
        raise NotImplementedError

    def set_state(self, actuator: T) -> T:
        """Update the state of an actuator."""
        return NotImplementedError
