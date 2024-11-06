# app/services/sensors/service.py
from typing import Generic, List, TypeVar
from fastapi import HTTPException

from app.models.sensors import (
    Sensor,
    SensorReading,
    SensorRepository,
)
from app.models.errors import ValidationError

T = TypeVar("T", bound=Sensor)


class SensorService(Generic[T]):
    """
    A service class for managing sensors.

    This class provides methods to interact with sensor repositories.
    It is generic over a type T which must be a subclass of Sensor.

    Args:
        sensor (SensorRepository[T]): The repository for the sensor.
        item_type (T): The specific type of sensor.
    """

    def __init__(self, sensor: SensorRepository[T], item_type: T) -> None:
        self.sensor = sensor
        self.item_type = item_type

    def get_all(self) -> List[T]:
        """
        Retrieve all sensors.

        Returns:
            List[T]: A list of sensors.
        """
        return self.sensor.get_all()

    def get_by_id(self, sensor_id: int) -> T:
        """
        Retrieve a sensor by its ID.

        Args:
            sensor_id (int): The ID of the sensor.

        Returns:
            T: The sensor with the specified ID.
        """
        return self.sensor.get_by_id(sensor_id)

    def post_reading(self, sensor_id: int, reading: SensorReading) -> T:
        """
        Post a new reading for a sensor.

        Args:
            sensor_id (int): The ID of the sensor.
            reading (SensorReading): The new reading to update.

        Returns:
            T: The updated sensor.
        """
        return self.sensor.post_reading(sensor_id, reading)
