"""Script tests different scenarios of user inputs, where expected results are taken from the SBR spreadsheet provided by ESC/
"""

import itertools

import pytest

from src.smart_building_rating_calculator.calculate_sbr_score import (
    get_sbr_scores,
    sbr_score,
)
from src.smart_building_rating_calculator.flex_archetype import FlexArchetype
from src.smart_building_rating_calculator.initiate_user_inputs import prep_user_inputs
from src.smart_building_rating_calculator.inputs import (
    BatterySize,
    EVChargerPower,
    HeatingSource,
    HotWaterSource,
    SolarInverterSize,
    UserInputs,
)
from src.smart_building_rating_calculator.intermediate_scoring import (
    calc_alternative_heating_score,
    calc_alternative_hot_water_score,
    calc_elec_heating_score,
    calc_ev_score,
    calc_home_battery_score,
    calc_home_heating_score,
    calc_hot_water_heating_score,
    calc_ics_score,
    calc_smart_meter_score,
    calc_solar_pv_score,
    calc_v2g_score,
)


@pytest.fixture(scope="module")
def test_smartest_home():
    user_inputs = UserInputs(
        smart_meter=True,
        smart_ev_charger=True,
        charger_power=EVChargerPower.CHARGER_7KW,
        smart_v2g_enabled=True,
        home_battery=True,
        battery_size=BatterySize.LARGE,
        solar_pv=True,
        pv_inverter_size=SolarInverterSize.LT_4KW,
        electric_heating=True,
        heating_source=HeatingSource.HEAT_PUMP,
        hot_water_source=HotWaterSource.HEAT_BATTERY_OR_ELEC_HOT_WATER_TANK,
        secondary_heating=True,
        secondary_hot_water=True,
        integrated_control_sys=True,
    )
    return user_inputs


@pytest.fixture(scope="module")
def test_sbr_b():
    user_inputs = UserInputs(
        smart_meter=True,
        smart_ev_charger=True,
        charger_power=EVChargerPower.CHARGER_7KW,
        smart_v2g_enabled=True,
        home_battery=True,
        battery_size=BatterySize.STANDARD,
        solar_pv=True,
        pv_inverter_size=SolarInverterSize.LT_4KW,
        electric_heating=True,
        heating_source=HeatingSource.HEAT_PUMP,
        hot_water_source=HotWaterSource.ELEC_SHOWER_BOILER_OR_OTHER,
        secondary_heating=False,
        secondary_hot_water=False,
        integrated_control_sys=True,
    )
    return user_inputs


@pytest.fixture(scope="module")
def test_solar_ev_battery_hp():
    user_inputs = UserInputs(
        smart_meter=True,
        smart_ev_charger=True,
        charger_power=EVChargerPower.CHARGER_7KW,
        smart_v2g_enabled=False,
        home_battery=True,
        battery_size=BatterySize.LARGE,
        solar_pv=True,
        pv_inverter_size=SolarInverterSize.LT_4KW,
        electric_heating=True,
        heating_source=HeatingSource.HEAT_PUMP,
        hot_water_source=HotWaterSource.HEAT_BATTERY_OR_ELEC_HOT_WATER_TANK,
        secondary_heating=False,
        secondary_hot_water=False,
        integrated_control_sys=True,
    )
    return user_inputs


@pytest.fixture(scope="module")
def test_solar_battery_power_diverter():
    user_inputs = UserInputs(
        smart_meter=True,
        smart_ev_charger=False,
        charger_power=EVChargerPower.NONE,
        smart_v2g_enabled=False,
        home_battery=True,
        battery_size=BatterySize.LARGE,
        solar_pv=True,
        pv_inverter_size=SolarInverterSize.LT_4KW,
        electric_heating=True,
        heating_source=HeatingSource.OTHER,
        hot_water_source=HotWaterSource.HEAT_BATTERY_OR_ELEC_HOT_WATER_TANK,
        secondary_heating=False,
        secondary_hot_water=True,
        integrated_control_sys=True,
    )
    return user_inputs


