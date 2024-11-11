from typing import Annotated, List, Union
from fastapi import APIRouter, Path, WebSocket, WebSocketDisconnect

from app.models.sensors import Flowmeter, SensorReading
from app.services.sensors.service import SensorService
from app.services.sensors.flowmeter import FlowmeterService
from app.utils.websocket_manager import WebSocketManager

router = APIRouter()

flowmeter_service = FlowmeterService()


@router.get("/", tags=["Sensors"], response_model=List[Union[Flowmeter]])
def get_all_sensors() -> List[Union[Flowmeter]]:
    """
    Retrieve a list of all sensors, including flowmeters.

    Returns:
        List[Union[Flowmeter]]: A list containing all the sensors.
    """
    sensors = (
        flowmeter_service.get_all()
        # Add other sensor services here, if you have more.
    )
    return sensors


class SensorRouter(APIRouter):
    """
    Class to create a router for the specified sensor service.
    """

    def __init__(self, service: SensorService, **kwargs):
        """
        Initialize the SensorRouter with the specified service.

        Args:
            service (SensorService): The service that handles the specific type of sensor.
            kwargs: Additional keyword arguments for APIRouter initialization.
        """
        super().__init__(**kwargs)
        self.service = service
        self.websocket_managers = [
            WebSocketManager() for _ in range(self.service.sensor.count)
        ]
        self._setup_routes()

    def _setup_routes(self):
        """
        Define the routes and handlers for the sensor service.
        """

        @self.get("/", response_model=List[self.service.item_type])
        async def get_all():
            """
            Retrieve all sensors of a specific type.

            Returns:
                List[self.service.item_type]: A list of sensors of the specified type.
            """
            return self.service.get_all()

        @self.get("/{sensor_id}", response_model=self.service.item_type)
        async def get_by_id(
            sensor_id: Annotated[int, Path(..., ge=0, lt=self.service.sensor.count)]
        ):
            """
            Retrieve a specific sensor by its ID.

            Args:
                sensor_id (int): The ID of the sensor to retrieve.

            Returns:
                self.service.item_type: The sensor object with the specified ID.
            """
            return self.service.get_by_id(sensor_id)

        @self.post("/{sensor_id}/reading", response_model=self.service.item_type)
        async def post_reading(
            sensor_id: Annotated[int, Path(..., ge=0, lt=self.service.sensor.count)],
            reading: SensorReading,
        ):
            """
            Post a new reading for a specific sensor.

            Args:
                sensor_id (int): The ID of the sensor.
                reading (SensorReading): The new reading to update.

            Returns:
                self.service.item_type: The updated sensor object.
            """
            await self.websocket_managers[sensor_id].broadcast(
                reading.model_dump_json()
            )
            return self.service.post_reading(sensor_id, reading)

        @self.websocket("/ws/{sensor_id}")
        async def websocket_endpoint(
            websocket: WebSocket,
            sensor_id: Annotated[int, Path(..., ge=0, lt=self.service.sensor.count)],
        ):
            await self.websocket_managers[sensor_id].connect(websocket)
            # Retrieve the current reading for the specified sensor
            current_reading: SensorReading = self.service.get_by_id(
                sensor_id
            ).current_reading
            # Send the current reading to the connected websocket client
            if current_reading:
                await self.websocket_managers[sensor_id].send_personal_message(
                    current_reading.model_dump_json(),
                    websocket,
                )
            try:
                # Stay connected to the websocket
                while True:
                    await websocket.receive_text()
            except WebSocketDisconnect:
                # Handle the websocket disconnection
                self.websocket_managers[sensor_id].disconnect(websocket)


# Import routers using the create_sensor_router function
router.include_router(
    SensorRouter(flowmeter_service),
    prefix="/flowmeters",
    tags=["Flowmeters"],
)
