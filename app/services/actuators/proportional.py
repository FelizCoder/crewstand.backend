from fastapi import WebSocket
from app.models.actuators import ProportionalValve
from app.services.actuators.service import ActuatorService
from app.utils.config import settings


match settings.PROPORTIONAL_MODE:
    case "GPIO":
        from app.repositories.actuators.GPIO.proportional_valves import (
            ProportionalActuator,
        )
    case "CAN":
        from app.repositories.actuators.CAN.proportional_valves import (
            ProportionalActuator,
        )


class ProportionalService(ActuatorService[ProportionalValve]):
    """
    A service class for managing proportional valves.

    This class provides methods to interact with a repository for proportional valves.
    It extends the ActuatorService class and is generic over ProportionalValve.
    """

    def __init__(self):
        actuator_repository = ProportionalActuator()
        super().__init__(actuator_repository, ProportionalValve)

    def disconnect(self) -> None:
        self.actuator_repo.disconnect()

    async def connect_current_position_websocket(
        self, ws_id: int, websocket: WebSocket
    ) -> None:
        """
        Connect a WebSocket to a proportional actuator for current position updates.

        Parameters
        ----------
        ws_id : int
            The ID of the proportional actuator to connect to.
        websocket : WebSocket
            The WebSocket object to connect.

        Returns
        -------
        None

        Notes
        -----
        This function connects the provided `websocket` object to the proportional actuator with the specified `ws_id`
        for current position updates.

        See Also
        --------
        disconnect_current_position_websocket : Disconnects a WebSocket from a proportional actuator for current position updates.
        """

        await self.actuator_repo.connect_current_position_websocket(ws_id, websocket)

    def disconnect_current_position_websocket(self, ws_id: int, websocket: WebSocket):
        """
        Disconnect a WebSocket from a proportional actuator for current position updates.

        Parameters
        ----------
        ws_id : int
            The ID of the proportional actuator to disconnect from.
        websocket : WebSocket
            The WebSocket object to disconnect.

        Returns
        -------
        None

        Notes
        -----
        This function disconnects the provided `websocket` object from the proportional actuator with the specified `ws_id`
        for current position updates.

        See Also
        --------
        connect_current_position_websocket : Connects a WebSocket to a proportional actuator for current position updates.
        """
        self.actuator_repo.disconnect_current_position_websocket(ws_id, websocket)
