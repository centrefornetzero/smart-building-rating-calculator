from inputs import (
    UserInputs,
    EVChargerPower,
    BatterySize,
    SolarInverterSize,
    HeatingSource,
    HotWaterSource,
)


def calc_ev_score(user_inputs: UserInputs) -> float:
    if user_inputs.charger_power == EVChargerPower.CHARGER_3KW:
        return 2.5
    elif user_inputs.charger_power == EVChargerPower.CHARGER_7KW:
        return 3
    elif user_inputs.charger_power == EVChargerPower.CHARGER_22KW:
        return 4
    else:
        return 0


def calc_v2g_score(user_inputs: UserInputs) -> float:
    if user_inputs.smart_v2g_enabled:
        return 3
    else:
        return 0


def calc_home_battery_score(user_inputs: UserInputs) -> float:

    if (
        user_inputs.home_battery
        and user_inputs.battery_size == BatterySize.LARGE
        and user_inputs.smart_v2g_enabled
    ):
        return 1
    elif (
        user_inputs.home_battery
        and user_inputs.battery_size == BatterySize.LARGE
        and (not user_inputs.smart_v2g_enabled)
        and user_inputs.smart_ev_charger
    ):
        return 2
    elif (
        user_inputs.home_battery
        and user_inputs.battery_size == BatterySize.LARGE
        and (not user_inputs.smart_v2g_enabled)
        and (not user_inputs.smart_ev_charger)
    ):
        return 4
    elif (
        user_inputs.home_battery
        and user_inputs.battery_size == BatterySize.STANDARD
        and user_inputs.smart_v2g_enabled
    ):
        return 0.5
    elif (
        user_inputs.home_battery
        and user_inputs.battery_size == BatterySize.STANDARD
        and (not user_inputs.smart_v2g_enabled)
        and user_inputs.smart_ev_charger
    ):
        return 1.5
    elif (
        user_inputs.home_battery
        and user_inputs.battery_size == BatterySize.STANDARD
        and (not user_inputs.smart_v2g_enabled)
        and (not user_inputs.smart_ev_charger)
    ):
        return 3.5
    else:
        return 0


def calc_solar_pv_score(user_inputs: UserInputs) -> float:

    if (
        user_inputs.solar_pv
        and user_inputs.pv_inverter_size == SolarInverterSize.GT_4KW
        and user_inputs.smart_v2g_enabled
    ):
        return 3.5
    elif (
        user_inputs.solar_pv
        and user_inputs.pv_inverter_size == SolarInverterSize.GT_4KW
        and (not user_inputs.smart_v2g_enabled)
        and user_inputs.home_battery
    ):
        return 2.5
    elif (
        user_inputs.solar_pv
        and user_inputs.pv_inverter_size == SolarInverterSize.GT_4KW
        and (not user_inputs.smart_v2g_enabled)
        and (not user_inputs.home_battery)
    ):
        return 1
    elif (
        user_inputs.solar_pv
        and user_inputs.pv_inverter_size == SolarInverterSize.LT_4KW
        and user_inputs.smart_v2g_enabled
    ):
        return 3
    elif (
        user_inputs.solar_pv
        and user_inputs.pv_inverter_size == SolarInverterSize.LT_4KW
        and (not user_inputs.smart_v2g_enabled)
        and user_inputs.home_battery
    ):
        return 2
    elif (
        user_inputs.solar_pv
        and user_inputs.pv_inverter_size == SolarInverterSize.LT_4KW
        and (not user_inputs.smart_v2g_enabled)
        and (not user_inputs.home_battery)
    ):
        return 1
    else:
        return 0


def calc_elec_heating_score(user_inputs: UserInputs) -> float:
    if user_inputs.heating_source in [
        HeatingSource.HEAT_PUMP,
        HeatingSource.ELEC_STORAGE_HEATER,
        HeatingSource.DIRECT_ELEC_HEAT,
    ] or user_inputs.hot_water_source in [
        HotWaterSource.HEAT_BATTERY_OR_ELEC_HOT_WATER_TANK,
        HotWaterSource.ELEC_SHOWER_BOILER_OR_OTHER,
    ]:
        return -1
    else:
        return 0


