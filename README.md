# Smart building rating calculator
The calculation to generate a Smart Building Rating (SBR) and SBR 'archetype'

## python-template

Centre for Net Zero's template for Python projects.

Tools:

* [Pipenv](https://github.com/pypa/pipenv) for dependency management
* [Pytest](https://github.com/pytest-dev/pytest/) for testing
* [Mypy](https://mypy.readthedocs.io/en/stable/) for type checking
* [Flake8](https://flake8.pycqa.org/en/latest/) for linting
* [isort](https://github.com/PyCQA/isort) and [black](https://github.com/psf/black) for formatting

Github Actions workflows:
* `test_and_lint.yaml` runs checks on a Ubuntu Github-hosted runner.

## Python Setup

You need to [set up your Python environment](https://docs.google.com/document/d/1Tg0eKalqOp-IJEeH7aShc9fYF5zn95H6jxEk25BLLUE/) first.

1. Clone this repo.
2. Run `make setup` in your terminal.

In step 2 this will:

* Run `pipenv sync --dev` to install dependencies.
* Install your local pre-commit environment which will be used to maintain code standards
* Check the tests work by running `pipenv run pytest`

## Performing SBR calculation

Main SBR calcuation is done with the `sbr_score` (`src/smart_building_rating_calculator/calculate_sbr_score.py`) function which takes in user inputs, and outputs:
1) SBR value (between 0 and 100)
2) SBR rating (A-G)
3) Flex Archetype (see `src/smart_building_rating_calculator/flexer_enums.py`).

Inputs must have datatypes as defined in `src/smart_building_rating_calculator/inputs.py`
- Most inputs are `bool` type (True/False)
- Others are StrEnum type e.g., `charger_power` must have a value of `EVChargerPower("3 kW")`, `EVChargerPower("7 kW")`, `EVChargerPower("22 kW")`, or `EVChargerPower("None")`
- Upon calling `sbr_score`, correct input datatypes are automatically checked for. An error is raised if input datatypes are incorrect.

Example of how to call `sbr_score` in python:

```ruby
from src.smart_building_rating_calculator.calculate_sbr_score import sbr_score
from src.smart_building_rating_calculator.inputs import (
    BatterySize,
    EVChargerPower,
    HeatingSource,
    HotWaterSource,
    SolarInverterSize,
)
sbr_val, sbr, flex_archetype = sbr_score(
        smart_meter=True,
        smart_ev_charger=True,
        charger_power=EVChargerPower("7 kW"),
        smart_v2g_enabled=True,
        home_battery=True,
        battery_size=BatterySize("8kWh or greater"),
        solar_pv=True,
        pv_inverter_size=SolarInverterSize("4 kW or less"),
        electric_heating=True,
        heating_source=HeatingSource("Heat Pump"),
        hot_water_source=HotWaterSource("Heat Battery / Electric Hot Water Tank"),
        secondary_heating=True,
        secondary_hot_water=True,
        integrated_control_sys=True)
```
