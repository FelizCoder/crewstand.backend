from fastapi import APIRouter

from app.repositories.missions.flow import FlowMissionRepository
from app.services.missions.flow import FlowMissionService

from .endpoints.actuators import router as actuators
from .endpoints.actuators import solenoid_service
from .endpoints.sensors import router as sensors
from .endpoints.sensors import flowmeter_service
from .endpoints.info import router as info
from .endpoints.missions import FlowMissionRouter

v1_router = APIRouter()

v1_router.include_router(actuators, prefix="/actuators")
v1_router.include_router(sensors, prefix="/sensors")
v1_router.include_router(info, prefix="/info", tags=["Backend Info"])
v1_router.include_router(
    FlowMissionRouter(
        service=FlowMissionService(
            mission_repo=FlowMissionRepository(
                actuator_service=solenoid_service,
                sensor_service=flowmeter_service,
                flow_sensor_id=0,
            )
        )
    ),
    prefix="/missions/flow",
    tags=["Flow Missions"],
)
