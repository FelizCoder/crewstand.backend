# app/api/v1/endpoints/actuators.py
from typing import Annotated, List, Union
from fastapi import APIRouter, Path, WebSocket, WebSocketDisconnect

from app.models.actuators import SolenoidValve, ProportionalValve, Pump
from app.services.actuators.proportional import ProportionalService
from app.services.actuators.pump import PumpService
from app.services.actuators.service import ActuatorService
from app.services.actuators.solenoid import SolenoidService
from app.utils.logger import logger
from app.utils.config import settings

router = APIRouter()

solenoid_service = SolenoidService()
proportional_service = ProportionalService()
pump_service = PumpService()


@router.get("/", tags=["Actuators"])
def get_all_actuators() -> List[Union[SolenoidValve, ProportionalValve, Pump]]:
    """
    Retrieve a list of all actuators, including solenoid valves, proportional valves, and pumps.

    Returns:
        List[Union[SolenoidValve, ProportionalValve, Pump]]: A list containing all the actuators.
    """
    actuators = (
        solenoid_service.get_all()
        + proportional_service.get_all()
        + pump_service.get_all()
    )
    return actuators


def create_actuator_router(service: ActuatorService):
    """
    Creates a router for the specified actuator service.

    Args:
        service (ActuatorService): The service that handles the specific type of actuator.

    Returns:
        APIRouter: A FastAPI router configured for the actuator service.
    """
    r = APIRouter()

    @r.get("/", response_model=List[service.item_type])
    def get_all():
        """
        Retrieve all actuators of a specific type.

        Returns:
            List[service.item_type]: A list of actuators of the specified type.
        """
        return service.get_all()

    @r.get("/{actuator_id}", response_model=service.item_type)
    def get_by_id(
        actuator_id: Annotated[int, Path(..., ge=0, lt=service.actuator_repo.count)]
    ):
        """
        Retrieve a specific actuator by its ID.

        Args:
            actuator_id (int): The ID of the actuator to retrieve.

        Returns:
            service.item_type: The actuator object with the specified ID.
        """
        return service.get_by_id(actuator_id)

    @r.post("/set", response_model=service.item_type)
    async def set_state(actuator: service.item_type):
        """
        Set the state of a specific actuator.

        Args:
            actuator (service.item_type): The actuator object with the state to be set.

        Returns:
            service.item_type: The actuator object after its state has been updated.
        """
        return await service.set_state(actuator)

    @r.websocket("/{actuator_id}/state")
    async def state_ws(
        websocket: WebSocket,
        actuator_id: Annotated[int, Path(..., ge=0, lt=service.actuator_repo.count)],
    ):
        """
        Establish a WebSocket connection for an actuator state updates.

        Parameters
        ----------
        websocket : WebSocket
            The WebSocket object to establish a connection with.
        actuator_id : int
            The ID of the actuator to receive state updates for. Must be within the range
            [0, service.actuator_repo.count).

        Returns
        -------
        None

        Notes
        -----
        This function establishes a WebSocket connection with the provided `websocket` object
        and starts listening for state updates for the specified `actuator_id`. The connection
        remains open until a WebSocket disconnect occurs.

        Raises
        ------
        WebSocketDisconnect
            If the WebSocket connection is disconnected.

        See Also
        --------
        proportional_service.connect_websocket : Connects a WebSocket to an actuator.
        proportional_service.disconnect_websocket : Disconnects a WebSocket from an actuator.
        """
        await proportional_service.connect_websocket(actuator_id, websocket)
        try:
            while True:
                websocket.receive_text()
        except WebSocketDisconnect:
            proportional_service.disconnect_websocket(actuator_id, websocket)

    return r


proportional_router = create_actuator_router(proportional_service)


@proportional_router.websocket("/{proportional_id}/current_position")
async def current_position_ws(
    websocket: WebSocket,
    proportional_id: Annotated[
        int, Path(..., ge=0, lt=proportional_service.actuator_repo.count)
    ],
):
    """
    Establish a WebSocket connection for current position updates of a proportional actuator.

    Parameters
    ----------
    websocket : WebSocket
        The WebSocket object to establish a connection with.
    proportional_id : int
        The ID of the proportional actuator to receive current position updates for. Must be within the range
        [0, proportional_service.actuator_repo.count).

    Returns
    -------
    None

    Notes
    -----
    This function establishes a WebSocket connection with the provided `websocket` object and starts listening for
    current position updates for the specified `proportional_id`. The connection remains open until a WebSocket
    disconnect occurs.

    Raises
    ------
    WebSocketDisconnect
        If the WebSocket connection is disconnected.

    See Also
    --------
    proportional_service.connect_current_position_websocket : Connects a WebSocket to a proportional actuator for current position updates.
    proportional_service.disconnect_current_position_websocket : Disconnects a WebSocket from a proportional actuator for current position updates.
    """
    await proportional_service.connect_current_position_websocket(
        proportional_id, websocket
    )

    try:
        # Stay connected to the websocket
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        # Handle the websocket disconnection
        proportional_service.disconnect_current_position_websocket(
            proportional_id, websocket
        )


# Import routers using the create_router function
router.include_router(
    create_actuator_router(solenoid_service),
    prefix="/solenoid",
    tags=["Solenoid Valves"],
)
router.include_router(
    proportional_router,
    prefix="/proportional",
    tags=["Proportional Valves"],
)
router.include_router(
    create_actuator_router(pump_service), prefix="/pump", tags=["Pumps"]
)


def shutdown_event():
    """
    Shuts down the proportional service and closes the GPIO device when the application is shutting down.
    """

    logger.debug("Shutting down proportional service")
    proportional_service.disconnect()

    # Close the GPIO device when the application shuts down
    settings.DEVICE.close()
    logger.info("GPIO device closed")


router.on_shutdown = [shutdown_event]
