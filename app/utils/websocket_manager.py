"""
WebSocket Manager Module.

This module defines the WebSocketManager class which handles WebSocket
connections, including connecting, disconnecting, and broadcasting messages
to all active WebSocket connections.
"""

from typing import List
from fastapi import WebSocket

from app.utils.logger import logger


class WebSocketManager:
    """
    Manager for handling WebSocket connections and broadcasting messages.

    This class allows for managing multiple WebSocket connections, including
    connecting, disconnecting, and broadcasting messages to all active connections.

    Attributes
    ----------
    active_connections : list of WebSocket
        A list storing the active WebSocket connections.

    Methods
    -------
    connect(websocket)
        Accepts a WebSocket connection and adds it to the active connections.
    disconnect(websocket)
        Removes a WebSocket connection from the active connections.
    broadcast(message)
        Sends a text message to all active WebSocket connections.
    """

    def __init__(self):
        """
        Initializes a new instance of WebSocketManager.

        This sets up an empty list of active WebSocket connections.
        """
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """
        Accepts a WebSocket connection and adds it to the active connections.

        Parameters
        ----------
        websocket : WebSocket
            The WebSocket connection to accept and manage.
        """
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.debug(f"WebSocket connection accepted: {websocket}")

    def disconnect(self, websocket: WebSocket):
        """
        Removes a WebSocket connection from the active connections.

        Parameters
        ----------
        websocket : WebSocket
            The WebSocket connection to be removed.
        """
        self.active_connections.remove(websocket)
        logger.debug(f"WebSocket connection removed: {websocket}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """
        Send a personal message to a specific WebSocket connection.

        Args:
            message (str): The message to be sent to the WebSocket connection.
            websocket (WebSocket): The WebSocket connection to send the message to.
        """
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        """
        Sends a text message to all active WebSocket connections.

        Parameters
        ----------
        message : str
            The message to be broadcasted to all active connections.
        """
        logger.debug(f"Broadcasting message: {message}")
        for connection in self.active_connections:
            await connection.send_text(message)
