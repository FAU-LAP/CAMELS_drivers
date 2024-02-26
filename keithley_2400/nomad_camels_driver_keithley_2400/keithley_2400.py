from .keithley_2400_ophyd import Keithley_2400

from nomad_camels.main_classes import device_class


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="keithley_2400",
            virtual=False,
            tags=["SMU", "Voltage", "Current"],
            directory="keithley_2400",
            ophyd_device=Keithley_2400,
            ophyd_class_name="Keithley_2400",
            **kwargs
        )
        self.config["current_compliance"] = 0.1
        self.config["voltage_compliance"] = 20
        self.config["voltage_range_source"] = 20
        self.config["current_range_source"] = 0.1
        self.config["voltage_range_sense"] = 20
        self.config["current_range_sense"] = 0.1


class subclass_config(device_class.Simple_Config):
    def __init__(
        self,
        parent=None,
        data="",
        settings_dict=None,
        config_dict=None,
        additional_info=None,
    ):
        labels = {
            "current_compliance": "Current Compliance (A)",
            "voltage_compliance": "Voltage Compliance (V)",
            "voltage_range_source": "Voltage source range (V)",
            "current_range_source": "Current source range (A)",
            "voltage_range_sense": "Voltage sensing range (V)",
            "current_range_sense": "Current sensing range (A)",
        }
        super().__init__(
            parent,
            "keithley_2400",
            data,
            settings_dict,
            config_dict,
            additional_info,
            labels=labels,
        )
        self.comboBox_connection_type.addItem("Local VISA")
        self.load_settings()
