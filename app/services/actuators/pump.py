from app.models.actuators import Pump
from app.repositories.actuators.GPIO.pumps import PumpActuator
from app.services.actuators.service import ActuatorService


class PumpService(ActuatorService[Pump]):
    """
    A service class for managing pumps.

    This class provides methods to interact with a repository for pumps.
    It extends the ActuatorService class and is generic over Pump.
    """

    def __init__(self):
        actuator_repository = PumpActuator()
        super().__init__(actuator_repository, Pump)
