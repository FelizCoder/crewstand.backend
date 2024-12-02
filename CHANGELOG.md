# Changelog

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
