# Crewstand Backend

Backend for the CREW test stand control

- [Crewstand Backend](#crewstand-backend)
  - [Dependencies](#dependencies)
  - [Configuration](#configuration)
    - [Debugging](#debugging)
    - [GPIO Mode Settings](#gpio-mode-settings)
    - [CAN Usage and Interface Setup](#can-usage-and-interface-setup)
  - [Quickstart Guide](#quickstart-guide)
  - [Running with Docker](#running-with-docker)

## Dependencies

This project relies on the following dependencies, see their official documentation for more information:

- [FastAPI](https://fastapi.tiangolo.com/learn/)
- [GPIOZero](https://gpiozero.readthedocs.io/en/latest/)

## Configuration

The [`config.py`](app\utils\config.py) file in the project allows for several configurations to be set via environment variables or a [`.env.local`](.env.example) file. Below is a list of all the configurable options and their descriptions:
| Configuration Variable | Description | Default | Example | Required |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- | --------------- | -------- |
| DEBUG_LEVEL | The level of debugging information to log. | INFO | DEBUG | No |
| FLOWMETER_COUNT | The number of flowmeters connected to the system. | 1  | 2 |
| GPIO_MODE | Specifies the mode of GPIO usage. | None | mock | No |
| GPIOZERO_PIN_FACTORY | Determines the pin factory to use when interacting with GPIO pins. This setting affects how the GPIOZero library operates. For more information, refer to the [official GPIOZero documentation](https://gpiozero.readthedocs.io/en/latest/api_pins.html#changing-the-pin-factory). Although not used in the project, this variable's value is read by the Config to display it for debugging purposes. | None | mock | No |
| MISSION_WAIT_SECONDS | The number of seconds the system waits before starting the next mission automatically. | 10 | 5 | No |
| PROJECT_NAME | The name of the project. | swncrew backend | swncrew backend | No |
| PROPORTIONAL_CAN_INTERFACE | The name of the CAN interface to use for the proportional valves. | can0 | can1 | No |
| PROPORTIONAL_GPIO | A comma-separated string of GPIO pins used for the proportional valves. | None | 10,11 | No |
| PROPORTIONAL_MODE | Specifies the control mode for the proportional valves. It can be set to `GPIO` for GPIO control, which generates a PWM signal on the Pins defined in `PROPORTIONAL_GPIO`. This option is useful for development as the output can be mapped to an LED and supports the mock mode. To use `CAN`, the [CAN interface must be set up properly](#can-usage-and-interface-setup) on the device.| Not Set | CAN | Yes |
| PUMP_GPIO | A comma-separated string of GPIO pins used for the pumps. | Not set | 20,21,23,24 | Yes |
| SOLENOID_GPIO | A comma-separated string of GPIO pins used for the solenoid valves. | Not set | 4,5,6 | Yes |
| VERSION | The version of the software. | Read from [`version.txt`](version.txt) | 0.0.1 | No |

### Debugging

The project uses a logger to log messages in the console. The debug level is set based on the DEBUG_LEVEL configuration. Possible debug levels include

- DEBUG
- INFO
- WARNING
- ERROR
- CRITICAL

### GPIO Mode Settings

To control the GPIO mode, set the `GPIO_MODE` configuration variable. By default, this variable is not set, which allows the project to use actual GPIO pins. However, for testing and development purposes, you can set `GPIO_MODE` to `mock` to utilize a simulated GPIO factory, eliminating the need for physical hardware interaction.

### CAN Usage and Interface Setup

To use the CAN bus control for the proportional valves, you need to set up the CAN interface on your device. Refer to the official documentation for your specific device to configure the CAN interface (e.g. [Waveshare CAN-HAT](https://www.waveshare.com/wiki/RS485_CAN_HAT)).

Following instructions apply for setting up and using the [Waveshare RS485 CAN HAT](https://www.waveshare.com/wiki/RS485_CAN_HAT) on a Raspberry Pi running Ubuntu. Please note that the steps might differ if you are using another device or a different configuration.

1. **Configure Your Raspberry Pi**:

- Add the following lines to your `/boot/firmware/config.txt` to enable SPI and configure the CAN interface:

```
dtparam=spi=on
dtoverlay=mcp2515-can0,oscillator=12000000,interrupt=25,spimaxfrequency=2000>
enable uart=1
```

- Reboot your Raspberry Pi to apply the changes.

2. **Bring Up the CAN Interface**

```bash
sudo ip link set can0 up type can bitrate 500000
sudo ifconfig can0 up
```

- You might initialize the CAN interface on boot.

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
docker run -p 5000:5000 -e DEBUG_LEVEL=DEBUG -e GPIO_MODE=mock -e GPIOZERO_PIN_FACTORY=mock -e PROJECT_NAME=swncrew_backend -e PROPORTIONAL_GPIO=10,11 -e PROPORTIONAL_MODE=GPIO -e PUMP_GPIO=20,21,23,24 -e SOLENOID_GPIO=4,5,6 ghcr.io/felizcoder/crewstand.backend:latest
```
