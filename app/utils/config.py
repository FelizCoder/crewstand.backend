from typing import Literal, Union
from gpiozero import Device
from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.utils.logger import logger


def read_version():
    """Read the version from `version.txt` inside the root directory."""
    with open("version.txt", "r", encoding="utf-8") as file:
        return file.read().strip()


class Config(BaseSettings):
    """Holds configuration settings for the project."""

    DEBUG_LEVEL: str = "INFO"
    DEVICE: Union[Device, None] = None
    FLOWMETER_COUNT: int = 1
    GPIO_MODE: str = ""
    INFLUXDB_BUCKET: str
    INFLUXDB_ORG: str
    INFLUXDB_TOKEN: str
    INFLUXDB_URL: HttpUrl
    GPIOZERO_PIN_FACTORY: Union[str, None] = None
    PROJECT_NAME: str = "swncrew backend"
    PROPORTIONAL_CAN_INTERFACE: str = "can0"
    PROPORTIONAL_GPIO: Union[str, None] = None
    PROPORTIONAL_MODE: Literal["GPIO", "CAN"]
    PUMP_GPIO: str
    SOLENOID_GPIO: str
    VERSION: str = read_version()

    model_config = SettingsConfigDict(env_file=".env.local")


settings = Config()

logger.setLevel(settings.DEBUG_LEVEL.upper())

logger.info(
    "Start project with current configuration \n %s", settings.model_dump_json(indent=2)
)

if settings.GPIO_MODE.lower() == "mock":
    from gpiozero.pins.mock import MockFactory, MockPWMPin

    logger.debug("Use mock GPIO mode")
    Device.pin_factory = MockFactory(pin_class=MockPWMPin)
    settings.DEVICE = Device()
