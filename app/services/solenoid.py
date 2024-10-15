from app.models.actuators import SolenoidValve
from app.repositories.GPIO.solenoid_valves import SolenoidActuator
from app.services.actuators import ActuatorService

class SolenoidService(ActuatorService[SolenoidValve]):
    def __init__(self):
        actuator_repository = SolenoidActuator()
        super().__init__(actuator_repository, SolenoidValve)