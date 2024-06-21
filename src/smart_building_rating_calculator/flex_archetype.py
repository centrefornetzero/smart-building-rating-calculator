from enum import StrEnum

from src.smart_building_rating_calculator.inputs import (HeatingSource,
                                                         HotWaterSource,
                                                         UserInputs)


class FlexArchetype(StrEnum):
    NO_FLEXER = "No Flexer"
    LOW_TECH_FLEXER = "Low-tech Flexer"
    GOOD_FLEXER = "Good Flexer"
    UNTAPPED_FLEXER = "Untapped Flexer"
    STRONG_FLEXER = "Strong Flexer"
    GOLD_FLEXER = "Gold Standard Flexer"


def check_gold_flexer(user_inputs: UserInputs) -> bool:
    gold_flexer = (
        user_inputs.smart_meter
        and user_inputs.smart_ev_charger
        and user_inputs.home_battery
        and (user_inputs.heating_source == HeatingSource.HEAT_PUMP)
        and user_inputs.solar_pv
        and user_inputs.integrated_control_sys
    )
    return gold_flexer


def check_strong_flexer(user_inputs: UserInputs):
    strong_flexer = (
        user_inputs.smart_meter
        and (user_inputs.smart_ev_charger or user_inputs.home_battery)
        and (
            (
                user_inputs.heating_source
                in [HeatingSource.HEAT_PUMP, HeatingSource.ELEC_STORAGE_HEATER]
            )
            or user_inputs.hot_water_source
            == HotWaterSource.HEAT_BATTERY_OR_ELEC_HOT_WATER_TANK
        )
    )
    return strong_flexer


def check_good_flexer(user_inputs: UserInputs, sbr_val: float) -> bool:
    good_flexer = (
        user_inputs.smart_meter
        and (
            user_inputs.smart_ev_charger
            or user_inputs.home_battery
            or user_inputs.heating_source
            in [HeatingSource.HEAT_PUMP, HeatingSource.ELEC_STORAGE_HEATER]
            or user_inputs.hot_water_source
            == HotWaterSource.HEAT_BATTERY_OR_ELEC_HOT_WATER_TANK  # CA
            or user_inputs.solar_pv  # CA
        )
        and sbr_val > 4
    )
    return good_flexer


def check_untapped_flexer(user_inputs: UserInputs) -> bool:
    untapped_flexer = (not user_inputs.smart_meter) and (
        user_inputs.smart_ev_charger
        or user_inputs.home_battery
        or (
            user_inputs.heating_source
            in [HeatingSource.HEAT_PUMP, HeatingSource.ELEC_STORAGE_HEATER]
        )
        or user_inputs.hot_water_source
        == HotWaterSource.HEAT_BATTERY_OR_ELEC_HOT_WATER_TANK  # CA
        or user_inputs.solar_pv  # CA
    )
    return untapped_flexer


def check_low_tech_flexer(user_inputs: UserInputs, sbr_val: float) -> bool:
    low_tech_flexer = (
        user_inputs.smart_meter
        and (not user_inputs.smart_ev_charger)
        and (not user_inputs.home_battery)
        and (
            user_inputs.heating_source
            not in [HeatingSource.HEAT_PUMP, HeatingSource.ELEC_STORAGE_HEATER]
        )
        and (not user_inputs.solar_pv)
        # and (not user_inputs.integrated_control_sys)
    )
    low_tech_flexer_ = (
        user_inputs.smart_meter
        and (
            user_inputs.smart_ev_charger
            or user_inputs.home_battery
            or user_inputs.heating_source
            in [HeatingSource.HEAT_PUMP, HeatingSource.ELEC_STORAGE_HEATER]
            or user_inputs.hot_water_source
            == HotWaterSource.HEAT_BATTERY_OR_ELEC_HOT_WATER_TANK  # CA
            or user_inputs.solar_pv  # CA
        )
        and sbr_val <= 4
    )

    return low_tech_flexer or low_tech_flexer_


def check_no_flexer(user_inputs: UserInputs) -> bool:
    no_flexer = (
        (not user_inputs.smart_meter)
        and (not user_inputs.smart_ev_charger)
        and (not user_inputs.home_battery)
        and (
            user_inputs.heating_source
            not in [HeatingSource.HEAT_PUMP, HeatingSource.ELEC_STORAGE_HEATER]
        )
        and (
            user_inputs.hot_water_source
            != HotWaterSource.HEAT_BATTERY_OR_ELEC_HOT_WATER_TANK
        )
        and (not user_inputs.solar_pv)
        # and (not user_inputs.integrated_control_sys)
    )
    return no_flexer


def calc_flex_archetype(user_inputs: UserInputs, sbr_val: float) -> str:
    if check_gold_flexer(user_inputs):
        return FlexArchetype.GOLD_FLEXER.value

    elif check_strong_flexer(user_inputs):
        return FlexArchetype.STRONG_FLEXER.value

    elif check_good_flexer(user_inputs, sbr_val):
        return FlexArchetype.GOOD_FLEXER.value

    elif check_untapped_flexer(user_inputs):
        return FlexArchetype.UNTAPPED_FLEXER.value

    elif check_low_tech_flexer(user_inputs, sbr_val):
        return FlexArchetype.LOW_TECH_FLEXER.value

    elif check_no_flexer(user_inputs):
        return FlexArchetype.NO_FLEXER.value
    else:
        print(user_inputs)
        raise ValueError("Invalid user inputs")
