from dataclasses import replace
from typing import List

from src.smart_building_rating_calculator.inputs import (
    BatterySize,
    EVChargerPower,
    HeatingSource,
    HotWaterSource,
    SolarInverterSize,
    UserInputs,
)


def calc_smart_meter_score(user_inputs: UserInputs) -> float:
    """Smart meter score: based on whether or not the household has a smart meter

    Args:
        user_inputs (UserInputs): user questionnaire

    Returns:
        float: smart meter score
    """
    if user_inputs.smart_meter:
        return 1.0
    else:
        return 0.0


def calc_ev_score(user_inputs: UserInputs) -> float:
    """EV score: based on the power of the EV charger

    Args:
        user_inputs (UserInputs): user questionnaire

    Returns:
        float: EV score
    """
    if user_inputs.charger_power == EVChargerPower.CHARGER_3KW:
        return 2.5
    elif user_inputs.charger_power == EVChargerPower.CHARGER_7KW:
        return 3.0
    elif user_inputs.charger_power == EVChargerPower.CHARGER_22KW:
        return 4.0
    else:
        return 0.0


def calc_v2g_score(user_inputs: UserInputs) -> float:
    """V2G score: based on whether or not the household has a smart V2G enabled charger

    Args:
        user_inputs (UserInputs): user questionnaire

    Returns:
        float: V2G score
    """
    if user_inputs.smart_v2g_enabled:
        return 3.0
    else:
        return 0.0


def calc_home_battery_score(user_inputs: UserInputs) -> float:
    """Home battery score: based on whether or not the household has a home battery, the size of the home battery, and whether or not the household has a smart V2G enabled charger and/or a smart EV charger

    Args:
        user_inputs (UserInputs): user questionnaire

    Returns:
        float: home battery score
    """
    home_battery_score = user_inputs

    home_battery_score_1 = replace(
        home_battery_score,
        home_battery=True,
        battery_size=BatterySize.LARGE,
        smart_v2g_enabled=True,
    )
    home_battery_score_2 = replace(
        home_battery_score,
        home_battery=True,
        battery_size=BatterySize.LARGE,
        smart_v2g_enabled=False,
        smart_ev_charger=True,
    )

    home_battery_score_4 = replace(
        home_battery_score,
        home_battery=True,
        battery_size=BatterySize.LARGE,
        smart_v2g_enabled=False,
        smart_ev_charger=False,
    )

    home_battery_score_0_5 = replace(
        home_battery_score,
        home_battery=True,
        battery_size=BatterySize.STANDARD,
        smart_v2g_enabled=True,
    )

    home_battery_score_1_5 = replace(
        home_battery_score,
        home_battery=True,
        battery_size=BatterySize.STANDARD,
        smart_v2g_enabled=False,
        smart_ev_charger=True,
    )

    home_battery_score_3_5 = replace(
        home_battery_score,
        home_battery=True,
        battery_size=BatterySize.STANDARD,
        smart_v2g_enabled=False,
        smart_ev_charger=False,
    )

    if user_inputs == home_battery_score_1:
        return 1.0

    elif user_inputs == home_battery_score_2:
        return 2.0

    elif user_inputs == home_battery_score_4:
        return 4.0

    elif user_inputs == home_battery_score_0_5:
        return 0.5

    elif user_inputs == home_battery_score_1_5:
        return 1.5

    elif user_inputs == home_battery_score_3_5:
        return 3.5
    else:
        return 0.0


def calc_solar_pv_score(user_inputs: UserInputs) -> float:
    """Solar PV score: based on whether or not the household has solar PV, the size of the solar PV inverter, and whether or not the household has a smart V2G enabled charger and/or a home battery

    Args:
        user_inputs (UserInputs): user questionnaire

    Returns:
        float: solar PV score
    """
    solar_pv_score = user_inputs

    solar_pv_score_3_5 = replace(
        solar_pv_score,
        solar_pv=True,
        pv_inverter_size=SolarInverterSize.GT_4KW,
        smart_v2g_enabled=True,
    )

    solar_pv_score_2_5 = replace(
        solar_pv_score,
        solar_pv=True,
        pv_inverter_size=SolarInverterSize.GT_4KW,
        smart_v2g_enabled=False,
        home_battery=True,
    )

    solar_pv_score_1 = replace(
        solar_pv_score,
        solar_pv=True,
        pv_inverter_size=SolarInverterSize.GT_4KW,
        smart_v2g_enabled=False,
        home_battery=False,
    )

    solar_pv_score_3 = replace(
        solar_pv_score,
        solar_pv=True,
        pv_inverter_size=SolarInverterSize.LT_4KW,
        smart_v2g_enabled=True,
    )

    solar_pv_score_2 = replace(
        solar_pv_score,
        solar_pv=True,
        pv_inverter_size=SolarInverterSize.LT_4KW,
        smart_v2g_enabled=False,
        home_battery=True,
    )

    solar_pv_score_1_ = replace(
        solar_pv_score,
        solar_pv=True,
        pv_inverter_size=SolarInverterSize.LT_4KW,
        smart_v2g_enabled=False,
        home_battery=False,
    )

    if user_inputs == solar_pv_score_3_5:
        return 3.5
    elif user_inputs == solar_pv_score_2_5:
        return 2.5
    elif (user_inputs == solar_pv_score_1) or (user_inputs == solar_pv_score_1_):
        return 1.0
    elif user_inputs == solar_pv_score_3:
        return 3.0
    elif user_inputs == solar_pv_score_2:
        return 2.0
    else:
        return 0.0


