from typing import List, Optional
from app.models.missions import (
    ClassifiedFlowControlMission,
    CompletedFlowControlMission,
    FlowControlMission,
    MissionRepository,
)
from app.utils.influx_client import influx_connector


class FlowMissionService:
    def __init__(self, mission_repo: MissionRepository) -> None:
        self.mission_repo = mission_repo
        self.database = influx_connector

    def add_to_queue(self, mission: List[FlowControlMission]) -> None:
        self.mission_repo.add_to_queue(mission)

    def get_current_mission(self) -> FlowControlMission:
        return self.mission_repo.get_current_mission()

    def get_next_mission(self) -> Optional[FlowControlMission]:
        return self.mission_repo.get_next_mission()

    def get_last_mission(self) -> Optional[ClassifiedFlowControlMission]:
        return self.mission_repo.get_last_mission()

    async def post_last_mission(self, mission: CompletedFlowControlMission):
        return await self.mission_repo.post_last_mission(mission)

    def get_queue_length(self) -> int:
        return self.mission_repo.get_queue_length()

    def get_active(self) -> bool:
        return self.mission_repo.get_active()

    def set_active(self, active: bool) -> bool:
        return self.mission_repo.set_active(active)
