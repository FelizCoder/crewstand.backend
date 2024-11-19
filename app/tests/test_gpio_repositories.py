# app/tests/test_actuators_gpio.py
import pytest
from unittest.mock import patch

from app.models.actuators import SolenoidValve, Pump, ProportionalValve
from app.repositories.actuators.GPIO.solenoid_valves import SolenoidActuator
from app.repositories.actuators.GPIO.pumps import PumpActuator
from app.repositories.actuators.GPIO.proportional_valves import ProportionalActuator


@pytest.fixture
def solenoid_actuator():
    with patch(
        "app.repositories.actuators.GPIO.solenoid_valves.settings"
    ) as mock_settings:
        mock_settings.SOLENOID_GPIO = "17,18,27,22"
        actuator = SolenoidActuator()
        return actuator


@pytest.fixture
def pump_actuator():
    with patch("app.repositories.actuators.GPIO.pumps.settings") as mock_settings:
        mock_settings.PUMP_GPIO = "17,18,27,22"
        actuator = PumpActuator()
        return actuator


@pytest.fixture
def proportional_actuator():
    with patch(
        "app.repositories.actuators.GPIO.proportional_valves.settings"
    ) as mock_settings:
        mock_settings.PROPORTIONAL_GPIO = "17,18,27,22"
        actuator = ProportionalActuator()
        return actuator


def test_solenoid_actuator(solenoid_actuator):
    # Test get_all
    solenoid_actuator.solenoids.value = [True, False, True, False]
    solenoids = solenoid_actuator.get_all()
    assert len(solenoids) == 4
    for i in range(len(solenoids)):
        assert solenoids[i].open == solenoid_actuator.solenoids[i].value
    
    # Test get_by_id
    solenoid_actuator.solenoids[1].value = False
    solenoid = solenoid_actuator.get_by_id(1)
    assert solenoid.id == 1
    assert solenoid.open is False

    # Test set_state
    assert solenoid_actuator.solenoids[3].value == 0
    solenoid_actuator.set_state(SolenoidValve(id=3, open=True))
    assert solenoid_actuator.solenoids[3].value == 1
    solenoid_actuator.set_state(SolenoidValve(id=-1, open=False))
    assert solenoid_actuator.solenoids.value == (0,0,0,0)


def test_pump_actuator(pump_actuator):
    # Test get_all
    initial_values = [False, True, False, True]
    pump_actuator.pumps.value = initial_values
    pumps = pump_actuator.get_all()
    assert len(pumps) == 4
    for i in range(len(pumps)):
        assert pumps[i].running == pump_actuator.pumps[i].value
    
    # Test get_by_id
    pump_actuator.pumps[2].value = True
    pump = pump_actuator.get_by_id(2)
    assert pump.id == 2
    assert pump.running is True

    # Test set_state
    assert pump_actuator.pumps[3].value == 1
    pump_actuator.set_state(Pump(id=3, running=False))
    assert pump_actuator.pumps[3].value == 0
    assert pump_actuator.set_state(Pump(id=-1, running=True))
    assert pump_actuator.pumps.value == (1,1,1,1)


def test_proportional_actuator(proportional_actuator):
    # Test get_all
    initial_values = [0.25, 0.75, 0.50, 0.10]
    proportional_actuator.proportionals.value = initial_values
    valves = proportional_actuator.get_all()
    assert len(valves) == 4
    for i in range(len(valves)):
        assert valves[i].position == initial_values[i] * proportional_actuator.factor
    
    # Test get_by_id
    proportional_actuator.proportionals[3].value = 0.80
    valve = proportional_actuator.get_by_id(3)
    assert valve.id == 3
    assert valve.position == 80

    # Test set_state
    assert proportional_actuator.proportionals[2].value == 0.5
    proportional_actuator.set_state(ProportionalValve(id=2, position=100))
    assert proportional_actuator.proportionals[2].value == 1.0
    proportional_actuator.set_state(ProportionalValve(id=-1, position=50))
    assert proportional_actuator.proportionals.value == (0.50, 0.50, 0.50, 0.50)
