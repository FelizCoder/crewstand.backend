from app.utils.logger import logger
from typing import List
from gpiozero import LEDBoard

from app.models.actuators import ActuatorRepository, SolenoidValve
from app.utils.config import settings


class SolenoidActuator(ActuatorRepository):
    def __init__(self):
        pins = list[int](settings.SOLENOID_GPIO.split(","))
        self.solenoids = LEDBoard(*pins)
        self.count = len(pins)
    
    def get_all(self) -> List[SolenoidValve]:
        values: List[bool] = self.solenoids.value
        solenoid_valves: List[SolenoidValve] = [SolenoidValve(id=i, open=val) for i, val in enumerate(values)]
        logger.debug(f"Solenoid valves: {solenoid_valves}")
        
        return solenoid_valves
    
    def get_by_id(self, id: int) -> SolenoidValve:
        state: bool = self.solenoids[id].value
        solenoid_valve: SolenoidValve = SolenoidValve(id=id, open=state)
        
        return solenoid_valve
    
    def set_state(self, request: SolenoidValve):
        request_state: bool = request.open
        
        if request.id == -1:
            # Set state for all solenoids
            self.solenoids.value = (request_state,) * self.count
        else:
            self.solenoids[request.id].value = request_state
        
        logger.debug(f"Solenoid {request.id} set to {request_state}")
        return SolenoidValve(id=request.id, open=self.solenoids.value[request.id])