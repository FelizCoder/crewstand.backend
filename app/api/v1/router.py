from fastapi import APIRouter

from .endpoints.actuators import router as actuators
from .endpoints.sensors import router as sensors
from .endpoints.info import router as info
from .endpoints.missions import router as missions

v1_router = APIRouter()

v1_router.include_router(actuators, prefix="/actuators")
v1_router.include_router(sensors, prefix="/sensors")
v1_router.include_router(info, prefix="/info", tags=["Backend Info"])
v1_router.include_router(missions, prefix="/missions")
