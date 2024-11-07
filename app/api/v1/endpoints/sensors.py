from typing import Annotated, List, Union
from fastapi import APIRouter, Path

from app.models.sensors import Flowmeter, SensorReading
from app.services.sensors.service import SensorService
from app.services.sensors.flowmeter import FlowmeterService

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


def create_sensor_router(service: SensorService):
    """
    Creates a router for the specified sensor service.

    Args:
        service (SensorService): The service that handles the specific type of sensor.

    Returns:
        APIRouter: A FastAPI router configured for the sensor service.
    """
    r = APIRouter()

    @r.get("/", response_model=List[service.item_type])
    def get_all():
        """
        Retrieve all sensors of a specific type.

        Returns:
            List[service.item_type]: A list of sensors of the specified type.
        """
        return service.get_all()

    @r.get("/{sensor_id}", response_model=service.item_type)
    def get_by_id(sensor_id: Annotated[int, Path(..., ge=0, lt=service.sensor.count)]):
        """
        Retrieve a specific sensor by its ID.

        Args:
            sensor_id (int): The ID of the sensor to retrieve.

        Returns:
            service.item_type: The sensor object with the specified ID.
        """
        return service.get_by_id(sensor_id)

    @r.post("/{sensor_id}/reading", response_model=service.item_type)
    def post_reading(
        sensor_id: Annotated[int, Path(..., ge=0, lt=service.sensor.count)],
        reading: SensorReading,
    ):
        """
        Post a new reading for a specific sensor.

        Args:
            sensor_id (int): The ID of the sensor.
            reading (SensorReading): The new reading to update.

        Returns:
            service.item_type: The updated sensor object.
        """
        return service.post_reading(sensor_id, reading)

    return r


# Import routers using the create_sensor_router function
router.include_router(
    create_sensor_router(flowmeter_service),
    prefix="/flowmeters",
    tags=["Flowmeters"],
)
