from typing import Generic, List, Literal, TypeVar
from enum import Enum
from fastapi import WebSocket
from pydantic import BaseModel, Field


class ActuatorEnum(str, Enum):
    """Enumeration for different types of actuators."""

    SOLENOID = "solenoid valve"
    PROPORTIONAL = "proportional valve"
    PUMP = "pump"


class Actuator(BaseModel):
    """Base model for an actuator."""

    type: ActuatorEnum
    id: int = Field(..., ge=-1, examples=[0, 1, 2])
    state: bool | float


class SolenoidValve(Actuator):
    """Model representing a solenoid valve actuator."""

    type: Literal[ActuatorEnum.SOLENOID] = ActuatorEnum.SOLENOID
    state: bool


class ProportionalValve(Actuator):
    """Model representing a proportional valve actuator."""

    type: Literal[ActuatorEnum.PROPORTIONAL] = ActuatorEnum.PROPORTIONAL
    state: float = Field(..., ge=0, le=100)
    current_position: float | None = Field(default=None, ge=0, le=100)


class Pump(Actuator):
    """Model representing a pump actuator."""

    type: Literal[ActuatorEnum.PUMP] = ActuatorEnum.PUMP
    state: bool


T = TypeVar("T", bound=Actuator)


class ActuatorRepository(Generic[T]):
    """Repository for managing actuator records."""

    item_type: T
    count: int

    def get_all(self) -> List[T]:
        """Retrieve all actuators of type T."""
        raise NotImplementedError

    def get_by_id(self, actuator_id: int) -> T:
        """Retrieve an actuator by its ID."""
        raise NotImplementedError

    def set_state(self, actuator: T) -> T:
        """Update the state of an actuator."""
        return NotImplementedError

    def disconnect(self):
        """
        Disconnect the actuator.

        This method is a placeholder and does not perform any actual disconnection.

        Returns
        -------
        None

        See Also
        --------
        actuator.repositories : Repositories that implement the actual disconnection logic.
        """

    async def connect_current_position_websocket(
        self, ws_id: int, websocket: WebSocket
    ):
        """
        Connect a WebSocket to an actuator for current position updates.

        Parameters
        ----------
        ws_id : int
            The ID of the actuator to connect to.
        websocket : WebSocket
            The WebSocket object to connect.

        Returns
        -------
        None

        Notes
        -----
        This function connects the provided `websocket` object to the actuator with the specified `ws_id` for current position updates.

        See Also
        --------
        disconnect_current_position_websocket : Disconnects a WebSocket from an actuator for current position updates.
        """

    def disconnect_current_position_websocket(self, ws_id: int, websocket: WebSocket):
        """
        Disconnect a WebSocket from an actuator for current position updates.

        Parameters
        ----------
        ws_id : int
            The ID of the actuator to disconnect from.
        websocket : WebSocket
            The WebSocket object to disconnect.

        Returns
        -------
        None

        Notes
        -----
        This function disconnects the provided `websocket` object from the actuator with the specified `ws_id` for current position updates.

        See Also
        --------
        connect_current_position_websocket : Connects a WebSocket to an actuator for current position updates.
        """
