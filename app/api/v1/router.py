from fastapi import APIRouter

from .endpoints.actuators import router as actuators

v1_router = APIRouter()

v1_router.include_router(actuators, prefix="/actuators")
