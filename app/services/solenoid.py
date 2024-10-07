from typing import List
from app.models.actuators import SolenoidValve
from .actuators import ActuatorService

class SolenoidService(ActuatorService[SolenoidValve]):
    item_type = SolenoidValve
    
    def get_all(self) -> List[SolenoidValve]:
        return super().get_all()
    
    def get_by_id(self, actuator_id: int) -> SolenoidValve:
        return super().get_by_id(actuator_id)
    
    def set_state(self, actuator: SolenoidValve) -> SolenoidValve:
        return super().set_state(actuator)