@pytest.fixture(scope="module")
def test_hp_secondary_heating_hot_water():
    user_inputs = UserInputs(
        smart_meter=True,
        smart_ev_charger=True,
        charger_power=EVChargerPower.CHARGER_7KW,
        smart_v2g_enabled=False,
        home_battery=False,
        battery_size=BatterySize.NONE,
        solar_pv=True,
        pv_inverter_size=SolarInverterSize.LT_4KW,
        electric_heating=False,
        heating_source=HeatingSource.OTHER,
        hot_water_source=HotWaterSource.OTHER,
        secondary_heating=False,
        secondary_hot_water=False,
        integrated_control_sys=True,
    )
    return user_inputs


@pytest.fixture(scope="module")
def test_solar_pv():
    user_inputs = UserInputs(
        smart_meter=True,
        smart_ev_charger=False,
        charger_power=EVChargerPower.NONE,
        smart_v2g_enabled=False,
        home_battery=False,
        battery_size=BatterySize.NONE,
        solar_pv=True,
        pv_inverter_size=SolarInverterSize.LT_4KW,
        electric_heating=False,
        heating_source=HeatingSource.OTHER,
        hot_water_source=HotWaterSource.OTHER,
        secondary_heating=False,
        secondary_hot_water=False,
        integrated_control_sys=True,
    )
    return user_inputs


@pytest.fixture(scope="module")
def test_smart_meter_only():
    user_inputs = UserInputs(
        smart_meter=True,
        smart_ev_charger=False,
        charger_power=EVChargerPower.NONE,
        smart_v2g_enabled=False,
        home_battery=False,
        battery_size=BatterySize.NONE,
        solar_pv=False,
        pv_inverter_size=SolarInverterSize.NONE,
        electric_heating=False,
        heating_source=HeatingSource.OTHER,
        hot_water_source=HotWaterSource.OTHER,
        secondary_heating=False,
        secondary_hot_water=False,
        integrated_control_sys=False,
    )
    return user_inputs


@pytest.fixture(scope="module")
def test_no_smart_meter():
    user_inputs = UserInputs(
        smart_meter=False,
        smart_ev_charger=True,
        charger_power=EVChargerPower.CHARGER_7KW,
        smart_v2g_enabled=True,
        home_battery=True,
        battery_size=BatterySize.LARGE,
        solar_pv=True,
        pv_inverter_size=SolarInverterSize.LT_4KW,
        electric_heating=True,
        heating_source=HeatingSource.HEAT_PUMP,
        hot_water_source=HotWaterSource.HEAT_BATTERY_OR_ELEC_HOT_WATER_TANK,
        secondary_heating=True,
        secondary_hot_water=True,
        integrated_control_sys=False,
    )
    return user_inputs


@pytest.mark.parametrize(
    "user_inputs, expected_smart_meter_score",
    [
        ("test_smartest_home", (1.0)),
        ("test_sbr_b", (1.0)),
        ("test_solar_ev_battery_hp", (1.0)),
        ("test_solar_battery_power_diverter", (1.0)),
        ("test_hp_secondary_heating_hot_water", (1.0)),
        ("test_solar_pv", (1.0)),
        ("test_smart_meter_only", (1.0)),
        ("test_no_smart_meter", (0.0)),
    ],
)
def test_smart_meter_score_calculator(user_inputs, expected_smart_meter_score, request):
    user_inputs = request.getfixturevalue(user_inputs)
    smart_meter_score = calc_smart_meter_score(user_inputs)
    assert smart_meter_score == expected_smart_meter_score


@pytest.mark.parametrize(
    "user_inputs, expected_ev_score",
    [
        ("test_smartest_home", (3.0)),
        ("test_sbr_b", (3.0)),
        ("test_solar_ev_battery_hp", (3.0)),
        ("test_solar_battery_power_diverter", (0.0)),
        ("test_hp_secondary_heating_hot_water", (3.0)),
        ("test_solar_pv", (0.0)),
        ("test_smart_meter_only", (0.0)),
        ("test_no_smart_meter", (3.0)),
    ],
)
def test_ev_score_calculator(user_inputs, expected_ev_score, request):
    user_inputs = request.getfixturevalue(user_inputs)
    ev_score = calc_ev_score(user_inputs)
    assert ev_score == expected_ev_score


