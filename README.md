# crewstand.backend
Backend for the CREW test stand control

## Configuration
The config.py file in the project allows for several configurations to be set via environment variables or a [`.env.local`](.env.example) file. Below is a list of all the configurable options and their descriptions:

| Configuration Variable | Description                                                             | Default | Example                |
| ---------------------- | ----------------------------------------------------------------------- | ------- | ---------------------- |
| PROJECT_NAME           | The name of the project.                                                | None    | swncrew backend |
| VERSION                | The version of the software.                                            | None    | Read from version.txt  |
| GPIOZERO_PIN_FACTORY   | Specifies the type of GPIO pins to use.                                 | None    | mock                   |
| SOLENOID_GPIO          | A comma-separated string of GPIO pins used for the solenoid valves.     | None    | 4,5,6                  |
| PROPORTIONAL_GPIO      | A comma-separated string of GPIO pins used for the proportional valves. | None    | 10,11                  |
| PUMP_GPIO              | A comma-separated string of GPIO pins used for the pumps.               | None    | 20,21,23,24            |
| DEBUG_LEVEL            | The level of debugging information to log.                              | INFO    | DEBUG                  |
| GPIO_MODE              | Specifies the mode of GPIO usage.                                       | None    | mock                   |

### Logging Configuration
The project uses a logger to log messages in the console. The debug level is set based on the DEBUG_LEVEL configuration. Possible debug levels include 
- DEBUG
- INFO
- WARNING 
- ERROR 
- CRITICAL

### Mock GPIO Mode
If GPIO_MODE is set to mock, the project will use a mock GPIO factory for testing purposes. This is useful for development and testing without physically interacting with hardware.
You should be able to use the actual GPIO pins if GPIO_MODE is not set.