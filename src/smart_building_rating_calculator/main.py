from src.smart_building_rating_calculator.inputs import (
    UserInputs,
    EVChargerPower,
    BatterySize,
    SolarInverterSize,
    HeatingSource,
    HotWaterSource,
)
from src.smart_building_rating_calculator.scoring import (
    calc_electrification_score,
    calc_ics_score,
)
from src.smart_building_rating_calculator.flex_archetype import calc_flex_archetype


def calc_sbr(sbr_val: float) -> str:
    if sbr_val >= 22:
        return "A"
    elif sbr_val >= 15:
        return "B"
    elif sbr_val >= 10:
        return "C"
    elif sbr_val >= 6:
        return "D"
    elif sbr_val >= 4:
        return "E"
    elif sbr_val >= 1:
        return "F"
    else:
        return "G"


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
):

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

    electrification_score = calc_electrification_score(user_inputs)

    smart_meter_score = int(user_inputs.smart_meter)
    ics_score = calc_ics_score(user_inputs)
    sbr_val = smart_meter_score * electrification_score * ics_score
    sbr = calc_sbr(sbr_val)

    flex_archetype = calc_flex_archetype(user_inputs, sbr_val)

    return sbr_val, sbr, flex_archetype
