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
    def __init__(self, count: int = 1):
        """
        Initializes a new instance of WebSocketManager.

        Args:
            count (int, optional): The number of WebSocket managers to initialize. Defaults to 1.
        """
        self.active_connections: List[List[WebSocket]] = [[] for _ in range(count)]

    # ... (existing methods remain the same, with adjustments to handle the list of lists)

    async def connect(self, index: int, websocket: WebSocket):
        """
        Accepts a WebSocket connection and adds it to the active connections.

        Parameters
        ----------
        index : int
            The index of the WebSocket manager.
        websocket : WebSocket
            The WebSocket connection to accept and manage.
        """
        await websocket.accept()
        self.active_connections[index].append(websocket)
        logger.debug(f"WebSocket connection accepted: {websocket.client}")

    def disconnect(self, index: int, websocket: WebSocket):
        """
        Removes a WebSocket connection from the active connections.

        Parameters
        ----------
        index : int
            The index of the WebSocket manager.
        websocket : WebSocket
            The WebSocket connection to be removed.
        """
        self.active_connections[index].remove(websocket)
        logger.debug(f"WebSocket connection removed: {websocket.client}")

    async def broadcast(self, index: int, message: str):
        """
        Sends a text message to all active WebSocket connections.

        Parameters
        ----------
        index : int
            The index of the WebSocket manager.
        message : str
            The message to be broadcasted to all active connections.
        """
        for connection in self.active_connections[index]:
            await connection.send_text(message)
