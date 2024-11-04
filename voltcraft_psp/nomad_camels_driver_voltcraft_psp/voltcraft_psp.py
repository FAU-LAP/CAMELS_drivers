import copy

from PySide6.QtWidgets import QLineEdit, QLabel, QComboBox

from nomad_camels.main_classes import device_class

from .voltcraft_psp_ophyd import Voltcraft_PSP


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="voltcraft_psp",
            tags=["power supply", "voltage"],
            ophyd_device=Voltcraft_PSP,
            ophyd_class_name="Voltcraft_PSP",
            **kwargs
        )
        self.settings["model"] = "PSP 1803"


class subclass_config(device_class.Simple_Config):
    def __init__(
        self,
        parent=None,
        data="",
        settings_dict=None,
        config_dict=None,
        additional_info=None,
    ):
        comboboxes = {"model": ["PSP 1405", "PSP 12010", "PSP 1803"]}
        super().__init__(
            parent,
            "Voltcraft PSP",
            data,
            settings_dict,
            config_dict,
            additional_info,
            comboBoxes=comboboxes,
        )
        self.comboBox_connection_type.addItem("Local VISA")
        self.load_settings()
