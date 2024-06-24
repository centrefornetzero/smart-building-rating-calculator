from src.smart_building_rating_calculator.calculate_sbr_score import get_sbr_scores
from src.smart_building_rating_calculator.flex_archetype import FlexArchetype
from src.smart_building_rating_calculator.inputs import (
    BatterySize,
    EVChargerPower,
    HeatingSource,
    HotWaterSource,
    SolarInverterSize,
    UserInputs,
)
from src.smart_building_rating_calculator.intermediate_scoring import (
    calc_electrification_score,
    calc_ics_score,
    calc_smart_meter_score,
)


class TestScoreCalculators:
    def test_smartest_home(self):
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
        elec_scores = calc_electrification_score(user_inputs)
        smart_meter_score = calc_smart_meter_score(user_inputs)
        ics_score = calc_ics_score(user_inputs)
        elec_scores.insert(0, smart_meter_score)
        elec_scores.insert(len(elec_scores), ics_score)

        expected_scores = [1, 3, 3, 1, 3, -1, 4, 2, 1, 1, 1.5]
        for score, expected_val in zip(elec_scores, expected_scores):
            assert score == expected_val

        sbr_val, sbr, flex_archetype = get_sbr_scores(user_inputs)
        assert sbr_val == 25.5
        assert sbr == "A"
        assert flex_archetype == FlexArchetype.GOLD_FLEXER

    def test_sbr_b(self):
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

        elec_scores = calc_electrification_score(user_inputs)
        smart_meter_score = calc_smart_meter_score(user_inputs)
        ics_score = calc_ics_score(user_inputs)
        elec_scores.insert(0, smart_meter_score)
        elec_scores.insert(len(elec_scores), ics_score)

        expected_scores = [1, 3, 3, 0.5, 3, -1, 4, 0, 0, 0, 1.5]
        for score, expected_val in zip(elec_scores, expected_scores):
            assert score == expected_val

        sbr_val, sbr, flex_archetype = get_sbr_scores(user_inputs)
        assert sbr_val == 18.75
        assert sbr == "B"
        assert flex_archetype == FlexArchetype.GOLD_FLEXER

    def test_solar_ev_battery_hp(self):
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

        elec_scores = calc_electrification_score(user_inputs)
        smart_meter_score = calc_smart_meter_score(user_inputs)
        ics_score = calc_ics_score(user_inputs)
        elec_scores.insert(0, smart_meter_score)
        elec_scores.insert(len(elec_scores), ics_score)

        expected_scores = [1, 3, 0, 2, 2, -1, 3, 0, 1, 0, 1.5]
        for score, expected_val in zip(elec_scores, expected_scores):
            assert score == expected_val

        sbr_val, sbr, flex_archetype = get_sbr_scores(user_inputs)
        assert sbr_val == 15.0
        assert sbr == "C"
        assert flex_archetype == FlexArchetype.GOLD_FLEXER

    def test_solar_battery_hp(self):
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

        elec_scores = calc_electrification_score(user_inputs)
        smart_meter_score = calc_smart_meter_score(user_inputs)
        ics_score = calc_ics_score(user_inputs)
        elec_scores.insert(0, smart_meter_score)
        elec_scores.insert(len(elec_scores), ics_score)

        expected_scores = [1, 0, 0, 4, 2, -1, 1, 0, 1, 1, 1.5]
        for score, expected_val in zip(elec_scores, expected_scores):
            assert score == expected_val

        sbr_val, sbr, flex_archetype = get_sbr_scores(user_inputs)
        assert sbr_val == 12
        assert sbr == "C"
        assert flex_archetype == FlexArchetype.STRONG_FLEXER

    def hp_secondary_heating_hot_water(self):
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

        elec_scores = calc_electrification_score(user_inputs)
        smart_meter_score = calc_smart_meter_score(user_inputs)
        ics_score = calc_ics_score(user_inputs)
        elec_scores.insert(0, smart_meter_score)
        elec_scores.insert(len(elec_scores), ics_score)

        expected_scores = [1, 3, 0, 0, 1, 0, 1, 0, 0, 0, 1.5]
        for score, expected_val in zip(elec_scores, expected_scores):
            assert score == expected_val

        sbr_val, sbr, flex_archetype = get_sbr_scores(user_inputs)
        assert sbr_val == 7.5
        assert sbr == "D"
        assert flex_archetype == FlexArchetype.GOOD_FLEXER

    def test_smart_meter_only(self):
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

        elec_scores = calc_electrification_score(user_inputs)
        smart_meter_score = calc_smart_meter_score(user_inputs)
        ics_score = calc_ics_score(user_inputs)
        elec_scores.insert(0, smart_meter_score)
        elec_scores.insert(len(elec_scores), ics_score)

        expected_scores = [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1]
        for score, expected_val in zip(elec_scores, expected_scores):
            assert score == expected_val

        sbr_val, sbr, flex_archetype = get_sbr_scores(user_inputs)
        assert sbr_val == 1
        assert sbr == "G"
        assert flex_archetype == FlexArchetype.LOW_TECH_FLEXER

    def no_smart_meter(self):
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

        elec_scores = calc_electrification_score(user_inputs)
        smart_meter_score = calc_smart_meter_score(user_inputs)
        ics_score = calc_ics_score(user_inputs)
        elec_scores.insert(0, smart_meter_score)
        elec_scores.insert(len(elec_scores), ics_score)

        expected_scores = [0, 3, 3, 1, 3, -1, 4, 2, 1, 1, 1]
        for score, expected_val in zip(elec_scores, expected_scores):
            assert score == expected_val

        sbr_val, sbr, flex_archetype = get_sbr_scores(user_inputs)
        assert sbr_val == 1
        assert sbr == "G"
        assert flex_archetype == FlexArchetype.LOW_TECH_FLEXER


# Test all combinations of get_sbr_scores inputs
def test_all_combinations():
    for smart_meter in [True, False]:
        for smart_ev_charger in [True, False]:
            for charger_power in EVChargerPower:
                for smart_v2g_enabled in [True, False]:
                    for home_battery in [True, False]:
                        for battery_size in BatterySize:
                            for solar_pv in [True, False]:
                                for pv_inverter_size in SolarInverterSize:
                                    for electric_heating in [True, False]:
                                        for heating_source in HeatingSource:
                                            for hot_water_source in HotWaterSource:
                                                for secondary_heating in [True, False]:
                                                    for secondary_hot_water in [
                                                        True,
                                                        False,
                                                    ]:
                                                        for integrated_control_sys in [
                                                            True,
                                                            False,
                                                        ]:
                                                            if not smart_ev_charger:
                                                                charger_power = (
                                                                    EVChargerPower.NONE
                                                                )
                                                                smart_v2g_enabled = (
                                                                    False
                                                                )
                                                            if not home_battery:
                                                                battery_size = (
                                                                    BatterySize.NONE
                                                                )
                                                            if not solar_pv:
                                                                pv_inverter_size = (
                                                                    SolarInverterSize.NONE
                                                                )

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

                                                            elec_scores = calc_electrification_score(
                                                                user_inputs
                                                            )

                                                            for score in elec_scores:
                                                                assert isinstance(
                                                                    score, float
                                                                )

                                                            (
                                                                sbr_val,
                                                                sbr,
                                                                flex_archetype,
                                                            ) = get_sbr_scores(
                                                                user_inputs
                                                            )

                                                            assert isinstance(
                                                                sbr_val,
                                                                float,
                                                            )
                                                            assert isinstance(sbr, str)
                                                            assert isinstance(
                                                                flex_archetype,
                                                                str,
                                                            )