@pytest.mark.parametrize(
    "user_inputs, expected_v2g_score",
    [
        ("test_smartest_home", (3.0)),
        ("test_sbr_b", (3.0)),
        ("test_solar_ev_battery_hp", (0.0)),
        ("test_solar_battery_power_diverter", (0.0)),
        ("test_hp_secondary_heating_hot_water", (0.0)),
        ("test_solar_pv", (0.0)),
        ("test_smart_meter_only", (0.0)),
        ("test_no_smart_meter", (3.0)),
    ],
)
def test_v2g_score_calculator(user_inputs, expected_v2g_score, request):
    user_inputs = request.getfixturevalue(user_inputs)
    v2g_score = calc_v2g_score(user_inputs)
    assert v2g_score == expected_v2g_score


@pytest.mark.parametrize(
    "user_inputs, expected_home_battery_score",
    [
        ("test_smartest_home", (1.0)),
        ("test_sbr_b", (0.5)),
        ("test_solar_ev_battery_hp", (2.0)),
        ("test_solar_battery_power_diverter", (4.0)),
        ("test_hp_secondary_heating_hot_water", (0.0)),
        ("test_solar_pv", (0.0)),
        ("test_smart_meter_only", (0.0)),
        ("test_no_smart_meter", (1.0)),
    ],
)
def test_home_battery_calculator(user_inputs, expected_home_battery_score, request):
    user_inputs = request.getfixturevalue(user_inputs)
    home_battery_score = calc_home_battery_score(user_inputs)
    assert home_battery_score == expected_home_battery_score


@pytest.mark.parametrize(
    "user_inputs, expected_solar_pv_score",
    [
        ("test_smartest_home", (3.0)),
        ("test_sbr_b", (3.0)),
        ("test_solar_ev_battery_hp", (2.0)),
        ("test_solar_battery_power_diverter", (2.0)),
        ("test_hp_secondary_heating_hot_water", (1.0)),
        ("test_solar_pv", (1.0)),
        ("test_smart_meter_only", (0.0)),
        ("test_no_smart_meter", (3.0)),
    ],
)
def test_solar_pv_score_calculator(user_inputs, expected_solar_pv_score, request):
    user_inputs = request.getfixturevalue(user_inputs)
    solar_pv_score = calc_solar_pv_score(user_inputs)
    assert solar_pv_score == expected_solar_pv_score


@pytest.mark.parametrize(
    "user_inputs, expected_elec_heating_score",
    [
        ("test_smartest_home", (-1.0)),
        ("test_sbr_b", (-1.0)),
        ("test_solar_ev_battery_hp", (-1.0)),
        ("test_solar_battery_power_diverter", (-1.0)),
        ("test_hp_secondary_heating_hot_water", (0.0)),
        ("test_solar_pv", (0.0)),
        ("test_smart_meter_only", (0.0)),
        ("test_no_smart_meter", (-1.0)),
    ],
)
def test_elec_heating_score_calculator(
    user_inputs, expected_elec_heating_score, request
):
    user_inputs = request.getfixturevalue(user_inputs)
    elec_heating_score = calc_elec_heating_score(user_inputs)
    assert elec_heating_score == expected_elec_heating_score


@pytest.mark.parametrize(
    "user_inputs, expected_home_heating_score",
    [
        ("test_smartest_home", (4.0)),
        ("test_sbr_b", (4.0)),
        ("test_solar_ev_battery_hp", (3.0)),
        ("test_solar_battery_power_diverter", (1.0)),
        ("test_hp_secondary_heating_hot_water", (1.0)),
        ("test_solar_pv", (1.0)),
        ("test_smart_meter_only", (1.0)),
        ("test_no_smart_meter", (4.0)),
    ],
)
def test_home_heating_score_calculator(
    user_inputs, expected_home_heating_score, request
):
    user_inputs = request.getfixturevalue(user_inputs)
    home_heating_score = calc_home_heating_score(user_inputs)
    assert home_heating_score == expected_home_heating_score


@pytest.mark.parametrize(
    "user_inputs, expected_alternative_heating_score",
    [
        ("test_smartest_home", (2.0)),
        ("test_sbr_b", (0.0)),
        ("test_solar_ev_battery_hp", (0.0)),
        ("test_solar_battery_power_diverter", (0.0)),
        ("test_hp_secondary_heating_hot_water", (0.0)),
        ("test_solar_pv", (0.0)),
        ("test_smart_meter_only", (0.0)),
        ("test_no_smart_meter", (2.0)),
    ],
)
def test_alternative_heating_score_calculator(
    user_inputs, expected_alternative_heating_score, request
):
    user_inputs = request.getfixturevalue(user_inputs)
    alternative_heating_score = calc_alternative_heating_score(user_inputs)
    assert alternative_heating_score == expected_alternative_heating_score


