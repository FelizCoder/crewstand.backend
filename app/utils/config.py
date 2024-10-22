from typing import Union
from gpiozero import Device
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.utils.logger import logger


def read_version():
    """Read the version from `version.txt` inside the root directory."""
    with open("version.txt", "r", encoding="utf-8") as file:
        return file.read().strip()


class Config(BaseSettings):
    """Holds configuration settings for the project."""

    PROJECT_NAME: str = "swncrew backend"
    VERSION: str = read_version()
    GPIOZERO_PIN_FACTORY: Union[str, None] = None
    SOLENOID_GPIO: str
    PROPORTIONAL_GPIO: str
    PUMP_GPIO: str
    DEBUG_LEVEL: str = "INFO"
    GPIO_MODE: str = ""
    DEVICE: Union[Device, None] = None

    model_config = SettingsConfigDict(env_file=".env.local")


settings = Config()

logger.setLevel(settings.DEBUG_LEVEL.upper())

logger.debug(
    "Start project with current configuration \n %s", settings.model_dump_json(indent=2)
)

if settings.GPIO_MODE.lower() == "mock":
    from gpiozero.pins.mock import MockFactory, MockPWMPin

    logger.debug("Use mock GPIO mode")
    Device.pin_factory = MockFactory(pin_class=MockPWMPin)
    settings.DEVICE = Device()
