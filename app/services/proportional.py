from app.models.actuators import ProportionalValve
from app.repositories.GPIO.proportional_valves import ProportionalActuator
from app.services.actuators import ActuatorService

class ProportionalService(ActuatorService[ProportionalValve]):
    def __init__(self):
        actuator_repository = ProportionalActuator()
        super().__init__(actuator_repository, ProportionalValve)