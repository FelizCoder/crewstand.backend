from typing import Generic, List, TypeVar

from fastapi import WebSocket
from app.models.sensors import Sensor, SensorReading, SensorRepository
from app.utils.websocket_manager import WebSocketManager
from app.utils.influx_client import influx_connector

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
        self.websocket_managers = [WebSocketManager() for _ in range(self.sensor.count)]
        self.influx = influx_connector

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
        sensor = self.sensor.post_reading(sensor_id, reading)
        self.influx.write_sensor(sensor)
        self.broadcast_reading(sensor_id, reading)
        return sensor

    async def connect_websocket(self, sensor_id: int, websocket: WebSocket):
        """
        Establish a WebSocket connection for a sensor.

        Parameters
        ----------
        sensor_id : int
            The ID of the sensor.
        websocket : WebSocket
            The WebSocket object to connect.

        Notes
        -----
        This method connects the WebSocket and sends the current reading of the sensor
        as a personal message to the WebSocket.

        See Also
        --------
        disconnect_websocket : Disconnect the WebSocket connection.
        broadcast_reading : Broadcast a reading to all connected WebSockets.
        """
        await self.websocket_managers[sensor_id].connect(websocket)

        current_reading = self.get_by_id(sensor_id).current_reading
        if current_reading:
            self.websocket_managers[sensor_id].send_personal_message(
                current_reading.model_dump_json(), websocket
            )

    def disconnect_websocket(self, sensor_id: int, websocket: WebSocket):
        """
        Disconnect a WebSocket connection for a sensor.

        Parameters
        ----------
        sensor_id : int
            The ID of the sensor.
        websocket : WebSocket
            The WebSocket object to disconnect.

        See Also
        --------
        connect_websocket : Establish a WebSocket connection.
        broadcast_reading : Broadcast a reading to all connected WebSockets.
        """
        self.websocket_managers[sensor_id].disconnect(websocket)

    def broadcast_reading(self, sensor_id: int, reading: SensorReading):
        """
        Broadcast a reading to all connected WebSockets for a sensor.

        Parameters
        ----------
        sensor_id : int
            The ID of the sensor.
        reading : SensorReading
            The reading to broadcast.

        See Also
        --------
        connect_websocket : Establish a WebSocket connection.
        disconnect_websocket : Disconnect the WebSocket connection.
        """
        self.websocket_managers[sensor_id].broadcast(reading.model_dump_json())
