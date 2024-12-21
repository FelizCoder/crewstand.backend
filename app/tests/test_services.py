# pylint: disable=C0116
# pylint: disable=C0115

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import HTTPException
from app.services.actuators.service import ActuatorService
from app.models.actuators import ActuatorEnum, ActuatorRepository, Actuator
from app.utils.influx_client import InfluxConnector
from app.utils.websocket_manager import WebSocketManager


class MockActuator(Actuator):
    def __init__(self, actuator_id, state=True):
        super().__init__(type=ActuatorEnum.PUMP, id=actuator_id, state=state)


# Fixtures
@pytest.fixture(name="repository")
def mock_actuator_repository():
    repository = MagicMock(spec=ActuatorRepository)
    repository.count = 5  # Assume there are 5 actuators in the repository
    return repository


@pytest.fixture(name="influx")
def mock_influx_connector():
    return MagicMock(spec=InfluxConnector)


@pytest.fixture(name="websocket")
def mock_websocket_manager():
    return AsyncMock(spec=WebSocketManager)


@pytest.fixture(name="service")
def actuator_service(repository, influx, websocket):
    service = ActuatorService(repository, MockActuator)
    service.database = influx
    service.websocket_manager = websocket
    return service


# Tests
def test_get_all_actuators(service, repository):
    # Arrange
    actuators = [MockActuator(i) for i in range(5)]
    repository.get_all.return_value = actuators

    # Act
    result = service.get_all()

    # Assert
    assert result == actuators
    repository.get_all.assert_called_once()


def test_get_actuator_by_id(service, repository):
    # Arrange
    actuator = MockActuator(1)
    repository.get_by_id.return_value = actuator

    # Act
    result = service.get_by_id(1)

    # Assert
    assert result == actuator
    repository.get_by_id.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_set_state_actuator_valid_id(service, repository):
    # Arrange
    actuator = MockActuator(3)
    repository.set_state.return_value = actuator

    # Act
    result = await service.set_state(actuator)

    # Assert
    assert result == actuator
    repository.set_state.assert_called_once_with(actuator)
    service.influx.write_actuator.assert_called_once_with(
        actuator, service.influx.write_actuator.call_args[0][1]
    )


@pytest.mark.asyncio
async def test_set_state_actuator_invalid_id(service, repository):
    # Arrange
    actuator = MockActuator(10)

    # Act & Assert
    with pytest.raises(HTTPException) as e:
        await service.set_state(actuator)

    assert e.value.status_code == 422
    assert e.value.detail[0]["msg"] == "Input must be lower than 5"


@pytest.mark.asyncio
async def test_set_state_actuator_id_minus_one(service, repository):
    # Arrange
    actuator = MockActuator(-1)
    repository.set_state.return_value = actuator

    # Act
    result = await service.set_state(actuator)

    # Assert
    assert result == actuator
    repository.set_state.assert_called_once_with(actuator)
    service.influx.write_actuator.assert_not_called()


@pytest.mark.asyncio
async def test_set_state_actuator_state_change(service, repository):
    # Arrange
    actuator = MockActuator(3, state=False)
    repository.set_state.return_value = actuator

    # Act
    result = await service.set_state(actuator)

    # Assert
    assert result == actuator
    repository.set_state.assert_called_once_with(actuator)
    service.influx.write_actuator.assert_called_once_with(
        actuator, service.influx.write_actuator.call_args[0][1]
    )


def test_disconnect_websocket(service):
    # Arrange
    actuator_id = 1
    websocket = MagicMock()

    # Act
    service.disconnect_websocket(actuator_id, websocket)

    # Assert
    service.websocket_manager.disconnect.assert_called_once_with(actuator_id, websocket)


@pytest.mark.asyncio
async def test_connect_websocket(service, repository):
    # Arrange
    actuator_id = 1
    websocket = AsyncMock()
    actuator = MockActuator(1)
    repository.get_by_id.return_value = actuator

    # Act
    await service.connect_websocket(actuator_id, websocket)

    # Assert
    service.websocket_manager.connect.assert_called_once_with(actuator_id, websocket)
    websocket.send_text.assert_called_once_with("True")


@pytest.mark.asyncio
async def test_broadcast_all_actuators(service, repository):
    # Arrange
    actuators = [MockActuator(i) for i in range(5)]
    repository.get_all.return_value = actuators

    # Act
    await service._broadcast_all_actuators()

    # Assert
    service.influx.write_actuator.assert_called()
    service.websocket_manager.broadcast.assert_called()
