"""
Valid answers to user questionnaire - inputs into the SBR calculator
"""

from dataclasses import dataclass
from enum import StrEnum


class HeatingSource(StrEnum):
    HEAT_PUMP = "Heat Pump"
    ELEC_STORAGE_HEATER = "Electric Storage Heater / Heat Battery"
    DIRECT_ELEC_HEAT = "Direct Electric Heat"
    OTHER = "Other"


class HotWaterSource(StrEnum):
    HEAT_BATTERY_OR_ELEC_HOT_WATER_TANK = "Heat Battery / Electric Hot Water Tank"
    ELEC_SHOWER_BOILER_OR_OTHER = (
        "Electric Shower / Electric Boiler / Other Electric Hot Water System"
    )
    OTHER = "Other"


class EVChargerPower(StrEnum):
    CHARGER_3KW = "3 kW"
    CHARGER_7KW = "7 kW"
    CHARGER_22KW = "22 kW"
    NONE = "None"


class BatterySize(StrEnum):
    STANDARD = "Smaller than 8kWh"
    LARGE = "8kWh or greater"
    NONE = "None"


class SolarInverterSize(StrEnum):
    LT_4KW = "4 kW or less"
    GT_4KW = "Greater than 4 kW"
    NONE = "None"


@dataclass
class UserInputs:
    smart_meter: bool
    smart_ev_charger: bool
    charger_power: EVChargerPower
    smart_v2g_enabled: bool
    home_battery: bool
    battery_size: BatterySize
    solar_pv: bool
    pv_inverter_size: SolarInverterSize
    electric_heating: bool
    heating_source: HeatingSource
    hot_water_source: HotWaterSource
    secondary_heating: bool
    secondary_hot_water: bool
    integrated_control_sys: bool
