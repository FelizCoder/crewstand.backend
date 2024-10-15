# app/api/v1/endpoints/actuators.py
from typing import Annotated, List, Union
from fastapi import APIRouter, Path

from app.models.actuators import SolenoidValve, ProportionalValve, Pump
from app.services.actuators import ActuatorService, list_actuators
from app.services.solenoid import SolenoidService
from app.services.proportional import ProportionalService
from app.services.pump import PumpService

router = APIRouter()

solenoid_service = SolenoidService()
proportional_service = ProportionalService()
pump_service = PumpService()

@router.get("/", tags=["Actuators"])
async def get_all() -> List[Union[SolenoidValve, ProportionalValve, Pump]]:
    actuators = await list_actuators()
    return actuators

def create_actuator_router(service: ActuatorService):
    r = APIRouter()

    @r.get("/", response_model=List[service.item_type])  # Update this with your service's item type
    def get_all():
        return service.get_all()

    @r.get("/{actuator_id}", response_model=service.item_type)
    def get_by_id(actuator_id: Annotated[int, Path(..., ge=0, lt=service.actuator.count)]):
        return service.get_by_id(actuator_id)

    @r.post("/set", response_model=service.item_type)
    def set_state(actuator: service.item_type):
        return service.set_state(actuator)

    return r

# Import routers using the create_router function
router.include_router(create_actuator_router(solenoid_service), prefix="/solenoid", tags=["Solenoid Valves"])
router.include_router(create_actuator_router(proportional_service), prefix="/proportional", tags=["Proportional Valves"])
router.include_router(create_actuator_router(pump_service), prefix="/pump", tags=["Pumps"])
