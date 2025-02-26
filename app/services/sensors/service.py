import json
from typing import Generic, List, Optional, TypeVar
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

    def __init__(self, sensor: SensorRepository[T]) -> None:
        self.sensor = sensor
        self.item_type = T
        self.reading_ws = WebSocketManager(self.sensor.count)
        self.setpoint_ws = WebSocketManager(self.sensor.count)
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

    async def post_reading(self, sensor_id: int, reading: SensorReading) -> T:
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
        await self.reading_ws.broadcast(sensor_id, reading.model_dump_json())

        return sensor

    async def connect_reading_ws(self, sensor_id: int, websocket: WebSocket):
        """
        Establish a WebSocket connection for a sensor and send its current reading.

        **Summary**
        ----------
        Initialize a WebSocket connection for a specified sensor, immediately
        transmitting its current reading to the client as a JSON message.

        **Parameters**
        ----------
        sensor_id : int
            Unique identifier of the sensor to connect.
        websocket : WebSocket
            WebSocket object to establish the connection with.

        **Notes**
        -----
        * This method assumes the sensor ID is valid and the WebSocket is usable.
        * The initial message sent to the client contains the sensor's current
        reading in JSON format (via `model_dump_json`).

        **See Also**
        --------
        * `disconnect_reading_ws` : Terminate the WebSocket connection.
        * `broadcast_reading` : Transmit a reading to all connected WebSockets.
        * `reading_ws.connect` : Underlying WebSocket connection establishment.
        """
        await self.reading_ws.connect(sensor_id, websocket)

        current_reading = self.get_by_id(sensor_id).current_reading
        if current_reading:
            await websocket.send_text(current_reading.model_dump_json())

    def disconnect_reading_ws(self, sensor_id: int, websocket: WebSocket):
        """
        Terminate a WebSocket connection for a sensor.

        **Summary**
        ----------
        Safely close an existing WebSocket connection associated with a sensor.

        **Parameters**
        ----------
        sensor_id : int
            Unique identifier of the sensor whose connection is to be terminated.
        websocket : WebSocket
            WebSocket object representing the connection to disconnect.

        **See Also**
        --------
        * `connect_reading_ws` : Establish a new WebSocket connection.
        * `broadcast_reading` : Broadcast a reading to all connected WebSockets.
        * `reading_ws.disconnect` : Underlying WebSocket disconnection method.
        """
        self.reading_ws.disconnect(sensor_id, websocket)

    async def post_setpoint(self, sensor_id: int, setpoint: Optional[float]) -> T:
        """
        Update the setpoint for a sensor and broadcast the change.

        Summary
        -------
        Set a new setpoint for a sensor with the given ID, persist the update,
        and notify connected clients via a WebSocket broadcast.

        Parameters
        ----------
        sensor_id : int
            Unique identifier of the sensor to update.
        setpoint : float
            New setpoint value for the specified sensor.

        Returns
        -------
        T
            The updated sensor object (type dependent on implementation).

        Notes
        -----
        This method assumes a valid sensor ID and does not include error handling
        for non-existent sensors. It is expected that such checks are performed
        before calling this method.

        See Also
        --------
        sensor.post_setpoint : Underlying method for setting the sensor's setpoint.
        influx.write_sensor : Persistence of sensor data.
        setpoint_ws.broadcast : Broadcasting setpoint updates to clients.
        """
        if setpoint is not None:
            setpoint = float(setpoint)

        sensor = self.sensor.post_setpoint(sensor_id, setpoint)

        self.influx.write_sensor(sensor)
        await self.setpoint_ws.broadcast(sensor_id, json.dumps(setpoint))

        return sensor

    async def connect_setpoint_ws(self, sensor_id: int, websocket: WebSocket):
        """
        Establish a WebSocket connection for a sensor's setpoint and send its value.

        **Summary**
        ----------
        Initialize a WebSocket connection for receiving setpoint updates for a
        specified sensor, immediately sending the current setpoint value as a JSON
        message to the client.

        **Parameters**
        ----------
        sensor_id : int
            Unique identifier of the sensor to connect for setpoint updates.
        websocket : WebSocket
            WebSocket object to establish the connection with.

        **Notes**
        -----
        * Assumes the provided sensor ID is valid and the WebSocket is functional.
        * The initial message contains the current setpoint in JSON format.

        **See Also**
        --------
        * `disconnect_setpoint_ws` : Disconnect the WebSocket connection.
        * `setpoint_ws.connect` : Underlying connection establishment method.
        """

        await self.setpoint_ws.connect(sensor_id, websocket)
        setpoint = self.get_by_id(sensor_id).setpoint
        await websocket.send_text(json.dumps(setpoint))

    def disconnect_setpoint_ws(self, sensor_id: int, websocket: WebSocket):
        """
        Disconnect a WebSocket connection for a sensor's setpoint.

        **Parameters**
        ----------
        sensor_id : int
            Sensor ID whose setpoint connection is to be terminated.
        websocket : WebSocket
            WebSocket object representing the connection.

        **See Also**
        --------
        * `connect_setpoint_ws` : Establish a new setpoint WebSocket connection.
        * `setpoint_ws.disconnect` : Underlying disconnection method.
        """
        self.setpoint_ws.disconnect(sensor_id, websocket)
