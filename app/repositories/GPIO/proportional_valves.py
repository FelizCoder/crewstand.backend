from typing import List
from gpiozero import LEDBoard

from app.models.actuators import ActuatorRepository, ProportionalValve
from app.utils.logger import logger
from app.utils.config import settings


class ProportionalActuator(ActuatorRepository):
    def __init__(self):
        pins = list[int](settings.PROPORTIONAL_GPIO.split(","))
        self.proportionals = LEDBoard(*pins, pwm=True)
        self.count = len(pins)
        self.factor: float = 100
    
    def get_all(self) -> List[ProportionalValve]:
        values: List[float] = self.proportionals.value
        proportional_valves: List[ProportionalValve] = [ProportionalValve(id=i, position=round(val*self.factor)) for i, val in enumerate(values)]
        logger.debug(f"Proportional valves: {proportional_valves}")
        
        return proportional_valves
    
    def get_by_id(self, id: int) -> ProportionalValve:
        state: int = round(self.proportionals[id].value * self.factor)
        proportional_valve: ProportionalValve = ProportionalValve(id=id, position=state)
        
        return proportional_valve
    
    def set_state(self, request: ProportionalValve):
        request_state: float = float(request.position) / self.factor
        
        if request.id == -1:
            # Set state for all proportionals
            self.proportionals.value = (request_state,) * self.count
        else:
            self.proportionals[request.id].value = request_state
        
        logger.debug(f"Proportional {request.id} set to {request_state}")
        new_state: int = round(self.proportionals[request.id].value *self.factor)
        return ProportionalValve(id=request.id, position=new_state)