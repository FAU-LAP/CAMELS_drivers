from .keithley_197a_ophyd import Keithley_197A

from nomad_camels.main_classes import device_class


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="keithley_197a",
            virtual=False,
            tags=["DMM", "voltage", "current"],
            directory="keithley_197a",
            ophyd_device=Keithley_197A,
            ophyd_class_name="Keithley_197A",
            **kwargs,
        )
        self.config["measure_range"] = ["Auto"]


class subclass_config(device_class.Simple_Config):
    def __init__(
        self,
        parent=None,
        data="",
        settings_dict=None,
        config_dict=None,
        additional_info=None,
    ):
        comboBoxes = {
            "measure_range": ["Auto", "200mV", "2V", "20V", "200V", "2000V", "10A"],
        }
        labels = {"measure_range": "Measurement Range"}
        super().__init__(
            parent,
            "Keithley_197a",
            data,
            settings_dict,
            config_dict,
            additional_info,
            comboBoxes=comboBoxes,
            labels=labels,
        )
        self.comboBox_connection_type.addItem("Local VISA")
        self.load_settings()
