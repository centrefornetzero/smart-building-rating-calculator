from src.smart_building_rating_calculator.inputs import (
    BatterySize,
    EVChargerPower,
    HeatingSource,
    HotWaterSource,
    SolarInverterSize,
    UserInputs,
)


def prep_user_inputs(
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

    assert isinstance(smart_meter, bool)
    assert isinstance(smart_ev_charger, bool)
    assert isinstance(charger_power, EVChargerPower)
    assert isinstance(smart_v2g_enabled, bool)
    assert isinstance(home_battery, bool)
    assert isinstance(battery_size, BatterySize)
    assert isinstance(solar_pv, bool)
    assert isinstance(pv_inverter_size, SolarInverterSize)
    assert isinstance(electric_heating, bool)
    assert isinstance(heating_source, HeatingSource)
    assert isinstance(hot_water_source, HotWaterSource)
    assert isinstance(secondary_heating, bool)
    assert isinstance(secondary_hot_water, bool)
    assert isinstance(integrated_control_sys, bool)

    if not smart_ev_charger:
        assert charger_power == EVChargerPower.NONE
    if not home_battery:
        assert battery_size == BatterySize.NONE
    if not solar_pv:
        assert pv_inverter_size == SolarInverterSize.NONE

    return user_inputs
