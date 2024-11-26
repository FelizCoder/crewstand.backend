# pylint: disable=E1136

import os
import canopen
from canopen.pdo.base import PdoMap
from typing import List

from app.models.actuators import ActuatorRepository, ProportionalValve
from app.utils.logger import logger
from app.utils.config import settings


class ProportionalActuator(ActuatorRepository):
    """
    Represents a proportional actuator controlling a proportional valve in a CANopen network.

    This class manages the connection to a CANopen network, initializes the
    actuator's state, retrieves its current position, and allows for control
    of the valve's position via command messages.

    Parameters
    ----------
    None: The constructor does not take any parameters, but connects to
    a predefined CAN network and initializes the actuator.

    Attributes
    ----------
    count : int
        The current count of actuators. Defaults to 1.
    network : canopen.Network
        The CANopen network instance.
    node : canopen.Node
        The node representing the actuator in the network.
    position : float
        The current position of the valve, expressed in percentage.
    position_command : canopen.PDO
        The command object used to send position commands to the valve.

    Methods
    -------
    get_all() -> List[ProportionalValve]:
        Retrieves a list of all connected ProportionalValve instances.

    get_by_id(actuator_id: int = 1) -> ProportionalValve:
        Retrieves the ProportionalValve instance by its ID.

    set_state(request: ProportionalValve):
        Sets the state of the valve based on the provided ProportionalValve request.

    disconnect():
        Disconnects the actuator from the CANopen network and sets the node to PRE-OPERATIONAL state.

    Examples
    --------
    >>> actuator = ProportionalActuator()
    >>> actuator.set_state(ProportionalValve(id=1, position=50.0))
    >>> current_position = actuator.get_by_id()
    >>> print(current_position.position)
    50.0

    Notes
    -----
    - Before using this class, ensure that the proper EDS file is available in the specified directory.
    - This class currently supports initializing only one Bürkert MotorValve 3280.

    Warnings
    --------
    - Ensure that the network settings (interface, channel, and bitrate) are correctly configured
        to avoid any connectivity issues.

    See Also
    --------
    ActuatorRepository : The base class providing shared functionalities among actuator classes.
    ProportionalValve : A class representing the configuration and state of the valve.
    """

    def __init__(self):
        self.count = 1  # Only the default setting for one Bürkert MotorValve 3280 is supported at the moment
        self.item_type = ProportionalValve

        current_file_directory = os.path.dirname(os.path.abspath(__file__))
        eds_file = os.path.join(
            current_file_directory,
            "eds",
            "Buerkert-MotorValve3280_CANopen_1.16-20240112.eds",
        )

        #  Connect to the CANopen Network
        self.network = canopen.Network()
        self.network.connect(
            interface="socketcan",
            channel=settings.PROPORTIONAL_CAN_INTERFACE,
            bitrate=500000,
        )

        # Add the node to the network
        self.node = self.network.add_node(5, eds_file)
        logger.debug(f"Initialized Node: {self.node.id}")
        logger.debug(
            f"Node {self.node.id} description: {self.node.sdo['Buerkert Device Description Object']['Device Name'].raw}"
        )

        # get the initial position of the Valve
        self.position: float = self.node.sdo["POS_Display.POS_Display"].phys

        # Read the PDO object dictionaries
        self.node.rpdo.read(from_od=True)
        self.node.tpdo.read(from_od=True)

        # Add callback for position TDPO
        self.node.tpdo[2].add_callback(self._on_position_received)

        # Initialize the position command for RPDO transmission
        self.position_command = self.node.rpdo[1]["CMDdigital.CMDdigital"]
        self.position_command.phys = self.position

        # Activate the node
        self.node.nmt.state = "OPERATIONAL"
        logger.debug(f"Node {self.node.id} set OPERATIONAL")
        self.node.rpdo[1].start(0.1)

    def get_all(self) -> List[ProportionalValve]:
        return [self.get_by_id()]

    def get_by_id(self, actuator_id: int = 0) -> ProportionalValve:
        rounded_position = round(self.position)
        clipped_position = max(0, min(100, rounded_position))

        return ProportionalValve(id=actuator_id, position=clipped_position)

    def set_state(self, actuator: ProportionalValve):
        # Assuming you set command using TPDO and RPDO data
        self.position_command.phys = actuator.position
        logger.debug(f"Proportional {actuator.id} set to {actuator.position}")

        return actuator

    def _on_position_received(self, msg: PdoMap):
        new_position = msg["POS_Display.POS_Display"].phys
        self.position = new_position
        logger.debug(f"Valve position received: {self.position}")

    def disconnect(self):
        """
        Disconnects the actuator from the CANopen network and
        sets the node to PRE-OPERATIONAL state.

        This method sets the actuator's node state to PRE-OPERATIONAL
        and disconnects it from the CANopen network, ensuring that
        all communication is halted and resources are released.

        Notes
        -----
        Once disconnected, the node cannot send or receive messages
        until it is re-initialized and reconnected to the network.
        """

        self.node.nmt.state = "PRE-OPERATIONAL"  # Deactivate the node
        logger.info(f"Node {self.node.id} set PRE-OPERATIONAL")
        self.network.disconnect()
        logger.info("Disconnected from CANopen Network")
