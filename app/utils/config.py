import os
import logging

def read_version():
    with open("version.txt", "r") as file:
        return file.read().strip()

class Config:
    PROJECT_NAME = os.getenv("PROJECT_NAME", default="swncrew backend")
    VERSION = read_version()
    
config = Config()

logging.debug(f"Start project with current configuration \n {config}")