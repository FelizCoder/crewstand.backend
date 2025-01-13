from typing import List
from app.models.sensors import Flowmeter, SensorReading, SensorRepository
from app.utils.logger import logger
from app.utils.config import settings


class FlowmeterSensor(SensorRepository[Flowmeter]):
    """
    FlowmeterSensor is a repository for managing flowmeter sensor data.

    This class provides methods to retrieve and update flowmeter sensor data. It initializes with a list containing one flowmeter sensor.

    Attributes
    ----------
    count : int
        The number of flowmeters. Initialized with a default value of 1.
    item_type : Type
        Type of sensor. Initialized to Flowmeter.
    flowmeters : List[Flowmeter]
        List containing flowmeter sensors, initialized with one `Flowmeter` object with `id=0`.

    Methods
    -------
    get_all()
        Retrieve all flowmeter sensors.

    get_by_id(sensor_id: int)
        Retrieve a specific flowmeter sensor by its ID.

    patch_reading(sensor_id: int, reading: SensorReading)
        Update the current reading of a specified flowmeter sensor by its ID.
    """

    def __init__(self):
        self.flowmeters = [Flowmeter(id=i) for i in range(settings.FLOWMETER_COUNT)]
        self.count = len(self.flowmeters)

    def get_all(self) -> List[Flowmeter]:
        flowmeters = self.flowmeters
        logger.debug("Flowmeters: %s", flowmeters)

        return flowmeters

    def get_by_id(self, sensor_id: int) -> Flowmeter:
        flowmeter = self.flowmeters[sensor_id]
        logger.debug("Flowmeter %d: %s", sensor_id, flowmeter)

        return flowmeter

    def post_reading(self, sensor_id: int, reading: SensorReading) -> Flowmeter:
        self.flowmeters[sensor_id].current_reading = reading
        logger.debug("Flowmeter %d reading patched: %s", sensor_id, reading)

        return self.flowmeters[sensor_id]

    def post_setpoint(self, sensor_id, setpoint):
        self.flowmeters[sensor_id].setpoint = setpoint
        logger.debug("Flowmeter %d setpoint patched: %s", sensor_id, setpoint)
        return self.flowmeters[sensor_id]
