from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Optional
from app.models.missions import (
    ClassifiedFlowControlMission,
    FlowControlMission,
)
from app.services.missions.flow import FlowMissionService

router = APIRouter(tags=["Missions"])


class FlowMissionRouter(APIRouter):
    """Router for flow control missions."""

    def __init__(self, service: FlowMissionService, **kwargs):
        super().__init__(**kwargs)
        self.service = service
        self._setup_routes()

    def _setup_routes(self):
        @self.post("/queue")
        async def add_to_queue(mission: List[FlowControlMission]):
            """Add a new mission to the queue."""
            self.service.add_to_queue(mission)
            return True

        @self.get("/current", response_model=Optional[FlowControlMission])
        async def get_current():
            """Get the currently executing mission."""
            return self.service.get_current_mission()

        @self.get("/next", response_model=Optional[FlowControlMission])
        async def get_next():
            """Get the next mission in the queue."""
            return self.service.get_next_mission()

        @self.get("/last", response_model=Optional[ClassifiedFlowControlMission])
        async def get_last():
            """Get the last completed mission."""
            return self.service.get_last_mission()

        @self.post("/last")
        async def post_last(mission: ClassifiedFlowControlMission):
            await self.service.post_last_mission(mission)
            return True

        @self.get("/queue/length")
        async def get_queue_length() -> int:
            """Get the current length of the mission queue."""
            return self.service.get_queue_length()

        @self.get("/active")
        async def get_active() -> bool:
            """Get Mission execution status."""
            return self.service.get_active()

        @self.post("/active")
        async def set_active(active: bool):
            """Set Mission execution to active."""
            self.service.set_active(active)

        @self.websocket("/completed")
        async def completed_missions_ws(websocket: WebSocket):
            await self.service.mission_repo.connect_completed_mission_websocket(
                websocket
            )

            try:
                while True:
                    await websocket.receive_text()
            except WebSocketDisconnect:
                await self.service.mission_repo.disconnect_completed_mission_websocket(
                    websocket
                )

        @self.websocket("/classified")
        async def classified_missions_ws(websocket: WebSocket):
            await self.service.mission_repo.connect_classified_mission_websocket(
                websocket
            )
            try:
                while True:
                    await websocket.receive_text()
            except WebSocketDisconnect:
                await self.service.mission_repo.disconnect_classified_mission_websocket(
                    websocket
                )