def calc_home_heating_score(user_inputs: UserInputs) -> float:
    if (
        user_inputs.heating_source == HeatingSource.HEAT_PUMP
        and user_inputs.smart_v2g_enabled
    ):
        return 4
    elif (
        user_inputs.heating_source == HeatingSource.HEAT_PUMP
        and not user_inputs.smart_v2g_enabled
        and user_inputs.home_battery
    ):
        return 3
    elif (
        user_inputs.heating_source == HeatingSource.HEAT_PUMP
        and not user_inputs.smart_v2g_enabled
        and not user_inputs.home_battery
    ):
        return 2
    elif (
        user_inputs.heating_source != HeatingSource.HEAT_PUMP
        and user_inputs.heating_source == HeatingSource.ELEC_STORAGE_HEATER
    ):
        return 3

    elif (
        user_inputs.heating_source != HeatingSource.HEAT_PUMP
        and user_inputs.heating_source != HeatingSource.ELEC_STORAGE_HEATER
        and user_inputs.heating_source == HeatingSource.DIRECT_ELEC_HEAT
        and (user_inputs.smart_v2g_enabled or user_inputs.home_battery)
    ):
        return 2
    elif (
        user_inputs.heating_source != HeatingSource.HEAT_PUMP
        and user_inputs.heating_source != HeatingSource.ELEC_STORAGE_HEATER
        and user_inputs.heating_source == HeatingSource.DIRECT_ELEC_HEAT
        and not user_inputs.smart_v2g_enabled
        and not user_inputs.home_battery
    ):
        return 0
    elif (
        user_inputs.heating_source != HeatingSource.HEAT_PUMP
        and user_inputs.heating_source != HeatingSource.ELEC_STORAGE_HEATER
        and user_inputs.heating_source != HeatingSource.DIRECT_ELEC_HEAT
    ):
        return 1
    else:
        return 0


def calc_alternative_heating_score(user_inputs: UserInputs) -> float:
    if (
        user_inputs.heating_source
        in [
            HeatingSource.HEAT_PUMP,
            HeatingSource.ELEC_STORAGE_HEATER,
            HeatingSource.DIRECT_ELEC_HEAT,
        ]
        and user_inputs.secondary_heating
    ):
        return 2
    elif (
        user_inputs.heating_source
        in [
            HeatingSource.HEAT_PUMP,
            HeatingSource.ELEC_STORAGE_HEATER,
            HeatingSource.DIRECT_ELEC_HEAT,
        ]
        and not user_inputs.secondary_heating
    ):
        return 0
    else:
        return 0


def calc_hot_water_heating_score(user_inputs: UserInputs) -> float:
    if (
        user_inputs.hot_water_source
        == HotWaterSource.HEAT_BATTERY_OR_ELEC_HOT_WATER_TANK
    ):
        return 1
    elif (
        user_inputs.hot_water_source == HotWaterSource.ELEC_SHOWER_BOILER_OR_OTHER
        and (user_inputs.smart_v2g_enabled or user_inputs.home_battery)
    ):
        return 0
    elif (
        user_inputs.hot_water_source == HotWaterSource.ELEC_SHOWER_BOILER_OR_OTHER
        and not user_inputs.smart_v2g_enabled
        and not user_inputs.home_battery
    ):
        return -1
    else:
        return 0


def calc_alternative_hot_water_score(user_inputs: UserInputs) -> float:
    if (
        user_inputs.hot_water_source
        in [
            HotWaterSource.HEAT_BATTERY_OR_ELEC_HOT_WATER_TANK,
            HotWaterSource.ELEC_SHOWER_BOILER_OR_OTHER,
        ]
        and user_inputs.secondary_hot_water
    ):
        return 1
    else:
        return 0


def calc_ics_score(user_inputs: UserInputs) -> float:
    if user_inputs.integrated_control_sys:
        return 1.5
    else:
        return 1


def calc_electrification_score(user_inputs: UserInputs) -> float:

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
    print(elec_scores)
    return sum(elec_scores)
