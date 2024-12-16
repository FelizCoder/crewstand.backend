from typing import List
from gpiozero import LEDBoard

from app.models.actuators import ActuatorRepository, ProportionalValve
from app.utils.logger import logger
from app.utils.config import settings


class ProportionalActuator(ActuatorRepository):
    """
    Represents a proportional actuator which controls proportional valves
    using GPIO pins specified in the settings.
    """

    def __init__(self):
        pins = list[int](settings.PROPORTIONAL_GPIO.split(","))
        self.proportionals = LEDBoard(*pins, pwm=True)
        self.count = len(pins)
        self.factor: float = 100

    def get_all(self) -> List[ProportionalValve]:
        values: List[float] = self.proportionals.value
        proportional_valves: List[ProportionalValve] = [
            ProportionalValve(id=i, state=round(val * self.factor))
            for i, val in enumerate(values)
        ]
        logger.debug("Proportional valves: %s", proportional_valves)
        return proportional_valves

    def get_by_id(self, actuator_id: int) -> ProportionalValve:
        state: int = round(self.proportionals[actuator_id].value * self.factor)
        proportional_valve: ProportionalValve = ProportionalValve(
            id=actuator_id, state=state
        )

        return proportional_valve

    def set_state(self, actuator: ProportionalValve):
        request_state: float = float(actuator.state) / self.factor

        if actuator.id == -1:
            # Set state for all proportionals
            self.proportionals.value = (request_state,) * self.count
        else:
            self.proportionals[actuator.id].value = request_state

        logger.debug("Proportional %s set to %s", actuator.id, request_state)
        new_state: int = round(self.proportionals[actuator.id].value * self.factor)
        return ProportionalValve(id=actuator.id, state=new_state)
