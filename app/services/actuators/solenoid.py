from app.models.actuators import SolenoidValve
from app.repositories.actuators.GPIO.solenoid_valves import SolenoidActuator
from app.services.actuators.service import ActuatorService


class SolenoidService(ActuatorService[SolenoidValve]):
    """
    A service class for managing solenoid valves.

    This class provides methods to interact with a repository for solenoid valves.
    It extends the ActuatorService class and is generic over SolenoidValve.
    """

    def __init__(self):
        actuator_repository = SolenoidActuator()
        super().__init__(actuator_repository, SolenoidValve)
