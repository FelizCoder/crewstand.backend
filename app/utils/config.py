from typing import Union

from .logger import logger
from pydantic_settings import BaseSettings, SettingsConfigDict

def read_version():
    with open("version.txt", "r") as file:
        return file.read().strip()

class Config(BaseSettings):
    PROJECT_NAME: str = 'swncrew backend'
    VERSION: str = read_version()
    GPIOZERO_PIN_FACTORY: Union[str, None] = None
    SOLENOID_GPIO: str
    PROPORTIONAL_GPIO: str
    PUMP_GPIO: str
    DEBUG_LEVEL: str = 'INFO'
    GPIO_MODE: str = ""
    
    model_config = SettingsConfigDict(env_file=".env.local")

settings = Config()

logger.setLevel(settings.DEBUG_LEVEL.upper()) 

logger.debug(f"Start project with current configuration \n {settings.model_dump()}")

if settings.GPIO_MODE.lower() == "mock":
    from gpiozero import Device
    from gpiozero.pins.mock import MockFactory, MockPWMPin
    logger.debug("Use mock GPIO mode")
    Device.pin_factory = MockFactory(pin_class=MockPWMPin)
