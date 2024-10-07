import logging
from typing import List, Union, TypeVar, Generic

from app.models.actuators import *

async def list_actuators() -> List[Union[SolenoidValve, ProportionalValve, Pump]]:
    logging.warning("This Service is not implemented yet")
    return [
        SolenoidValve(type=ActuatorEnum.SOLENOID ,id=0, open=False),
        ProportionalValve(type=ActuatorEnum.PROPORTIONAL ,id=0, position=0),
        Pump(type=ActuatorEnum.PUMP ,id=0, running=False),
    ]

T = TypeVar('T', bound=Actuator)

class ActuatorService(Generic[T]):
    item_type: T
    
    def get_all(self) -> List[T]:
        raise NotImplementedError
    
    def get_by_id(self, actuator_id: int) -> T:
        raise NotImplementedError
    
    def set_state(self, actuator: T) -> T:
        raise NotImplementedError