from typing import Tuple

import pandas as pd

from src.smart_building_rating_calculator.flex_archetype import \
    calc_flex_archetype
from src.smart_building_rating_calculator.inputs import (BatterySize,
                                                         EVChargerPower,
                                                         HeatingSource,
                                                         HotWaterSource,
                                                         SolarInverterSize,
                                                         UserInputs)
from src.smart_building_rating_calculator.scoring import (
    calc_electrification_score, calc_ics_score, calc_smart_meter_score)


def calc_sbr(sbr_val: float) -> str:
    rating = pd.cut(
        [sbr_val],
        bins=[-10, 1, 4, 6, 10, 15, 22, 100],
        right=True,
        labels=["G", "F", "E", "D", "C", "B", "A"],
    )
    return rating[0]


def calc_sbr_score(
    user_inputs: UserInputs,
) -> Tuple[float, str, str]:
    electrification_score = calc_electrification_score(user_inputs)

    smart_meter_score = calc_smart_meter_score(user_inputs)
    ics_score = calc_ics_score(user_inputs)
    sbr_val = smart_meter_score * sum(electrification_score) * ics_score
    sbr = calc_sbr(sbr_val)

    flex_archetype = calc_flex_archetype(user_inputs, sbr_val)

    return float(sbr_val), sbr, flex_archetype


def sbr_score(
    smart_meter: bool,
    smart_ev_charger: bool,
    charger_power: EVChargerPower,
    smart_v2g_enabled: bool,
    home_battery: bool,
    battery_size: BatterySize,
    solar_pv: bool,
    pv_inverter_size: SolarInverterSize,
    electric_heating: bool,
    heating_source: HeatingSource,
    hot_water_source: HotWaterSource,
    secondary_heating: bool,
    secondary_hot_water: bool,
    integrated_control_sys: bool,
) -> Tuple[float, str, str]:
    user_inputs = UserInputs(
        smart_meter,
        smart_ev_charger,
        charger_power,
        smart_v2g_enabled,
        home_battery,
        battery_size,
        solar_pv,
        pv_inverter_size,
        electric_heating,
        heating_source,
        hot_water_source,
        secondary_heating,
        secondary_hot_water,
        integrated_control_sys,
    )

    sbr_val, sbr, flex_archetype = calc_sbr_score(user_inputs)

    return sbr_val, sbr, flex_archetype
