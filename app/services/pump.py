from app.models.actuators import Pump
from app.repositories.GPIO.pumps import PumpActuator
from app.services.actuators import ActuatorService

class PumpService(ActuatorService[Pump]):
    def __init__(self):
        actuator_repository = PumpActuator()
        super().__init__(actuator_repository, Pump)