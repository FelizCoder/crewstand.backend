from typing import Type
from enum import Enum
from pydantic import BaseModel

class ActuatorEnum(str, Enum):
    SOLENOID = "solenoid valve"
    PROPORTIONAL = "proportional valve"
    PUMP = "pump"

class Actuator(BaseModel):
    type: ActuatorEnum
    id: int
    
class SolenoidValve(Actuator):
    type: ActuatorEnum = ActuatorEnum.SOLENOID
    open: bool
    
class ProportionalValve(Actuator):
    type: ActuatorEnum = ActuatorEnum.PROPORTIONAL
    position: int
    
class Pump(Actuator):
    type: ActuatorEnum = ActuatorEnum.PUMP
    running: bool