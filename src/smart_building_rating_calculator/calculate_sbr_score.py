from typing import Tuple

import pandas as pd
from src.smart_building_rating_calculator.initiate_user_inputs import prep_user_inputs
from src.smart_building_rating_calculator.flex_archetype import calc_flex_archetype
from src.smart_building_rating_calculator.intermediate_scoring import calc_sbr_score
from src.smart_building_rating_calculator.inputs import UserInputs


def calc_sbr(sbr_val: float) -> str:
    rating = pd.cut(
        [sbr_val],
        bins=[-10, 1, 4, 6, 10, 15, 22, 100],
        right=True,
        labels=["G", "F", "E", "D", "C", "B", "A"],
    )
    return rating[0]


def get_sbr_scores(user_inputs: UserInputs) -> Tuple[float, str, str]:
    sbr_val = calc_sbr_score(user_inputs)
    sbr = calc_sbr(sbr_val)
    flex_archetype = calc_flex_archetype(user_inputs, sbr_val)

    return sbr_val, sbr, flex_archetype


def sbr_score(
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
) -> Tuple[float, str, str]:
    user_inputs = prep_user_inputs(
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
    sbr_val, sbr, flex_archetype = get_sbr_scores(user_inputs)
    return sbr_val, sbr, flex_archetype
