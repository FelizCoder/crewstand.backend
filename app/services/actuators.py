import logging
from typing import List, Union, TypeVar, Generic

from app.models.actuators import *
from app.utils.logger import not_implemented_warning

async def list_actuators() -> List[Union[SolenoidValve, ProportionalValve, Pump]]:
    not_implemented_warning()
    return [
        SolenoidValve(type=ActuatorEnum.SOLENOID ,id=0, open=False),
        SolenoidValve(type=ActuatorEnum.SOLENOID ,id=1, open=True),
        ProportionalValve(type=ActuatorEnum.PROPORTIONAL ,id=0, position=0),
        Pump(type=ActuatorEnum.PUMP ,id=0, running=False),
    ]

T = TypeVar('T', bound=Actuator)

class ActuatorService(Generic[T]):
    item_type: T
    
    async def get_all(self) -> List[T]:
        raise NotImplementedError
    
    async def get_by_id(self, actuator_id: int) -> T:
        raise NotImplementedError
    
    async def set_state(self, actuator: T) -> T:
        not_implemented_warning()
        return actuator