from typing import Tuple

import pandas as pd

from src.smart_building_rating_calculator.flex_archetype import calc_flex_archetype
from src.smart_building_rating_calculator.initiate_user_inputs import prep_user_inputs
from src.smart_building_rating_calculator.inputs import (
    BatterySize,
    EVChargerPower,
    HeatingSource,
    HotWaterSource,
    SolarInverterSize,
    UserInputs,
)
from src.smart_building_rating_calculator.intermediate_scoring import calc_sbr_score


def calc_sbr(sbr_val: float) -> str:
    """Calculate SBR rating (A-G) based on SBR value

    Args:
        sbr_val (float): SBR value

    Returns:
        str: SBR rating
    """
    rating = pd.cut(
        [sbr_val],
        bins=[-10, 1, 4, 6, 10, 15, 22, 100],
        right=True,
        labels=["G", "F", "E", "D", "C", "B", "A"],
    )
    return rating[0]


def get_sbr_scores(user_inputs: UserInputs) -> Tuple[float, str, str]:
    """Get key SBR scores

    Args:
        user_inputs (UserInputs): user questionnaire

    Returns:
        Tuple[float, str, str]: SBR value, SBR rating, Flex Archetype
    """
    sbr_val = calc_sbr_score(user_inputs)
    sbr = calc_sbr(sbr_val)
    flex_archetype = calc_flex_archetype(user_inputs, sbr_val)

    return sbr_val, sbr, flex_archetype


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
    """Main SBR calcuation function. Takes in user inputs and returns:
        1) Normalised SBR value (between 0 and 100)
        2) SBR rating (A-G)
        3) Flex Archetype (see `src/smart_building_rating_calculator/flexer_enums.py`).

    Args:
        smart_meter (bool): do they have a smart meter?
        smart_ev_charger (bool): do they have a smart EV charger?
        charger_power (EVChargerPower): what is the power of the EV charger?
        smart_v2g_enabled (bool): is the smart charger V2G enabled?
        home_battery (bool): do they have a home battery?
        battery_size (BatterySize): what size is the home battery?
        solar_pv (bool): do they have solar PV?
        pv_inverter_size (SolarInverterSize): what size is the solar PV inverter?
        electric_heating (bool): do they have electric heating?
        heating_source (HeatingSource): what is the heating source?
        hot_water_source (HotWaterSource): what is the hot water source?
        secondary_heating (bool): do they have secondary heating?
        secondary_hot_water (bool): do they have secondary hot water?
        integrated_control_sys (bool): do they have an integrated control system?

    Returns:
        Tuple[float, str, str]: SBR numerical value (out of 100), SBR rating (A-G), and Flex Archetype (e.g. "Untapped Flexer")
    """
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

    # Normalise score between 0 & 100
    min_sbr = -3.0
    max_sbr = 27.75
    sbr_normalised = 100 * (sbr_val - min_sbr) / (max_sbr - min_sbr)

    return sbr_normalised, sbr, flex_archetype
