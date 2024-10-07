from typing import List
from app.models.actuators import ProportionalValve
from .actuators import ActuatorService

class ProportionalService(ActuatorService[ProportionalValve]):
    item_type = ProportionalValve
    
    def get_all(self) -> List[ProportionalValve]:
        return super().get_all()
    
    def get_by_id(self, actuator_id: int) -> ProportionalValve:
        return super().get_by_id(actuator_id)
    
    def set_state(self, actuator: ProportionalValve) -> ProportionalValve:
        return super().set_state(actuator)