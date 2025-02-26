import time
from typing import Generic, List, Literal, Optional, TypeVar
from enum import Enum
from pydantic import BaseModel, Field


class SensorEnum(str, Enum):
    """Enumeration for different types of sensors."""

    FLOWMETER = "flowmeter"


class SensorReading(BaseModel):
    """Base model for a sensor reading."""

    value: float
    timestamp_ns: int = Field(
        ...,
        description="Timestamp of the reading in nanoseconds since Epoch",
        examples=[time.time_ns()],
    )


class Setpoint(BaseModel):
    setpoint: Optional[float] = None


class Sensor(Setpoint):
    """Base model for an sensor."""

    type: SensorEnum
    unit: str = Field(..., examples=["l/min", "°C", "bar", "V"])
    id: int = Field(..., ge=0, examples=[0, 1, 2])
    current_reading: Optional[SensorReading] = None


class Flowmeter(Sensor):
    """Model for a flowmeter sensor."""

    type: Literal[SensorEnum.FLOWMETER] = SensorEnum.FLOWMETER
    unit: str = "l/min"


T = TypeVar("T", bound=Sensor)


class SensorRepository(Generic[T]):
    """Repository for managing sensor records."""

    item_type: T = T
    count: int

    def get_all(self) -> List[T]:
        """Retrieve all Sensors of type T."""
        raise NotImplementedError

    def get_by_id(self, sensor_id: int) -> T:
        """Retrieve an Sensor by its ID."""
        raise NotImplementedError

    def post_reading(self, sensor_id: int, reading: SensorReading) -> T:
        """Update the state of a Sensor with a new reading."""
        raise NotImplementedError

    def post_setpoint(self, sensor_id: int, setpoint: Optional[float]) -> T:
        """Update the setpoint of a parameter"""
        raise NotImplementedError