def calc_elec_heating_score(user_inputs: UserInputs) -> float:
    """Electric heating score: based on the heating source

    Args:
        user_inputs (UserInputs): user questionnaire

    Returns:
        float: electric heating score
    """
    if user_inputs.heating_source in [
        HeatingSource.HEAT_PUMP,
        HeatingSource.ELEC_STORAGE_HEATER,
        HeatingSource.DIRECT_ELEC_HEAT,
    ] or user_inputs.hot_water_source in [
        HotWaterSource.HEAT_BATTERY_OR_ELEC_HOT_WATER_TANK,
        HotWaterSource.ELEC_SHOWER_BOILER_OR_OTHER,
    ]:
        return -1.0
    else:
        return 0.0


def calc_home_heating_score(user_inputs: UserInputs) -> float:
    """Home heating score: based on the heating source and whether or not the household has a smart V2G enabled charger and/or a home battery

    Args:
        user_inputs (UserInputs): user questionnaire

    Returns:
        float: home heating score
    """
    home_heating_score = user_inputs

    home_heating_score_4 = replace(
        home_heating_score,
        heating_source=HeatingSource.HEAT_PUMP,
        smart_v2g_enabled=True,
    )
    home_heating_score_3 = replace(
        home_heating_score,
        heating_source=HeatingSource.HEAT_PUMP,
        smart_v2g_enabled=False,
        home_battery=True,
    )
    home_heating_score_2 = replace(
        home_heating_score,
        heating_source=HeatingSource.HEAT_PUMP,
        smart_v2g_enabled=False,
        home_battery=False,
    )
    home_heating_score_3_ = replace(
        home_heating_score, heating_source=HeatingSource.ELEC_STORAGE_HEATER
    )
    home_heating_score_2_ = replace(
        home_heating_score,
        heating_source=HeatingSource.DIRECT_ELEC_HEAT,
        smart_v2g_enabled=True,
    )
    home_heating_score_2__ = replace(
        home_heating_score,
        heating_source=HeatingSource.DIRECT_ELEC_HEAT,
        home_battery=True,
    )
    home_heating_score_0 = replace(
        home_heating_score,
        heating_source=HeatingSource.DIRECT_ELEC_HEAT,
        smart_v2g_enabled=False,
        home_battery=False,
    )
    home_heating_score_1 = replace(
        home_heating_score, heating_source=HeatingSource.OTHER
    )

    if user_inputs == home_heating_score_4:
        return 4.0
    elif (user_inputs == home_heating_score_3) or (
        user_inputs == home_heating_score_3_
    ):
        return 3.0
    elif (
        (user_inputs == home_heating_score_2)
        or (user_inputs == home_heating_score_2_)
        or (user_inputs == home_heating_score_2__)
    ):
        return 2.0
    elif user_inputs == home_heating_score_0:
        return 0.0
    elif user_inputs == home_heating_score_1:
        return 1.0
    else:
        return 0.0


def calc_alternative_heating_score(user_inputs: UserInputs) -> float:
    """Alternative heating score: based on whether or not the household has an alternative heating source

    Args:
        user_inputs (UserInputs): user questionnaire

    Returns:
        float: alternative heating score
    """
    if (
        user_inputs.heating_source
        in [
            HeatingSource.HEAT_PUMP,
            HeatingSource.ELEC_STORAGE_HEATER,
            HeatingSource.DIRECT_ELEC_HEAT,
        ]
        and user_inputs.secondary_heating
    ):
        return 2.0
    elif (
        user_inputs.heating_source
        in [
            HeatingSource.HEAT_PUMP,
            HeatingSource.ELEC_STORAGE_HEATER,
            HeatingSource.DIRECT_ELEC_HEAT,
        ]
        and not user_inputs.secondary_heating
    ):
        return 0.0
    else:
        return 0.0


