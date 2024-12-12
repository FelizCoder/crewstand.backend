# app/tests/test_actuators_gpio.py
import pytest

from app.models.sensors import Flowmeter, SensorReading
from app.repositories.sensors.flowmeter import FlowmeterSensor


@pytest.fixture(name="repo")
def flowmeter_repo():
    sensor = FlowmeterSensor()
    return sensor


def test_flowmeter_sensor(repo):
    # Test get_all
    expected_flowmeters = [Flowmeter(id=0), Flowmeter(id=1)]
    repo.flowmeters = expected_flowmeters

    flowmeters = repo.get_all()
    assert len(flowmeters) == len(expected_flowmeters)
    assert flowmeters == expected_flowmeters

    # Test get_by_id
    flowmeter = repo.get_by_id(0)
    assert flowmeter == expected_flowmeters[0]

    # Test set_state
    new_reading = SensorReading(timestamp_ns=1730906908814683100, value=42.42)
    expected = Flowmeter(id=0, current_reading=new_reading)
    flowmeter = repo.post_reading(0, new_reading)
    assert repo.flowmeters[0] == expected
    assert flowmeter == expected
