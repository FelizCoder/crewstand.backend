from app.models.actuators import ProportionalValve
from app.repositories.GPIO.proportional_valves import ProportionalActuator
from app.services.actuators import ActuatorService


class ProportionalService(ActuatorService[ProportionalValve]):
    """
    A service class for managing proportional valves.

    This class provides methods to interact with a repository for proportional valves.
    It extends the ActuatorService class and is generic over ProportionalValve.
    """

    def __init__(self):
        actuator_repository = ProportionalActuator()
        super().__init__(actuator_repository, ProportionalValve)
