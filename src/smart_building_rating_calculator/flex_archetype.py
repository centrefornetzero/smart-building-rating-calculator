from src.smart_building_rating_calculator.inputs import (
    UserInputs,
    HeatingSource,
    HotWaterSource,
)
from enum import StrEnum


class FlexArchetypes(StrEnum):
    NO_FLEXER = "No Flexer"
    LOW_TECH_FLEXER = "Low-tech Flexer"
    GOOD_FLEXER = "Good Flexer"
    UNTAPPED_FLEXER = "Untapped Flexer"
    STRONG_FLEXER = "Strong Flexer"
    GOLD_FLEXER = "Gold Standard Flexer"


def calc_flex_archetype(user_inputs: UserInputs, sbr_val: float) -> FlexArchetypes:

    if (
        user_inputs.smart_meter
        and user_inputs.smart_ev_charger
        and user_inputs.home_battery
        and user_inputs.heating_source == HeatingSource.HEAT_PUMP
        and user_inputs.solar_pv
        and user_inputs.integrated_control_sys
    ):
        return FlexArchetypes.GOLD_FLEXER.value

    elif user_inputs.smart_meter and (
        user_inputs.smart_ev_charger
        or user_inputs.home_battery
        or user_inputs.heating_source
        in [HeatingSource.HEAT_PUMP, HeatingSource.ELEC_STORAGE_HEATER]
        or user_inputs.hot_water_source
        == HotWaterSource.HEAT_BATTERY_OR_ELEC_HOT_WATER_TANK
    ):
        return FlexArchetypes.STRONG_FLEXER.value

    elif not user_inputs.smart_meter and (
        user_inputs.smart_ev_charger
        or user_inputs.home_battery
        or user_inputs.heating_source
        in [HeatingSource.HEAT_PUMP, HeatingSource.ELEC_STORAGE_HEATER]
    ):
        return FlexArchetypes.UNTAPPED_FLEXER.value

    elif (
        user_inputs.smart_meter
        and (
            user_inputs.smart_ev_charger
            or user_inputs.home_battery
            or user_inputs.heating_source
            in [HeatingSource.HEAT_PUMP, HeatingSource.ELEC_STORAGE_HEATER]
        )
        and sbr_val > 4
    ):
        return FlexArchetypes.GOOD_FLEXER.value

    elif (
        user_inputs.smart_meter
        and not user_inputs.smart_ev_charger
        and not user_inputs.home_battery
        and user_inputs.heating_source
        not in [HeatingSource.HEAT_PUMP, HeatingSource.ELEC_STORAGE_HEATER]
        and not user_inputs.solar_pv
        and not user_inputs.integrated_control_sys
    ):
        return FlexArchetypes.LOW_TECH_FLEXER.value

    elif (
        not user_inputs.smart_meter
        and not user_inputs.smart_ev_charger
        and not user_inputs.home_battery
        and (
            user_inputs.heating_source
            not in [HeatingSource.HEAT_PUMP, HeatingSource.ELEC_STORAGE_HEATER]
        )
        and (
            user_inputs.hot_water_source
            != HotWaterSource.HEAT_BATTERY_OR_ELEC_HOT_WATER_TANK
        )
        and not user_inputs.solar_pv
        and not user_inputs.integrated_control_sys
    ):
        return FlexArchetypes.NO_FLEXER.value
