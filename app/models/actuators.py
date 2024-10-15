from typing import Generic, List, Type, TypeVar
from enum import Enum
from pydantic import BaseModel, Field

class ActuatorEnum(str, Enum):
    SOLENOID = "solenoid valve"
    PROPORTIONAL = "proportional valve"
    PUMP = "pump"

class Actuator(BaseModel):
    type: ActuatorEnum
    id: int = Field(..., ge=-1, examples=[0,1,2])
    
class SolenoidValve(Actuator):
    type: ActuatorEnum = ActuatorEnum.SOLENOID
    open: bool
    
class ProportionalValve(Actuator):
    type: ActuatorEnum = ActuatorEnum.PROPORTIONAL
    position: int = Field(..., ge=0, le=100)
    
class Pump(Actuator):
    type: ActuatorEnum = ActuatorEnum.PUMP
    running: bool
    
T = TypeVar('T', bound=Actuator)

class ActuatorRepository(Generic[T]):
    item_type: T
    count: int
    
    async def get_all(self) -> List[T]:
        raise NotImplementedError
    
    async def get_by_id(self, actuator_id: int) -> T:
        raise NotImplementedError
    
    async def set_state(self, actuator: T) -> T:
        return NotImplementedError