@pytest.mark.parametrize(
    "user_inputs, expected_hot_water_heating_score",
    [
        ("test_smartest_home", (1.0)),
        ("test_sbr_b", (0.0)),
        ("test_solar_ev_battery_hp", (1.0)),
        ("test_solar_battery_power_diverter", (1.0)),
        ("test_hp_secondary_heating_hot_water", (0.0)),
        ("test_solar_pv", (0.0)),
        ("test_smart_meter_only", (0.0)),
        ("test_no_smart_meter", (1.0)),
    ],
)
def test_alternative_hot_water_heating_score_calculator(
    user_inputs, expected_hot_water_heating_score, request
):
    user_inputs = request.getfixturevalue(user_inputs)
    hot_water_heating_score = calc_hot_water_heating_score(user_inputs)
    assert hot_water_heating_score == expected_hot_water_heating_score


@pytest.mark.parametrize(
    "user_inputs, expected_alternative_hot_water_score",
    [
        ("test_smartest_home", (1.0)),
        ("test_sbr_b", (0.0)),
        ("test_solar_ev_battery_hp", (0.0)),
        ("test_solar_battery_power_diverter", (1.0)),
        ("test_hp_secondary_heating_hot_water", (0.0)),
        ("test_solar_pv", (0.0)),
        ("test_smart_meter_only", (0.0)),
        ("test_no_smart_meter", (1.0)),
    ],
)
def test_alternative_hot_water_score_calculator(
    user_inputs, expected_alternative_hot_water_score, request
):
    user_inputs = request.getfixturevalue(user_inputs)
    alternative_hot_water_score = calc_alternative_hot_water_score(user_inputs)
    assert alternative_hot_water_score == expected_alternative_hot_water_score


@pytest.mark.parametrize(
    "user_inputs, expected_ics_score",
    [
        ("test_smartest_home", (1.5)),
        ("test_sbr_b", (1.5)),
        ("test_solar_ev_battery_hp", (1.5)),
        ("test_solar_battery_power_diverter", (1.5)),
        ("test_hp_secondary_heating_hot_water", (1.5)),
        ("test_solar_pv", (1.5)),
        ("test_smart_meter_only", (1.0)),
        ("test_no_smart_meter", (1.0)),
    ],
)
def test_ics_score_calculator(user_inputs, expected_ics_score, request):
    user_inputs = request.getfixturevalue(user_inputs)
    ics_score = calc_ics_score(user_inputs)
    assert ics_score == expected_ics_score


@pytest.mark.parametrize(
    "user_inputs, expected_sbr_score",
    [
        ("test_smartest_home", (25.5)),
        ("test_sbr_b", (18.75)),
        ("test_solar_ev_battery_hp", (15.0)),
        ("test_solar_battery_power_diverter", (12.0)),
        ("test_hp_secondary_heating_hot_water", (7.5)),
        ("test_smart_meter_only", (1.0)),
        ("test_no_smart_meter", (0.0)),
    ],
)
def test_sbr_score_calculator(user_inputs, expected_sbr_score, request):
    user_inputs = request.getfixturevalue(user_inputs)
    sbr_val, _, _ = get_sbr_scores(user_inputs)
    assert sbr_val == expected_sbr_score


@pytest.mark.parametrize(
    "user_inputs, expected_sbr",
    [
        ("test_smartest_home", ("A")),
        ("test_sbr_b", ("B")),
        ("test_solar_ev_battery_hp", ("C")),
        ("test_solar_battery_power_diverter", ("C")),
        ("test_hp_secondary_heating_hot_water", ("D")),
        ("test_smart_meter_only", ("G")),
        ("test_no_smart_meter", ("G")),
    ],
)
def test_sbr_calculator(user_inputs, expected_sbr, request):
    user_inputs = request.getfixturevalue(user_inputs)
    _, sbr, _ = get_sbr_scores(user_inputs)
    assert sbr == expected_sbr


