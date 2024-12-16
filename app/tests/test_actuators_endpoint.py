# pylint: disable=C0116

import pytest
from fastapi.testclient import TestClient
from fastapi.exceptions import RequestValidationError
from app.api.v1.endpoints.actuators import router
from app.models.actuators import ProportionalValve, Pump, SolenoidValve
from app.services.actuators.proportional import ProportionalService
from app.services.actuators.pump import PumpService
from app.services.actuators.solenoid import SolenoidService


@pytest.fixture(name="client")
def setup_test_client():
    with TestClient(router) as client:
        yield client


def test_get_all_actuators(client, mocker):
    expected_solenoid = [SolenoidValve(id=1, state=False)]
    expected_proportional = [ProportionalValve(id=2, state=42)]
    expected_pump = [Pump(id=3, state=True)]

    mocker.patch.object(SolenoidService, "get_all", return_value=expected_solenoid)
    mocker.patch.object(
        ProportionalService,
        "get_all",
        return_value=expected_proportional,
    )
    mocker.patch.object(PumpService, "get_all", return_value=expected_pump)

    response = client.get("/")

    assert response.status_code == 200
    actuators = response.json()
    assert len(actuators) == 3
    assert {actuator["id"] for actuator in actuators} == {1, 2, 3}


def test_solenoid_get_all(client, mocker):
    expected = [SolenoidValve(id=1, state=True), SolenoidValve(id=2, state=False)]
    mocker.patch.object(
        SolenoidService,
        "get_all",
        return_value=expected,
    )

    response = client.get("/solenoid/")
    assert response.status_code == 200

    # Test response can parse to SolenoidValve model
    actual = [SolenoidValve(**solenoid) for solenoid in response.json()]
    assert actual == expected


def test_solenoid_get_by_id(client, mocker):
    expected = SolenoidValve(id=1, state=True)
    mocker.patch.object(
        SolenoidService,
        "get_by_id",
        return_value=expected,
    )

    response = client.get("/solenoid/1")
    assert response.status_code == 200

    # Test response can parse to SolenoidValve model
    actual = SolenoidValve(**response.json())
    assert actual == expected


def test_solenoid_set(client, mocker):
    def set_state_side_effect(request: SolenoidValve):
        return request

    mocker.patch.object(
        SolenoidService,
        "set_state",
        side_effect=set_state_side_effect,
    )

    # Test setting state to False
    expected = SolenoidValve(id=42, state=False)
    response = client.post("/solenoid/set", data=expected.model_dump_json())
    assert response.status_code == 200
    actual = SolenoidValve(**response.json())
    assert actual == expected
    # Test setting state to True
    expected = SolenoidValve(id=24, state=True)
    response = client.post("/solenoid/set", data=expected.model_dump_json())
    assert response.status_code == 200
    actual = SolenoidValve(**response.json())
    assert actual == expected


def test_solenoid_set_request_invalid(client):
    requests = [Pump(id=1, state=True), ProportionalValve(id=1, state=42)]

    for request in requests:
        with pytest.raises(RequestValidationError) as exc_info:
            client.post("solenoid/set", data=request.model_dump_json())
        assert exc_info.type == RequestValidationError


def test_proportional_get_all(client, mocker):
    expected = [
        ProportionalValve(id=1, state=42),
        ProportionalValve(id=2, state=24),
    ]

    mocker.patch.object(
        ProportionalService,
        "get_all",
        return_value=expected,
    )

    response = client.get("/proportional/")
    assert response.status_code == 200

    # Test response can parse to ProportionalValve model
    actual = [ProportionalValve(**valve) for valve in response.json()]
    assert actual == expected


def test_proportional_get_by_id(client, mocker):
    expected = ProportionalValve(id=1, state=42)
    mocker.patch.object(
        ProportionalService,
        "get_by_id",
        return_value=expected,
    )

    response = client.get("/proportional/1")
    assert response.status_code == 200

    # Test response can parse to ProportionalValve model
    actual = ProportionalValve(**response.json())
    assert actual == expected


def test_proportional_set(client, mocker):
    def set_position_side_effect(request: ProportionalValve):
        return request

    mocker.patch.object(
        ProportionalService,
        "set_state",
        side_effect=set_position_side_effect,
    )

    # Test setting position to 42
    expected = ProportionalValve(id=1, state=42)
    response = client.post("/proportional/set", data=expected.model_dump_json())
    assert response.status_code == 200
    actual = ProportionalValve(**response.json())
    assert actual == expected

    # Test setting position to 24
    expected = ProportionalValve(id=2, state=24)
    response = client.post("/proportional/set", data=expected.model_dump_json())
    assert response.status_code == 200
    actual = ProportionalValve(**response.json())
    assert actual == expected


def test_proportional_set_request_invalid(client):
    requests = [
        Pump(id=1, state=True),  # invalid request for ProportionalValve endpoint
        SolenoidValve(id=3, state=False),
    ]

    for request in requests:
        with pytest.raises(RequestValidationError) as exc_info:
            client.post("/proportional/set", data=request.model_dump_json())
        assert exc_info.type == RequestValidationError


def test_pump_get_all(client, mocker):
    expected = [
        Pump(id=1, state=True),
        Pump(id=2, state=False),
    ]

    mocker.patch.object(
        PumpService,
        "get_all",
        return_value=expected,
    )

    response = client.get("/pump/")
    assert response.status_code == 200

    # Test response can parse to Pump model
    actual = [Pump(**valve) for valve in response.json()]
    assert actual == expected


def test_pump_set(client, mocker):
    def set_state_side_effect(request: Pump):
        return request

    mocker.patch.object(
        PumpService,
        "set_state",
        side_effect=set_state_side_effect,
    )

    # Test setting state to True
    expected = Pump(id=1, state=True)
    response = client.post("/pump/set", data=expected.model_dump_json())
    assert response.status_code == 200
    actual = Pump(**response.json())
    assert actual == expected
    # Test setting state to False
    expected = Pump(id=2, state=False)
    response = client.post("/pump/set", data=expected.model_dump_json())
    assert response.status_code == 200
    actual = Pump(**response.json())
    assert actual == expected


def test_pump_get_by_id(client, mocker):
    expected = Pump(id=1, state=True)

    mocker.patch.object(
        PumpService,
        "get_by_id",
        return_value=expected,
    )

    response = client.get("/pump/1")
    assert response.status_code == 200
    actual = Pump(**response.json())
    assert actual == expected


def test_pump_set_request_invalid(client):
    requests = [
        ProportionalValve(id=1, state=42),  # invalid request for Pump endpoint
        SolenoidValve(id=2, state=True),
    ]

    for request in requests:
        with pytest.raises(RequestValidationError) as exc_info:
            client.post("/pump/set", data=request.model_dump_json())
        assert exc_info.type == RequestValidationError
