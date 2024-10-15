from typing import List, Union, TypeVar, Generic
from fastapi import HTTPException

from app.models.actuators import *
from app.models.errors import ValidationError
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
    def __init__(self, actuator: ActuatorRepository[T], item_type: T) -> None:
        self.item_type = item_type
        self.actuator = actuator
        
    def get_all(self) -> List[T]:
        return self.actuator.get_all()
    
    def get_by_id(self, actuator_id: int) -> T:
        return self.actuator.get_by_id(actuator_id)
    
    def set_state(self, actuator: T) -> T:
        self.validate_actuator_id(actuator)
        return self.actuator.set_state(actuator)
    
    def validate_actuator_id(self, actuator: T):
        if actuator.id >= self.actuator.count:
            raise HTTPException(status_code=422, detail=[
                ValidationError(
                    loc=["body","id"],
                    msg=f"Input must be lower than {self.actuator.count}",
                    type="lower_than",
                    input=actuator.id,
                ).model_dump()
            ])
        pass