# Changelog

## [1.4.0](https://github.com/FelizCoder/crewstand.backend/compare/v1.3.1...v1.4.0) (2025-04-08)


### Features

* **api/missions:** Allow bulk mission queuing for FlowControlMission ([fd2db49](https://github.com/FelizCoder/crewstand.backend/commit/fd2db49de17d2da94ec6312cfda8f25214229b4f)), closes [#89](https://github.com/FelizCoder/crewstand.backend/issues/89)
* **missions:** add automatic mission wait time configuration ([c755082](https://github.com/FelizCoder/crewstand.backend/commit/c755082ba4b18820dfe94b7d194e1010c532fd7c)), closes [#89](https://github.com/FelizCoder/crewstand.backend/issues/89)
* **missions:** Enhance Mission Management & InfluxDB Logging ([8bb9aeb](https://github.com/FelizCoder/crewstand.backend/commit/8bb9aeb829b1f2b1a7fd9faf50f0e0cce39d8346)), closes [#84](https://github.com/FelizCoder/crewstand.backend/issues/84)
* **missions:** implement mission execution management ([e27ca8d](https://github.com/FelizCoder/crewstand.backend/commit/e27ca8d7199ce1cfb724ab769a97d861f5cd1be6)), closes [#81](https://github.com/FelizCoder/crewstand.backend/issues/81)
* start uvicorn on init main ([6f0afb9](https://github.com/FelizCoder/crewstand.backend/commit/6f0afb93b28b22d9465c5bb69153e344ee4e59db))

## [1.3.1](https://github.com/FelizCoder/crewstand.backend/compare/v1.3.0...v1.3.1) (2025-02-26)


### Bug Fixes

* Clear setpoint at end of flow mission ([a0973cb](https://github.com/FelizCoder/crewstand.backend/commit/a0973cbceedf7c3a1204511e31b4bd143d25e20e))

## [1.3.0](https://github.com/FelizCoder/crewstand.backend/compare/v1.2.1...v1.3.0) (2025-02-25)


### Features

* **missions:** add endpoint to post mission to queue ([14b0758](https://github.com/FelizCoder/crewstand.backend/commit/14b07588051a5b64a5c84dc92e78ad46aea798f6)), closes [#77](https://github.com/FelizCoder/crewstand.backend/issues/77)
* **missions:** implement flow control mission execution ([98e2475](https://github.com/FelizCoder/crewstand.backend/commit/98e2475ac7171da49357cc93fd605567acdc7ddc)), closes [#77](https://github.com/FelizCoder/crewstand.backend/issues/77)

## [1.2.1](https://github.com/FelizCoder/crewstand.backend/compare/v1.2.0...v1.2.1) (2025-02-18)


### Bug Fixes

* **actuators & logging:** ensure accurate timestamping for proportional actuator positions ([0ff032a](https://github.com/FelizCoder/crewstand.backend/commit/0ff032ab8e4ae6589a1296eec1f38809d9dcd914)), closes [#74](https://github.com/FelizCoder/crewstand.backend/issues/74)
* ensure ProportionalValve state is within range ([1d30ff5](https://github.com/FelizCoder/crewstand.backend/commit/1d30ff50f9f530424ff93541e8105f9e6ab92c90)), closes [#72](https://github.com/FelizCoder/crewstand.backend/issues/72)
* **influx:** change state_origin tag to type in Influx write ([b4156f6](https://github.com/FelizCoder/crewstand.backend/commit/b4156f62aa1740da34274a814006458badc3b383)), closes [#74](https://github.com/FelizCoder/crewstand.backend/issues/74)

## [1.2.0](https://github.com/FelizCoder/crewstand.backend/compare/v1.1.0...v1.2.0) (2025-01-23)


### Features

* **api:** add `/v1/info/version` endpoint ([c05d637](https://github.com/FelizCoder/crewstand.backend/commit/c05d637145d32503715bffda3d60cf4b8ac447a7))
* **sensors:** Enhance Sensor Model & API with Setpoint Management ([472bf6b](https://github.com/FelizCoder/crewstand.backend/commit/472bf6bbe5457945ffc0da3650b8a56dba3d7ce6)), closes [#63](https://github.com/FelizCoder/crewstand.backend/issues/63)

## [1.1.0](https://github.com/FelizCoder/crewstand.backend/compare/v1.0.0...v1.1.0) (2025-01-08)


### Features

* **actuators, websocket, influx:** Enhance Actuator WebSocket Connectivity & Influx Timeout ([6210e19](https://github.com/FelizCoder/crewstand.backend/commit/6210e19c39e8ade922997f2c52873f3c22cab617))
* **ActuatorService:** Enhance Actuator State Management with WebSocket and InfluxDB Integration ([14ac37b](https://github.com/FelizCoder/crewstand.backend/commit/14ac37becbd8d3ee6fcd6902c329fda8da746a0e))
* **app/utils/influx_client:** Enhance InfluxConnector with improved documentation, error handling, and refactored write operations ([63ac241](https://github.com/FelizCoder/crewstand.backend/commit/63ac241dbdd326b274b9f1033190367388ca763c)), closes [#67](https://github.com/FelizCoder/crewstand.backend/issues/67)
* **influx_client:** Standardize Field Keys & Introduce "state_origin" Tag ([3e0c32f](https://github.com/FelizCoder/crewstand.backend/commit/3e0c32f4f4eab8193df0eaa842c16558931f8c32))
* Introduce WebSocket Support for Real-time Actuator State Updates ([e330927](https://github.com/FelizCoder/crewstand.backend/commit/e33092757d71037908a973ffa04a157eb3842a76)), closes [#53](https://github.com/FelizCoder/crewstand.backend/issues/53)
* **ProportionalActuator:** Enhance with current position tracking and InfluxDB logging ([d8c6314](https://github.com/FelizCoder/crewstand.backend/commit/d8c63148b69c323f0756aab17e1d95eec3d21e1b))

## [1.0.0](https://github.com/FelizCoder/crewstand.backend/compare/v0.11.0...v1.0.0) (2024-12-16)


### ⚠ BREAKING CHANGES

* **models:** The following actuator-specific state attributes have been replaced:
    - `SolenoidValve`: `open` -> `state` (bool)
    - `Pump`: `running` -> `state` (bool)
    - `ProportionalValve`: `position` -> `state` (float)

### Code Refactoring

* **models:** unify actuator state attributes into a single `state` field ([474a2d1](https://github.com/FelizCoder/crewstand.backend/commit/474a2d1a5e84717d122fbc733f96360591e27c19))

## [0.11.0](https://github.com/FelizCoder/crewstand.backend/compare/v0.10.0...v0.11.0) (2024-12-12)


### Features

* **influxdb:** add InfluxDB configuration and client ([8d0ca0f](https://github.com/FelizCoder/crewstand.backend/commit/8d0ca0f5f766e22218f43aa9ecf0c59bb20638dc)), closes [#56](https://github.com/FelizCoder/crewstand.backend/issues/56)
* **sensors:** integrate InfluxDB logging ([d1fd1ed](https://github.com/FelizCoder/crewstand.backend/commit/d1fd1ed917c5881e6c7ff665755cbf159ed1a607)), closes [#56](https://github.com/FelizCoder/crewstand.backend/issues/56)

## [0.10.0](https://github.com/FelizCoder/crewstand.backend/compare/v0.9.1...v0.10.0) (2024-12-02)


### Features

* add support for multiple flowmeters ([6178afe](https://github.com/FelizCoder/crewstand.backend/commit/6178afedaf54f29070ac5a0a93522109117110e0)), closes [#55](https://github.com/FelizCoder/crewstand.backend/issues/55)

## [0.9.1](https://github.com/FelizCoder/crewstand.backend/compare/v0.9.0...v0.9.1) (2024-11-26)


### Bug Fixes

* **ProportionalCAN:** add `set_state` return value ([b43c14b](https://github.com/FelizCoder/crewstand.backend/commit/b43c14b160df5cf676b54487c2a50c1eb4e3c681))
* **ProportionalCAN:** change default in `get_by_id` ([87a4071](https://github.com/FelizCoder/crewstand.backend/commit/87a407148a6e2abd5ec1fb5e0612c378e76c4cbb))

## [0.9.0](https://github.com/FelizCoder/crewstand.backend/compare/v0.8.0...v0.9.0) (2024-11-26)


### Features

* redirect root to `/docs` ([9926e03](https://github.com/FelizCoder/crewstand.backend/commit/9926e038cb8ec0fac2903782498376d0e2abbaa4))


### Bug Fixes

* **proportional can:** ensure correct range and integer position ([3d8b87d](https://github.com/FelizCoder/crewstand.backend/commit/3d8b87dc75afb363e79bb4b6eda3c23058fb7211))

## [0.8.0](https://github.com/FelizCoder/crewstand.backend/compare/v0.7.0...v0.8.0) (2024-11-18)


### Features

* add websocket broadcast functionality on post reading ([65dd526](https://github.com/FelizCoder/crewstand.backend/commit/65dd5260718fe6f2f1ecd6df5e362230ab5df16c)), closes [#47](https://github.com/FelizCoder/crewstand.backend/issues/47)

## [0.7.0](https://github.com/FelizCoder/crewstand.backend/compare/v0.6.0...v0.7.0) (2024-11-11)


### Features

* **sensors:** add sensor endpoints and update OpenAPI documentation ([d90b2d7](https://github.com/FelizCoder/crewstand.backend/commit/d90b2d73a52760f91cab78c414cc1944fe1d408c)), closes [#43](https://github.com/FelizCoder/crewstand.backend/issues/43)

## [0.6.0](https://github.com/FelizCoder/crewstand.backend/compare/v0.5.1...v0.6.0) (2024-10-31)


### Features

* **can:** implement repository for opencan proportional valve ([69e8030](https://github.com/FelizCoder/crewstand.backend/commit/69e8030ff684374b8589716151be87c6e5786564)), closes [#40](https://github.com/FelizCoder/crewstand.backend/issues/40)
* **shutdown:** add shutdown event handling and logging for proportional service and GPIO device ([baf149c](https://github.com/FelizCoder/crewstand.backend/commit/baf149cb7651fdea7c2a4f2a390a73cab2714bed))

## [0.5.1](https://github.com/FelizCoder/crewstand.backend/compare/v0.5.0...v0.5.1) (2024-10-22)


### Bug Fixes

* **icon:** Icon for swagger docs ([f81c005](https://github.com/FelizCoder/crewstand.backend/commit/f81c0050b373c73c02116ae075c9565f5102afd4))

## [0.5.0](https://github.com/FelizCoder/crewstand.backend/compare/v0.4.2...v0.5.0) (2024-10-22)


### Features

* add favicon endpoint and ([a9f13a3](https://github.com/FelizCoder/crewstand.backend/commit/a9f13a304d871a9aca45ebd0ada5b4742093a299))

## [0.4.2](https://github.com/FelizCoder/crewstand.backend/compare/v0.4.1...v0.4.2) (2024-10-17)


### Bug Fixes

* **gpio:** GPIO close on graceful shutdown ([8cf8fdb](https://github.com/FelizCoder/crewstand.backend/commit/8cf8fdbb85529745c1699d346f62a3d84a78d567)), closes [#29](https://github.com/FelizCoder/crewstand.backend/issues/29)

## [0.4.1](https://github.com/FelizCoder/crewstand.backend/compare/v0.4.0...v0.4.1) (2024-10-16)


### Bug Fixes

* **deps:** add additional GPIO libraries to requirements ([f7b185d](https://github.com/FelizCoder/crewstand.backend/commit/f7b185d4a5da987459109798518684b4248dd939))

## [0.4.0](https://github.com/FelizCoder/crewstand.backend/compare/v0.3.0...v0.4.0) (2024-10-16)


### Features

* update actuator API to use service methods ([1cf82c7](https://github.com/FelizCoder/crewstand.backend/commit/1cf82c7705afcb0d45f2d6261d6b265bb97f69d2))


### Bug Fixes

* update configuration and fix type errors ([a2ad70b](https://github.com/FelizCoder/crewstand.backend/commit/a2ad70b47a49d094f8345e4c09fb92d7f4748c87))

## [0.3.0](https://github.com/FelizCoder/crewstand.backend/compare/v0.2.0...v0.3.0) (2024-10-15)


### Features

* **actuators:** Add GPIO Control ([e313c45](https://github.com/FelizCoder/crewstand.backend/commit/e313c450f182ded8561320f462b506f451127fb2))
* add GPIO configuration ([c1c496e](https://github.com/FelizCoder/crewstand.backend/commit/c1c496ed79f0bcfd4c6be8e0fa2c52ad3f8636b2))
* **api:** enhanced input validation ([6a8e694](https://github.com/FelizCoder/crewstand.backend/commit/6a8e694e371725a4c9628fcec7e7007a24dc50e0))
* enhanced logging ([cbd72f6](https://github.com/FelizCoder/crewstand.backend/commit/cbd72f6809a413d6202cc37d1d2d6a39e19ea291))
* **GPIO:** add shutdown event to gracefully handle GPIO device closure ([7c5663e](https://github.com/FelizCoder/crewstand.backend/commit/7c5663e20f50726294989f28b79c2161c7551da4))

## [0.2.0](https://github.com/FelizCoder/crewstand.backend/compare/v0.1.1...v0.2.0) (2024-10-13)


### Features

* **actuators:** mock services in actuator module ([ddb4f33](https://github.com/FelizCoder/crewstand.backend/commit/ddb4f330315e370ea42bb0a38873fc2cbd3c992e))

## [0.1.1](https://github.com/FelizCoder/crewstand.backend/compare/v0.1.0...v0.1.1) (2024-10-10)


### Bug Fixes

* **docker:** import version from repo ([e282566](https://github.com/FelizCoder/crewstand.backend/commit/e28256669c582ca734b2cbfc50fd84c3631ff001))

## [0.1.0](https://github.com/FelizCoder/crewstand.backend/compare/v0.1.0...v0.1.0) (2024-10-08)


### Features

* backend api implementation ([b1f81e3](https://github.com/FelizCoder/crewstand.backend/commit/b1f81e3febc2fc0967b784b79c086ad00ff54c85))
* initial backend setup ([0d5ce71](https://github.com/FelizCoder/crewstand.backend/commit/0d5ce7192d351ba965b257beb164a5f8d1cabcd5))
* track openapi.json in git repository ([f0489b6](https://github.com/FelizCoder/crewstand.backend/commit/f0489b697ebde9b8a494536dea06aa13457caa38))
* update FastAPI initialization with project name and version from config ([8add1a9](https://github.com/FelizCoder/crewstand.backend/commit/8add1a9a5e83e8afc544cbeca0674716369fc011))


### Miscellaneous Chores

* set initial release ([8c217f2](https://github.com/FelizCoder/crewstand.backend/commit/8c217f246bc7ddc157c80dda1eb9cdf1c7cdbdbc))

## 0.1.0 (2024-10-08)


### Features

* backend api implementation ([b1f81e3](https://github.com/FelizCoder/crewstand.backend/commit/b1f81e3febc2fc0967b784b79c086ad00ff54c85))
* initial backend setup ([0d5ce71](https://github.com/FelizCoder/crewstand.backend/commit/0d5ce7192d351ba965b257beb164a5f8d1cabcd5))
* track openapi.json in git repository ([f0489b6](https://github.com/FelizCoder/crewstand.backend/commit/f0489b697ebde9b8a494536dea06aa13457caa38))
* update FastAPI initialization with project name and version from config ([8add1a9](https://github.com/FelizCoder/crewstand.backend/commit/8add1a9a5e83e8afc544cbeca0674716369fc011))


### Miscellaneous Chores

* set initial release ([8c217f2](https://github.com/FelizCoder/crewstand.backend/commit/8c217f246bc7ddc157c80dda1eb9cdf1c7cdbdbc))

## 0.1.0 (2024-10-03)


### Features

* initial backend setup ([0d5ce71](https://github.com/FelizCoder/crewstand.backend/commit/0d5ce7192d351ba965b257beb164a5f8d1cabcd5))


### Miscellaneous Chores

* set initial release ([8c217f2](https://github.com/FelizCoder/crewstand.backend/commit/8c217f246bc7ddc157c80dda1eb9cdf1c7cdbdbc))
