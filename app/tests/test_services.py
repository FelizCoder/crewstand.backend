# pylint: disable=C0116
# pylint: disable=C0115

from unittest.mock import MagicMock
from fastapi import HTTPException
import pytest

from app.models.actuators import ActuatorEnum, ActuatorRepository, Actuator
from app.services.actuators.service import ActuatorService


class MockActuator(Actuator):
    def __init__(self, actuator_id):
        super().__init__(type=ActuatorEnum.PUMP, id=actuator_id)


# Fixtures
@pytest.fixture(name="repository")
def mock_actuator_repository():
    repository = MagicMock(spec=ActuatorRepository)
    repository.count = 5  # Assume there are 5 actuators in the repository
    return repository


@pytest.fixture(name="service")
def actuator_service(repository):
    return ActuatorService(repository, MockActuator)


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


def test_set_state_actuator_valid_id(service, repository):
    # Arrange
    actuator = MockActuator(3)
    repository.set_state.return_value = actuator

    # Act
    result = service.set_state(actuator)

    # Assert
    assert result == actuator
    repository.set_state.assert_called_once_with(actuator)


def test_set_state_actuator_invalid_id(service):
    # Arrange
    actuator = MockActuator(10)

    # Act & Assert
    with pytest.raises(HTTPException) as e:
        service.set_state(actuator)

    assert e.value.status_code == 422
    assert e.value.detail[0]["msg"] == "Input must be lower than 5"
