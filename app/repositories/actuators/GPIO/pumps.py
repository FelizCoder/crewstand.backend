from typing import List
from gpiozero import LEDBoard

from app.models.actuators import ActuatorRepository, Pump
from app.utils.logger import logger
from app.utils.config import settings


class PumpActuator(ActuatorRepository):
    def __init__(self):
        pins = list[int](settings.PUMP_GPIO.split(","))
        self.pumps = LEDBoard(*pins)
        self.count = len(pins)

    def get_all(self) -> List[Pump]:
        values: List[bool] = self.pumps.value
        pumps: List[Pump] = [Pump(id=i, state=val) for i, val in enumerate(values)]
        logger.debug(f"Pumps: {pumps}")

        return pumps

    def get_by_id(self, id: int) -> Pump:
        state: bool = self.pumps[id].value
        solenoid_valve: Pump = Pump(id=id, state=state)

        return solenoid_valve

    def set_state(self, request: Pump):
        request_state: bool = request.state

        if request.id == -1:
            # Set state for all solenoids
            self.pumps.value = (request_state,) * self.count
        else:
            self.pumps[request.id].value = request_state

        logger.debug(f"Pump {request.id} set to {request_state}")
        return Pump(id=request.id, state=self.pumps.value[request.id])
