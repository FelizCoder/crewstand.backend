# Crewstand Backend
Backend for the CREW test stand control

- [Crewstand Backend](#crewstand-backend)
  - [Dependencies](#dependencies)
  - [Configuration](#configuration)
    - [Debugging](#debugging)
    - [GPIO Mode Settings](#gpio-mode-settings)
  - [Quickstart Guide](#quickstart-guide)
  - [Running with Docker](#running-with-docker)

## Dependencies
This project relies on the following dependencies, see their official documentation for more information:
* [FastAPI](https://fastapi.tiangolo.com/learn/)
* [GPIOZero](https://gpiozero.readthedocs.io/en/latest/)

## Configuration
The [`config.py`](app\utils\config.py) file in the project allows for several configurations to be set via environment variables or a [`.env.local`](.env.example) file. Below is a list of all the configurable options and their descriptions:

| Configuration Variable | Description                                                                                                                                                                                                                                                                                                                                                                                            | Default                                | Example         | Required |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------- | --------------- | -------- |
| DEBUG_LEVEL            | The level of debugging information to log.                                                                                                                                                                                                                                                                                                                                                             | INFO                                   | DEBUG           | No       |
| GPIO_MODE              | Specifies the mode of GPIO usage.                                                                                                                                                                                                                                                                                                                                                                      | None                                   | mock            | No       |
| GPIOZERO_PIN_FACTORY   | Determines the pin factory to use when interacting with GPIO pins. This setting affects how the GPIOZero library operates. For more information, refer to the [official GPIOZero documentation](https://gpiozero.readthedocs.io/en/latest/api_pins.html#changing-the-pin-factory). Although not used in the project, this variable's value is read by the Config to display it for debugging purposes. | None                                   | mock            | No       |
| PROJECT_NAME           | The name of the project.                                                                                                                                                                                                                                                                                                                                                                               | None                                   | swncrew backend | No       |
| PROPORTIONAL_GPIO      | A comma-separated string of GPIO pins used for the proportional valves.                                                                                                                                                                                                                                                                                                                                | None                                   | 10,11           | Yes      |
| PUMP_GPIO              | A comma-separated string of GPIO pins used for the pumps.                                                                                                                                                                                                                                                                                                                                              | None                                   | 20,21,23,24     | Yes      |
| SOLENOID_GPIO          | A comma-separated string of GPIO pins used for the solenoid valves.                                                                                                                                                                                                                                                                                                                                    | None                                   | 4,5,6           | Yes      |
| VERSION                | The version of the software.                                                                                                                                                                                                                                                                                                                                                                           | Read from [`version.txt`](version.txt) | 0.0.1           | No       |

### Debugging
The project uses a logger to log messages in the console. The debug level is set based on the DEBUG_LEVEL configuration. Possible debug levels include 
- DEBUG
- INFO
- WARNING 
- ERROR 
- CRITICAL

### GPIO Mode Settings
To control the GPIO mode, set the `GPIO_MODE` configuration variable. By default, this variable is not set, which allows the project to use actual GPIO pins. However, for testing and development purposes, you can set `GPIO_MODE` to `mock` to utilize a simulated GPIO factory, eliminating the need for physical hardware interaction.

## Quickstart Guide
To get started quickly, follow these steps:

1. Clone the repository: `git clone https://github.com/FelizCoder/crewstand.backend`
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env.local` file and set the desired [configurations](#configuration) (e.g., PROJECT_NAME, VERSION, etc.)
4. Run the backend: `fastapi dev app/main.py`

## Running with Docker
You can easily run this project using Docker. Here's how:

1. **Pull the Docker image**: `docker pull ghcr.io/felizcoder/crewstand.backend:latest`
2. **Set environment variables**: Configure the [required environment variables](#configuration) using the `-e` flag.
3. **Run the Docker container**: The API will be exposed on port 5000. `docker run -p 5000:5000 -e <environment variables> ghcr.io/felizcoder/crewstand.backend:latest`
   
Example command:
```bash
docker run -p 5000:5000 -e DEBUG_LEVEL=DEBUG -e GPIO_MODE=mock -e GPIOZERO_PIN_FACTORY=mock -e PROJECT_NAME=swncrew_backend -e PROPORTIONAL_GPIO=10,11 -e PUMP_GPIO=20,21,23,24 -e SOLENOID_GPIO=4,5,6 ghcr.io/felizcoder/crewstand.backend:latest
```