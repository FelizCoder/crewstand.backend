import time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

from app.models.actuators import Actuator, ActuatorEnum
from app.models.missions import CompletedFlowControlMission
from app.models.sensors import Sensor
from app.utils.config import settings
from app.utils.logger import logger


class InfluxConnector:
    """
    Summary
    ----------
    Provides a synchronous interface for writing data to an InfluxDB instance.
    Handles sensor and actuator data writes with automatic point generation.

    Parameters
    ----------
    url : str, optional
        InfluxDB server URL ( defaults to `settings.INFLUXDB_URL.unicode_string()` )
    token : str, optional
        InfluxDB authentication token ( defaults to `settings.INFLUXDB_TOKEN` )
    org : str, optional
        InfluxDB organization ( defaults to `settings.INFLUXDB_ORG` )
    bucket : str, optional
        Target InfluxDB bucket for writes ( defaults to `settings.INFLUXDB_BUCKET` )

    Attributes
    ----------
    bucket : str
        Target InfluxDB bucket for writes.
    client : InfluxDBClient
        Underlying InfluxDB client instance.
    write_api : WriteApi
        Synchronous write API for the InfluxDB client.

    Methods
    ----------
    write_sensor(sensor)
        Writes a sensor reading to InfluxDB.
    write_actuator(actuator, timestamp_ns)
        Writes an actuator state to InfluxDB with a specified timestamp.
    _write(point)
        Internal method for writing a pre-constructed InfluxDB point.

    Raises
    ----------
    ConnectionError
        If a connection issue occurs while writing to InfluxDB, an error is logged.

    Notes
    -----
    This class is designed for synchronous use. For asynchronous operations, consider using the asynchronous InfluxDB client.
    Instance configuration is primarily driven by the application's settings module.
    """

    def __init__(
        self,
        url=settings.INFLUXDB_URL.unicode_string(),
        token=settings.INFLUXDB_TOKEN,
        org=settings.INFLUXDB_ORG,
        bucket=settings.INFLUXDB_BUCKET,
    ):

        self.bucket = bucket
        self.client = InfluxDBClient(
            url=url,
            token=token,
            org=org,
            debug=(settings.DEBUG_LEVEL == "DEBUG"),
            timeout=250,
        )

        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def write_sensor(self, sensor: Sensor):
        """
        Summary
        ----------
        Writes a sensor reading to InfluxDB, constructing the data point from the provided sensor object.

        **Parameters**
        ----------
        sensor : Sensor
            Sensor object containing the type, ID, current reading value, and timestamp.

        Notes
        -----
        *   This method assumes the `sensor` object has the following attributes:
            *   `type`: Sensor type (used as the InfluxDB measurement)
            *   `id`: Sensor ID (used as the field key)
            *   `current_reading`: Object containing `value` and `timestamp_ns` attributes
        *   The write operation is handled by the internal `_write` method, which logs any connection errors.

        See Also
        ----------
        _write : Internal method for writing InfluxDB points.
        """

        point = (
            Point(sensor.type.value)
            .field(field="reading", value=sensor.current_reading.value)
            .field(field="setpoint", value=sensor.setpoint)
            .tag(key="id", value=sensor.id)
            .time(
                time=sensor.current_reading.timestamp_ns,
                write_precision=WritePrecision.NS,
            )
        )
        self._write(point)

    def write_actuator(self, actuator: Actuator, timestamp_ns: int):
        """
        Summary
        ----------
        Writes an actuator state to InfluxDB, optionally specifying a custom timestamp.

        Parameters
        ----------
        actuator : Actuator
            Actuator object containing the type, ID, and current state.
        timestamp_ns : int, optional
            Custom timestamp in nanoseconds (defaults to the current time if omitted).

        Notes
        -----
        *   This method assumes the `actuator` object has the following attributes:
            *   `type`: Actuator type (used as the InfluxDB measurement)
            *   `id`: Actuator ID (used as the field key)
            *   `state`: Current actuator state value
        *   The write operation is handled by the internal `_write` method, which logs any connection errors.
        *   If no custom timestamp is provided, the current system time (in nanoseconds) is used.

        See Also
        ----------
        _write : Internal method for writing InfluxDB points.
        time.time_ns : Function for retrieving the current time in nanoseconds.
        """
        point = (
            Point(actuator.type.value)
            .field(field="state", value=actuator.state)
            .tag(key="id", value=actuator.id)
            .tag(key="type", value="set")
            .time(time=timestamp_ns, write_precision=WritePrecision.NS)
        )
        self._write(point)

    def write_current_proportional_position(
        self,
        proportional_id: int,
        current_position: float,
        timestamp_ns: int,
    ):
        """
        Writes the current proportional position of an actuator to the InfluxDB database.

        Parameters
        ----------
        proportional_id : int
            The ID of the proportional actuator.
        current_position : float
            The current position of the proportional actuator.
        timestamp_ns : int
            The timestamp of the measurement, in nanoseconds.

        Returns
        -------
        None

        Raises
        ------
        Exception
            If there is an error while writing to InfluxDB.
        """
        point = (
            Point(ActuatorEnum.PROPORTIONAL.value)
            .field(field="state", value=current_position)
            .tag(key="id", value=proportional_id)
            .tag(key="type", value="current")
            .time(time=timestamp_ns, write_precision=WritePrecision.NS)
        )
        self._write(point)

    def write_completed_flow_control_mission(
        self, mission: CompletedFlowControlMission
    ):
        """
        Writes a representation of a completed flow control mission to the InfluxDB database.

        Parameters
        ----------
        mission : CompletedFlowControlMission
            The completed flow control mission to be stored in the InfluxDB database.
            This object holds the details of the completed mission including the start and end
            timestamps with nanosecond precision.

        Returns
        -------
        None
            This method does not return anything; it writes data points to the database.

        Raises
        ------
        Exception
            If an error occurs during the process of writing to the InfluxDB database,
            an exception is caught and logged for debugging purposes.
            The method continues execution after handling the exception but no specific
            exceptions are propagated or re-raised.

        See Also
        --------
        CompletedFlowControlMission : The custom data structure representing a completed flow control mission.

        Notes
        -----
        This method constructs an InfluxDB Point from `mission` that encapsulates:
        - Mission-specific tags like 'actual end use', 'actual start time', 'actual duration',
        and 'valve id'.
        - An 'end timestamp [ns]' tag set to `mission.end_ns`.
        - The time set to `mission.start_ns` with nanosecond precision.

        The constructed point is then written to the InfluxDB database using the
        `_write` method, which is assumed to handle the writing process seamlessly.
        """
        point = (
            Point("Flow Control Mission")
            .field("end timestamp [s]", mission.end_ts.timestamp())
            .tag("actual end use", mission.flow_control_mission.actual_end_use)
            .tag("actual start time", mission.flow_control_mission.actual_start_time)
            .tag("actual duration", mission.flow_control_mission.actual_duration)
            .tag("valve id", mission.flow_control_mission.valve_id)
            .time(time=mission.start_ts, write_precision=WritePrecision.NS)
        )
        logger.debug(f"Writing mission to InfluxDB: {mission}")
        self._write(point)

    def _write(self, point):
        try:
            self.write_api.write(bucket=self.bucket, record=point)
        except Exception as e:
            logger.error(f"Failed to write to InfluxDB: {e}")


influx_connector = InfluxConnector()
