# app/services/sensors/flowmeter.py
from typing import List
from app.models.sensors import Flowmeter
from app.repositories.sensors.flowmeter import FlowmeterSensor
from app.services.sensors.service import SensorService


class FlowmeterService(SensorService[Flowmeter]):
    """
    A service class for managing flowmeter sensors.

    This class provides methods to interact with a repository for flowmeter sensors.
    It extends the SensorService class and is generic over Flowmeter.
    """

    def __init__(self):
        sensor_repository = FlowmeterSensor()
        super().__init__(sensor_repository)
