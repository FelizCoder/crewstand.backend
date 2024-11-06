from fastapi import APIRouter

from .endpoints.actuators import router as actuators
from .endpoints.sensors import router as sensors

v1_router = APIRouter()

v1_router.include_router(actuators, prefix="/actuators")
v1_router.include_router(sensors, prefix="/sensors")
