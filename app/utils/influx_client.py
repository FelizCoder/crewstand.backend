import time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

from app.models.actuators import Actuator
from app.models.sensors import Sensor
from app.utils.config import settings


class InfluxConnector:
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
            debug=settings.DEBUG_LEVEL,
        )

        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def write_sensor(self, sensor: Sensor):
        point = (
            Point(sensor.type.value)
            .field(field=sensor.id, value=sensor.current_reading.value)
            .time(
                time=sensor.current_reading.timestamp_ns,
                write_precision=WritePrecision.NS,
            )
        )

        self.write_api.write(bucket=self.bucket, record=point)

    def write_actuator(self, actuator: Actuator, state):
        point = (
            Point(actuator.type.value)
            .field(field=actuator.id, value=state)
            .time(time=time.time_ns(), write_precision=WritePrecision.NS)
        )

        self.write_api.write(bucket=self.bucket, record=point)


influx_connector = InfluxConnector()