@pytest.mark.parametrize(
    "user_inputs, expected_archetype",
    [
        ("test_smartest_home", (FlexArchetype.GOLD_FLEXER)),
        ("test_sbr_b", (FlexArchetype.GOLD_FLEXER)),
        ("test_solar_ev_battery_hp", (FlexArchetype.GOLD_FLEXER)),
        ("test_solar_battery_power_diverter", (FlexArchetype.STRONG_FLEXER)),
        ("test_hp_secondary_heating_hot_water", (FlexArchetype.GOOD_FLEXER)),
        ("test_smart_meter_only", (FlexArchetype.LOW_TECH_FLEXER)),
        ("test_no_smart_meter", (FlexArchetype.UNTAPPED_FLEXER)),
    ],
)
def test_archetype_calculator(user_inputs, expected_archetype, request):
    user_inputs = request.getfixturevalue(user_inputs)
    _, _, archetype = get_sbr_scores(user_inputs)
    assert archetype == expected_archetype


class TestAllCombination:
    input_combinations = itertools.product(
        [True, False],  # smart_meter
        [True, False],  # smart_ev_charger
        EVChargerPower.__members__.values(),
        [True, False],  # smart_v2g_enabled
        [True, False],  # home_battery
        BatterySize.__members__.values(),
        [True, False],  # solar_pv
        SolarInverterSize.__members__.values(),
        [True, False],  # electric_heating
        HeatingSource.__members__.values(),
        HotWaterSource.__members__.values(),
        [True, False],  # secondary_heating
        [True, False],  # secondary_hot_water
        [True, False],  # integrated_control_sys
    )
    error_input_combinations = [
        inputs
        for inputs in input_combinations
        if (
            (inputs[1] and inputs[2] == EVChargerPower.NONE)
            or (inputs[4] and inputs[5] == BatterySize.NONE)
            or (inputs[6] and inputs[7] == SolarInverterSize.NONE)
            or (not inputs[1] and inputs[2] != EVChargerPower.NONE)
            or (not inputs[4] and inputs[5] != BatterySize.NONE)
            or (not inputs[6] and inputs[7] != SolarInverterSize.NONE)
        )
    ]

    @pytest.mark.xfail(raises=AssertionError)
    def test_raises_exceptions_for_bad_inputs(self):
        for inputs in self.error_input_combinations:
            prep_user_inputs(*inputs)

    def test_assert_expected_types(self):
        valid_input_combinations = [
            inputs
            for inputs in self.input_combinations
            if input not in self.error_input_combinations
        ]

        for inputs in valid_input_combinations:
            user_inputs = UserInputs(*inputs)

            ev_score = calc_ev_score(user_inputs)
            v2g_score = calc_v2g_score(user_inputs)
            home_battery_score = calc_home_battery_score(user_inputs)
            solar_pv_score = calc_solar_pv_score(user_inputs)
            elec_heating_score = calc_elec_heating_score(user_inputs)
            home_heating_score = calc_home_heating_score(user_inputs)
            alternative_heating_score = calc_alternative_heating_score(user_inputs)
            hot_water_heating_score = calc_hot_water_heating_score(user_inputs)
            alternative_hot_water_score = calc_alternative_hot_water_score(user_inputs)

            assert isinstance(ev_score, float)
            assert isinstance(v2g_score, float)
            assert isinstance(home_battery_score, float)
            assert isinstance(solar_pv_score, float)
            assert isinstance(elec_heating_score, float)
            assert isinstance(home_heating_score, float)
            assert isinstance(alternative_heating_score, float)
            assert isinstance(hot_water_heating_score, float)
            assert isinstance(alternative_hot_water_score, float)

            sbr_normalised, sbr, flex_archetype = sbr_score(*inputs)

            assert isinstance(sbr_normalised, float)
            assert isinstance(sbr, str)
            assert isinstance(flex_archetype, str)

    def test_assert_sbr_range(self):
        valid_input_combinations = [
            inputs
            for inputs in self.input_combinations
            if input not in self.error_input_combinations
        ]

        for inputs in valid_input_combinations:
            sbr_normalised, sbr, flex_archetype = sbr_score(*inputs)

            assert sbr_normalised >= 0.0 and sbr_normalised <= 100.0
            assert sbr in ["A", "B", "C", "D", "E", "F", "G"]
            assert flex_archetype in FlexArchetype._value2member_map_.keys()
