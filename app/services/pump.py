from typing import List
from app.models.actuators import Pump
from .actuators import ActuatorService

class PumpService(ActuatorService[Pump]):
    item_type = Pump
    
    def get_all(self) -> List[Pump]:
        return super().get_all()
    
    def get_by_id(self, actuator_id: int) -> Pump:
        return super().get_by_id(actuator_id)
    
    def set_state(self, actuator: Pump) -> Pump:
        return super().set_state(actuator)