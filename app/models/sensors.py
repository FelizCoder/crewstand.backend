from typing import Generic, List, TypeVar, Union
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
        examples=[1730906908814683100],
    )


class Sensor(BaseModel):
    """Base model for an sensor."""

    type: SensorEnum
    id: int = Field(..., ge=0, examples=[0, 1, 2])
    current_reading: Union[SensorReading, None] = None
    unit: str = Field(..., examples=["l/min", "°C", "bar", "V"])


class Flowmeter(Sensor):
    """Model for a flowmeter sensor."""

    type: SensorEnum = SensorEnum.FLOWMETER
    unit: str = "l/min"


T = TypeVar("T", bound=Sensor)


class SensorRepository(Generic[T]):
    """Repository for managing sensor records."""

    item_type: T
    count: int

    def get_all(self) -> List[T]:
        """Retrieve all Sensors of type T."""
        raise NotImplementedError

    def get_by_id(self, sensor_id: int) -> T:
        """Retrieve an Sensor by its ID."""
        raise NotImplementedError

    def post_reading(self, sensor_id, reading: SensorReading) -> T:
        """Update the state of an actuator."""
        return NotImplementedError
