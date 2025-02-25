from fastapi import APIRouter
from typing import Optional
from app.models.missions import FlowControlMission
from app.services.missions.flow import FlowMissionService

router = APIRouter(tags=["Missions"])


class FlowMissionRouter(APIRouter):
    """Router for flow control missions."""

    def __init__(self, service: FlowMissionService, **kwargs):
        super().__init__(**kwargs)
        self.service = service
        self._setup_routes()

    def _setup_routes(self):
        @self.post("/queue", response_model=FlowControlMission)
        async def add_to_queue(mission: FlowControlMission):
            """Add a new mission to the queue."""
            self.service.add_to_queue(mission)
            return mission

        @self.get("/current", response_model=Optional[FlowControlMission])
        async def get_current():
            """Get the currently executing mission."""
            return self.service.get_current_mission()

        @self.get("/next", response_model=Optional[FlowControlMission])
        async def get_next():
            """Get the next mission in the queue."""
            return self.service.get_next_mission()

        @self.get("/queue/length")
        async def get_queue_length() -> int:
            """Get the current length of the mission queue."""
            return self.service.get_queue_length()
