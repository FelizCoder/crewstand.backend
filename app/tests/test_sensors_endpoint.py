# pylint: disable=C0116

from contextlib import ExitStack
from fastapi.exceptions import RequestValidationError
import pytest
from fastapi.testclient import TestClient
from app.api.v1.endpoints.sensors import router
from app.models.sensors import Flowmeter, SensorReading
from app.services.sensors.flowmeter import FlowmeterService


@pytest.fixture(name="client")
def setup_test_client():
    with TestClient(router) as client:
        yield client


def test_get_all_sensors(client, mocker):
    expected_flowmeters = [Flowmeter(id=1), Flowmeter(id=2)]

    mocker.patch.object(FlowmeterService, "get_all", return_value=expected_flowmeters)

    response = client.get("/")

    assert response.status_code == 200
    actual = [Flowmeter(**flowmeter) for flowmeter in response.json()]
    assert actual == expected_flowmeters


def test_flowmeter_get_all(client, mocker):
    expected = [Flowmeter(id=1), Flowmeter(id=2)]

    mocker.patch.object(FlowmeterService, "get_all", return_value=expected)

    response = client.get("/flowmeters/")
    assert response.status_code == 200

    # Test response can parse to Flowmeter model
    actual = [Flowmeter(**flowmeter) for flowmeter in response.json()]
    assert actual == expected


def test_flowmeter_get_by_id(client, mocker):
    sensor_id = 0
    expected = Flowmeter(id=sensor_id, current_reading=None)

    mocker.patch.object(FlowmeterService, "get_by_id", return_value=expected)

    response = client.get(f"/flowmeters/{sensor_id}")
    assert response.status_code == 200

    # Test response can parse to Flowmeter model
    actual = Flowmeter(**response.json())
    assert actual == expected


def test_flowmeter_post_reading(client, mocker):
    sensor_id = 0
    new_reading = SensorReading(value=42.0, timestamp_ns=1730906908814683100)
    expected = Flowmeter(id=sensor_id, current_reading=new_reading)

    def patch_reading_side_effect(sensor_id, reading: SensorReading):
        return Flowmeter(id=sensor_id, current_reading=reading)

    mocker.patch.object(
        FlowmeterService, "post_reading", side_effect=patch_reading_side_effect
    )

    response = client.post(
        f"/flowmeters/{sensor_id}/reading", data=new_reading.model_dump_json()
    )
    assert response.status_code == 200
    actual = Flowmeter(**response.json())
    assert actual == expected


def test_flowmeter_post_reading_request_invalid(client):
    sensor_id = 1
    invalid_readings = [
        {"value": "invalid_str", "timestamp_ns": "non_int"},
        {"invalid_field": 42.0, "another_invalid_field": 0},
    ]

    for reading in invalid_readings:
        with pytest.raises(RequestValidationError) as exc_info:
            _ = client.post(f"/flowmeters/{sensor_id}/reading", data=reading)
        assert (
            exc_info.type == RequestValidationError
        )  # Unprocessable Entity (validation error)


def test_websocket_initial_reading(client, mocker):
    sensor_id = 0
    expected = SensorReading(value=42.0, timestamp_ns=1730906908814683100)
    flowmeter = Flowmeter(id=sensor_id, current_reading=expected)

    mocker.patch.object(FlowmeterService, "get_by_id", return_value=flowmeter)

    with client.websocket_connect(f"/flowmeters/ws/{sensor_id}") as websocket:
        data = websocket.receive_text()
        assert data == expected.model_dump_json()