def calc_hot_water_heating_score(user_inputs: UserInputs) -> float:
    """Hot water heating score: based on the hot water source and whether or not the household has a smart V2G enabled charger and/or a home battery

    Args:
        user_inputs (UserInputs): user questionnaire

    Returns:
        float: hot water heating score
    """
    hot_water_heating_score = user_inputs

    hot_water_heating_score_1 = replace(
        hot_water_heating_score,
        hot_water_source=HotWaterSource.HEAT_BATTERY_OR_ELEC_HOT_WATER_TANK,
    )
    hot_water_heating_score_0 = replace(
        hot_water_heating_score,
        hot_water_source=HotWaterSource.ELEC_SHOWER_BOILER_OR_OTHER,
        smart_v2g_enabled=True,
    )
    hot_water_heating_score_0_ = replace(
        hot_water_heating_score,
        hot_water_source=HotWaterSource.ELEC_SHOWER_BOILER_OR_OTHER,
        home_battery=True,
    )
    hot_water_heating_score_neg1 = replace(
        hot_water_heating_score,
        hot_water_source=HotWaterSource.ELEC_SHOWER_BOILER_OR_OTHER,
        smart_v2g_enabled=False,
        home_battery=False,
    )

    if user_inputs == hot_water_heating_score_1:
        return 1.0
    elif (
        user_inputs == hot_water_heating_score_0
        or user_inputs == hot_water_heating_score_0_
    ):
        return 0.0
    elif user_inputs == hot_water_heating_score_neg1:
        return -1.0
    else:
        return 0.0


def calc_alternative_hot_water_score(user_inputs: UserInputs) -> float:
    """Alternative hot water score: based on whether or not the household has an alternative hot water source

    Args:
        user_inputs (UserInputs): user questionnaire

    Returns:
        float: alternative hot water score
    """
    if (
        user_inputs.hot_water_source
        in [
            HotWaterSource.HEAT_BATTERY_OR_ELEC_HOT_WATER_TANK,
            HotWaterSource.ELEC_SHOWER_BOILER_OR_OTHER,
        ]
        and user_inputs.secondary_hot_water
    ):
        return 1.0
    else:
        return 0.0


def calc_ics_score(user_inputs: UserInputs) -> float:
    """Integrated Control System (ICS) score: based on whether or not the household has an integrated control system

    Args:
        user_inputs (UserInputs): user questionnaire

    Returns:
        float: ICS score
    """
    if user_inputs.integrated_control_sys:
        return 1.5
    else:
        return 1.0


def calc_electrification_score(user_inputs: UserInputs) -> List[float]:
    """Calculates individual scoring for 'electrification measures' which feed into the SBR calculator

    Args:
        user_inputs (UserInputs): user questionnaire

    Returns:
        List[float]: list of scores for each electrification measure
    """
    ev_score = calc_ev_score(user_inputs)
    v2g_score = calc_v2g_score(user_inputs)
    home_battery_score = calc_home_battery_score(user_inputs)
    solar_pv_score = calc_solar_pv_score(user_inputs)
    elec_heating_score = calc_elec_heating_score(user_inputs)
    home_heating_score = calc_home_heating_score(user_inputs)
    alternative_heating_score = calc_alternative_heating_score(user_inputs)
    hot_water_heating_score = calc_hot_water_heating_score(user_inputs)
    alternative_hot_water_score = calc_alternative_hot_water_score(user_inputs)

    elec_scores = [
        ev_score,
        v2g_score,
        home_battery_score,
        solar_pv_score,
        elec_heating_score,
        home_heating_score,
        alternative_heating_score,
        hot_water_heating_score,
        alternative_hot_water_score,
    ]

    return elec_scores


def calc_sbr_score(
    user_inputs: UserInputs,
) -> float:
    """Calculate Smart Building Rating (SBR) numerical score
     Uses ESC's excel calculations.

    Args:
        user_inputs (UserInputs): user questionnaire

    Returns:
        float: SBR numerical score
    """
    electrification_score = calc_electrification_score(user_inputs)

    smart_meter_score = calc_smart_meter_score(user_inputs)
    ics_score = calc_ics_score(user_inputs)
    sbr_val = smart_meter_score * sum(electrification_score) * ics_score

    return float(sbr_val)
