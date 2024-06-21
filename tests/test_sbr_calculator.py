from src.smart_building_rating_calculator.flex_archetype import FlexArchetype
from src.smart_building_rating_calculator.inputs import (BatterySize,
                                                         EVChargerPower,
                                                         HeatingSource,
                                                         HotWaterSource,
                                                         SolarInverterSize)
from src.smart_building_rating_calculator.main import sbr_score


class TestSBRScore:
    def test_high_sbr_gold_flexer(self):
        sbr_val, sbr, flex_archetype = sbr_score(
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

        assert sbr_val == 25.5
        assert sbr == "A"
        assert flex_archetype == FlexArchetype.GOLD_FLEXER

    def test_medium_sbr_strong_flexer(self):
        sbr_val, sbr, flex_archetype = sbr_score(
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

        assert sbr_val == 12
        assert sbr == "C"
        assert flex_archetype == FlexArchetype.STRONG_FLEXER

    def test_low_sbr_untapped_flexer(self):
        sbr_val, sbr, flex_archetype = sbr_score(
            smart_meter=False,
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

        assert sbr_val == 0
        assert sbr == "G"
        assert flex_archetype == FlexArchetype.UNTAPPED_FLEXER

    def test_med_sbr_good_flexer(self):
        sbr_val, sbr, flex_archetype = sbr_score(
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

        assert sbr_val == 7.5
        assert sbr == "D"
        assert flex_archetype == FlexArchetype.GOOD_FLEXER

    def test_low_sbr_low_tech_flexer(self):
        sbr_val, sbr, flex_archetype = sbr_score(
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

        assert sbr_val == 1
        assert sbr == "G"
        assert flex_archetype == FlexArchetype.LOW_TECH_FLEXER


# test all combinations of sbr_score
