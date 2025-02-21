from fastapi import APIRouter
from app.models.missions import FlowControlMission
from app.utils.logger import logger


router = APIRouter(tags=["Missions"])


@router.post("/queue", response_model=FlowControlMission)
def post_mission_to_queue(mission: FlowControlMission):
    # TODO: Implement mission service
    logger.warning("Mission service is not implemented yet.")
    return mission
