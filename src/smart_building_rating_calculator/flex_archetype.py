"""
Based on Andy's calcuations, this module calculates the flex archetype of a building based on the user inputs and the SBR value.
"""

from src.smart_building_rating_calculator.flexer_enums import FlexArchetype
from src.smart_building_rating_calculator.inputs import (
    HeatingSource,
    HotWaterSource,
    UserInputs,
)


def check_gold_flexer(user_inputs: UserInputs) -> bool:
    """Checks if household is classified as a Gold Standard Flexer.

    Args:
        user_inputs (UserInputs): user questionnaire

    Returns:
        bool: whether or not household satisfies Gold Standard Flexer requirements
    """
    gold_flexer = (
        user_inputs.smart_meter
        and user_inputs.smart_ev_charger
        and user_inputs.home_battery
        and (user_inputs.heating_source == HeatingSource.HEAT_PUMP)
        and user_inputs.solar_pv
        and user_inputs.integrated_control_sys
    )
    return gold_flexer


def check_strong_flexer(user_inputs: UserInputs) -> bool:
    """Checks if household is classified as a Strong Flexer.

    Args:
        user_inputs (UserInputs): user questionnaire

    Returns:
        bool: whether or not household satisfies Strong Flexer requirements
    """
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
    """Checks if household is classified as a Good Flexer.

    Args:
        user_inputs (UserInputs): user questionnaire
        sbr_val (float): numerical SBR value

    Returns:
        bool: whether or not household satisfies Good Flexer requirements
    """
    good_flexer = (
        user_inputs.smart_meter
        and (
            user_inputs.smart_ev_charger
            or user_inputs.home_battery
            or user_inputs.heating_source
            in [HeatingSource.HEAT_PUMP, HeatingSource.ELEC_STORAGE_HEATER]
            or user_inputs.hot_water_source
            == HotWaterSource.HEAT_BATTERY_OR_ELEC_HOT_WATER_TANK
            or user_inputs.solar_pv
        )
        and sbr_val > 4
    )
    return good_flexer


def check_untapped_flexer(user_inputs: UserInputs) -> bool:
    """Checks if household is classified as an Untapped Flexer.

    Args:
        user_inputs (UserInputs): user questionnaire

    Returns:
        bool: whether or not household satisfies Untapped Flexer requirements
    """
    untapped_flexer = (not user_inputs.smart_meter) and (
        user_inputs.smart_ev_charger
        or user_inputs.home_battery
        or (
            user_inputs.heating_source
            in [HeatingSource.HEAT_PUMP, HeatingSource.ELEC_STORAGE_HEATER]
        )
        or user_inputs.hot_water_source
        == HotWaterSource.HEAT_BATTERY_OR_ELEC_HOT_WATER_TANK
        or user_inputs.solar_pv
    )
    return untapped_flexer


def check_low_tech_flexer(user_inputs: UserInputs, sbr_val: float) -> bool:
    """Checks if household is classified as a Low-tech Flexer.

    Args:
        user_inputs (UserInputs): user questionnaire
        sbr_val (float): numerical SBR value

    Returns:
        bool: whether or not household satisfies Low-tech Flexer requirements
    """
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
            == HotWaterSource.HEAT_BATTERY_OR_ELEC_HOT_WATER_TANK
            or user_inputs.solar_pv
        )
        and sbr_val <= 4
    )

    return low_tech_flexer or low_tech_flexer_


def check_no_flexer(user_inputs: UserInputs) -> bool:
    """Checks if household is classified as a No Flexer.

    Args:
        user_inputs (UserInputs): user questionnaire

    Returns:
        bool: whether or not household satisfies No Flexer requirements
    """
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
    )
    return no_flexer


def calc_flex_archetype(user_inputs: UserInputs, sbr_val: float) -> str:
    """Calculates the Flex Archetype (FlexArchetype: `src/smart_building_rating_calculator/flexer_enums.py`)
    based on user inputs and SBR value.

    Args:
        user_inputs (UserInputs): user questionnaire
        sbr_val (float): numerical SBR value

    Raises:
        ValueError: if flexer type cannot be constructed based on user inputs, ValueError is raised

    Returns:
        str: FlexArchetype.value (e.g. "Gold Standard Flexer")
    """
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
        raise ValueError("Invalid user inputs")
