from .agilent_34970_ophyd import (
    Agilent_34970,
    v_range_dict,
    c_range_dict,
    r_range_dict,
    resolution_dict,
    temp_unit_dict,
)

from nomad_camels.main_classes import device_class


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="agilent_34970",
            virtual=False,
            ophyd_device=Agilent_34970,
            ophyd_class_name="Agilent_34970",
            non_channel_functions=[
                "deactivate_all_channels_units_1_3",
            ],
            **kwargs
        )


class subclass_config(device_class.Simple_Config):
    def __init__(
        self,
        parent=None,
        data="",
        settings_dict=None,
        config_dict=None,
        additional_info=None,
    ):
        comboboxes = {
            "measurement_type": [
                "Temperature",
                "DC Voltage",
                "AC Voltage",
                "DC Current",
                "AC Current",
                "Resistance",
                "4-Wire Resistance",
                "Frequency",
                "Period",
                "Digital",
                "Totalizer",
            ],
            "transducer_type": [
                "Thermocouple",
                "RTD",
                "Thermistor",
                "4-Wire RTD",
            ],
            "thermocouple_type": [
                "B",
                "E",
                "J",
                "K",
                "N",
                "R",
                "S",
                "T",
            ],
            "thermistor_type": ["2252", "5000", "10000"],
            "RTD_type": ["85", "91"],
            "temperature_unit": temp_unit_dict.keys(),
            "measurement_range": v_range_dict.keys(),
            "measurement_resolution": resolution_dict.keys(),
            "current_range": c_range_dict.keys(),
            "current_resolution": resolution_dict.keys(),
            "resistance_range": r_range_dict.keys(),
            "resistance_resolution": resolution_dict.keys(),
        }
        super().__init__(
            parent,
            "Agilent 34970",
            data,
            settings_dict,
            config_dict,
            additional_info,
            comboBoxes=comboboxes,
        )
        self.comboBox_connection_type.addItem("Local VISA")
        self.load_settings()
