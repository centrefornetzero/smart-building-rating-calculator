# Smart building rating calculator
This package allows users to calculate Smart Building Ratings (SBR) and their associated SBR 'archetype'. In brief, the smart building rating is a metric that measures a building’s potential to flex its energy demand.  More information on the concept and methodology used to compute the SBR can be found on our [website](https://www.centrefornetzero.org/impact/smart-building-rating).

## Installation

To install this package, run

```
pip install smart-building-rating-calculator
```

## Performing the SBR calculation

The main SBR calculation is done with the [`sbr_score`](src/smart_building_rating_calculator/calculate_sbr_score.py) function which takes in user inputs, and outputs:
1) SBR value (between 0 and 100)
2) SBR rating (A-G)
3) Flex Archetype (see [`flexer_enums.py`](`src/smart_building_rating_calculator/flexer_enums.py`)).

Inputs must have datatypes as defined in [`inputs.py`](src/smart_building_rating_calculator/inputs.py`)
- Most inputs are `bool` type (`True`/`False`)
- Others are `StrEnum` type e.g., `charger_power` must have a value of `EVChargerPower("3 kW")`, `EVChargerPower("7 kW")`, `EVChargerPower("22 kW")`, or `EVChargerPower("None")`
- Upon calling `sbr_score`, correct input datatypes are automatically checked. An error is raised if input datatypes are incorrect.

Here's an example of how to compute the SBR for a given set of inputs, using the `sbr_score` function.

```python
from smart_building_rating_calculator.calculate_sbr_score import sbr_score
from smart_building_rating_calculator.inputs import (
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
