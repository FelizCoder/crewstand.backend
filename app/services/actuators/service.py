import asyncio
import time
from typing import Generic, List, TypeVar
from fastapi import HTTPException, WebSocket

from app.models.actuators import (
    Actuator,
    ActuatorRepository,
)
from app.models.errors import ValidationError
from app.utils.websocket_manager import WebSocketManager
from app.utils.influx_client import influx_connector

T = TypeVar("T", bound=Actuator)


class ActuatorService(Generic[T]):
    """
    A service class for managing actuators.

    This class provides methods to interact with actuator repositories.
    It is generic over a type T which must be a subclass of Actuator.

    Args:
        actuator (ActuatorRepository[T]): The repository for the actuator.
        item_type (T): The specific type of actuator.
    """

    def __init__(self, actuator_repo: ActuatorRepository[T], item_type: T) -> None:
        self.actuator_repo = actuator_repo
        self.item_type = item_type

        self.websocket_manager = WebSocketManager(self.actuator_repo.count)
        self.influx = influx_connector

        # Send initial states to Database and Websockets
        asyncio.run(self._broadcast_all_actuators())

    def get_all(self) -> List[T]:
        """
        Retrieve all actuators.

        Returns:
            List[T]: A list of actuators.
        """
        return self.actuator_repo.get_all()

    def get_by_id(self, actuator_id: int) -> T:
        """
        Retrieve an actuator by its ID.

        Args:
            actuator_id (int): The ID of the actuator.

        Returns:
            T: The actuator with the specified ID.
        """
        return self.actuator_repo.get_by_id(actuator_id)

    async def set_state(self, actuator: T) -> T:
        """
        Update the state of a specified actuator.

        Summary
        -------
        Sets the state of an actuator, validates its ID, and triggers relevant
        updates to the repository, InfluxDB, and broadcasts to connected clients.

        Parameters
        ----------
        actuator : T
            The actuator object containing the new state to be applied.
            Must have a valid 'id' attribute.

        Returns
        -------
        T
            The actuator object with its state updated.

        Notes
        -----
        - Validates the actuator's ID before proceeding with the update.
        - If the actuator's ID is -1,
          all instances of the Actuator will be set to the corresponding state.
        - updates InfluxDB with the actuator's new state and broadcasts
        the new state to connected clients via WebSocket.
        - The current timestamp (in nanoseconds) is used for InfluxDB updates.

        See Also
        --------
        _validate_actuator_id : Validates an actuator's ID.
        actuator_repo.set_state : Updates the actuator's state in the repository.
        influx.write_actuator : Writes actuator data to InfluxDB.
        websocket_manager.broadcast : Broadcasts a message to connected clients.
        _broadcast_all_actuators : Broadcasts the state of all actuators.

        Raises
        ------
        ValueError
            If the actuator's ID is invalid (handled within _validate_actuator_id).
        """
        self._validate_actuator_id(actuator)
        timestamp_ns = time.time_ns()
        self.actuator_repo.set_state(actuator)

        if actuator.id == -1:
            await self._broadcast_all_actuators()
        else:
            self.influx.write_actuator(actuator, timestamp_ns)
            await self.websocket_manager.broadcast(actuator.id, actuator.state)

        return actuator

    async def connect_websocket(self, actuator_id: int, websocket: WebSocket):
        """
        Establish a WebSocket connection for an actuator.

        Summary
        -------
        Connects the WebSocket and sends the current state of the actuator as a personal message.

        Parameters
        ----------
        actuator_id : int
            The unique identifier of the actuator.
        websocket : WebSocket
            The WebSocket object to establish the connection with.

        Returns
        -------
        None

        Notes
        -----
        This method is responsible for initializing the WebSocket connection and
        immediately sending the current state of the actuator to the connected client.
        The state is retrieved using the `get_by_id` method.

        See Also
        --------
        disconnect_websocket : Disconnect the WebSocket connection.
        get_by_id : Retrieve an actuator by its unique identifier.
        """

        await self.websocket_manager.connect(actuator_id, websocket)

        current_state = self.get_by_id(actuator_id).state
        await websocket.send_text(str(current_state))

    def disconnect_websocket(self, actuator_id: int, websocket: WebSocket):
        """
        Disconnect a WebSocket connection for an actuator.

        Summary
        -------
        Terminates the WebSocket connection for the specified actuator.

        Parameters
        ----------
        actuator_id : int
            The unique identifier of the actuator.
        websocket : WebSocket
            The WebSocket object to disconnect.

        Returns
        -------
        None

        Notes
        -----
        This method is used to cleanly terminate an existing WebSocket connection,
        ensuring resources are properly released.

        See Also
        --------
        connect_websocket : Establish a WebSocket connection.
        """
        self.websocket_manager.disconnect(actuator_id, websocket)

    async def _broadcast_all_actuators(self):
        """
        Broadcast the current state of all actuators to connected clients.

        Summary
        -------
        This method simultaneously updates the InfluxDB with the current state of all
        actuators and broadcasts their states to all connected WebSocket clients.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Notes
        -----
        This method is designed to be executed asynchronously, leveraging
        `asyncio.gather` to run multiple broadcast tasks concurrently, ensuring
        efficient dissemination of actuator states to all connected clients.
        The current timestamp (in nanoseconds) is uniformly applied to all
        actuators for synchronization purposes.

        See Also
        --------
        get_all : Retrieve a list of all actuators.
        websocket_manager.broadcast : Broadcast a message to connected clients.
        influx.write_actuator : Write actuator data to InfluxDB.

        Warnings
        --------
        This method is intended for internal use within the service and should not
        be invoked directly from external interfaces.
        """
        tasks = []
        actuators = self.get_all()
        timestamp_ns = time.time_ns()

        for actuator in actuators:
            self.influx.write_actuator(actuator=actuator, timestamp_ns=timestamp_ns)
            broadcast_task = self.websocket_manager.broadcast(
                index=actuator.id, message=actuator.state
            )
            tasks.append(broadcast_task)

        await asyncio.gather(*tasks)

    def _validate_actuator_id(self, actuator: T):
        """
        Validate the actuator ID.

        Args:
            actuator (T): The actuator to validate.

        Raises:
            HTTPException: If the actuator ID is invalid.
        """
        if actuator.id >= self.actuator_repo.count:
            raise HTTPException(
                status_code=422,
                detail=[
                    ValidationError(
                        loc=["body", "id"],
                        msg=f"Input must be lower than {self.actuator_repo.count}",
                        type="lower_than",
                        input=actuator.id,
                    ).model_dump()
                ],
            )
