from app.models.actuators import ProportionalValve
from app.services.actuators.service import ActuatorService
from app.utils.config import settings


match settings.PROPORTIONAL_MODE:
    case "GPIO":
        from app.repositories.actuators.GPIO.proportional_valves import (
            ProportionalActuator,
        )
    case "CAN":
        from app.repositories.actuators.CAN.proportional_valves import (
            ProportionalActuator,
        )


class ProportionalService(ActuatorService[ProportionalValve]):
    """
    A service class for managing proportional valves.

    This class provides methods to interact with a repository for proportional valves.
    It extends the ActuatorService class and is generic over ProportionalValve.
    """

    def __init__(self):
        actuator_repository = ProportionalActuator()
        super().__init__(actuator_repository, ProportionalValve)

    def disconnect(self) -> None:
        """Disconnect from the service.

        This method will terminate the connection to the service,
        freeing up resources and resetting the object to a state as if
        it had just been instantiated.

        """
