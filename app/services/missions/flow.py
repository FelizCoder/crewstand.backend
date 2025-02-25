from typing import Optional
from app.models.missions import FlowControlMission, MissionRepository
from app.utils.influx_client import influx_connector


class FlowMissionService:
    def __init__(self, mission_repo: MissionRepository) -> None:
        self.mission_repo = mission_repo
        self.database = influx_connector

    def add_to_queue(self, mission: FlowControlMission) -> None:
        self.mission_repo.add_to_queue(mission)

    def get_current_mission(self) -> FlowControlMission:
        return self.mission_repo.get_current_mission()

    def get_next_mission(self) -> Optional[FlowControlMission]:
        return self.mission_repo.get_next_mission()

    def get_queue_length(self) -> int:
        return self.mission_repo.get_queue_length()
