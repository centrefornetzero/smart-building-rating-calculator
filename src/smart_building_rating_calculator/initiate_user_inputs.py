from src.smart_building_rating_calculator.inputs import (
    BatterySize,
    EVChargerPower,
    HeatingSource,
    HotWaterSource,
    SolarInverterSize,
    UserInputs,
)


def prep_user_inputs(
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
    """Checks datatypes and consistency of user inputs from questionnaire.

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
        UserInputs: user questionnaire results in structured format
    """
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
    if smart_ev_charger:
        assert charger_power != EVChargerPower.NONE
    if home_battery:
        assert battery_size != BatterySize.NONE
    if solar_pv:
        assert pv_inverter_size != SolarInverterSize.NONE

    return user_inputs
