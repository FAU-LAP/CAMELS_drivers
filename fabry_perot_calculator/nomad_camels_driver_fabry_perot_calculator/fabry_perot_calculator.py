import sys
import os
from .fabry_perot_calculator_ophyd import Fabry_Perot_Calculator
from nomad_camels.ui_widgets.path_button_edit import Path_Button_Edit
from nomad_camels.utility import variables_handling
from nomad_camels.ui_widgets.warn_popup import WarnPopup
from PySide6.QtWidgets import QComboBox, QLabel
from PySide6.QtCore import Qt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
try:
    from andor_shamrock_500.nomad_camels_driver_andor_shamrock_500.andor_shamrock_500_config_sub import (
        subclass_config_sub,
    )
except:
    from nomad_camels_driver_andor_shamrock_500.andor_shamrock_500_config_sub import (
        subclass_config_sub,
    )

from nomad_camels.main_classes import device_class


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="fabry_perot_calculator",
            virtual=True,
            tags=["fabry-perot,", "virtual", "instrument"],
            directory="fabry_perot_calculator",
            ophyd_device=Fabry_Perot_Calculator,
            ophyd_class_name="Fabry_Perot_Calculator",
            **kwargs,
        )
        self.config["background_data_path"] = "background data path"
        self.config["reflectivity_data_path"] = "Reflectivity path"
        self.config["!non_string!_spectrometer"] = ""

    def get_necessary_devices(self):
        return [self.config["!non_string!_spectrometer"]]


class subclass_config(device_class.Device_Config):
    def __init__(
        self,
        parent=None,
        data="",
        settings_dict=None,
        config_dict=None,
        additional_info=None,
    ):
        super().__init__(
            parent,
            "Fabry Perot Calculator",
            data,
            settings_dict,
            config_dict,
            additional_info,
        )
        self.comboBox_spectrometer = QComboBox()
        self.comboBox_spectrometer.addItems(list(variables_handling.devices.keys()))
        self.reflectivity_data_path = Path_Button_Edit()
        self.background_data_path = Path_Button_Edit()
        self.layout().addWidget(QLabel("Reflectivity data path"), 20, 0)
        self.layout().addWidget(self.reflectivity_data_path, 20, 1, 1, 4)
        self.layout().addWidget(QLabel("Background data path"), 21, 0)
        self.layout().addWidget(self.background_data_path, 21, 1, 1, 4)
        self.layout().addWidget(QLabel("Spectrometer"), 22, 0)
        self.layout().addWidget(self.comboBox_spectrometer, 22, 1, 1, 4)
        self.load_settings()

    def get_config(self):
        self.config_dict["background_data_path"] = self.background_data_path.get_path()
        self.config_dict["reflectivity_data_path"] = (
            self.reflectivity_data_path.get_path()
        )
        self.config_dict["!non_string!_spectrometer"] = (
            self.comboBox_spectrometer.currentText()
        )
        return super().get_config()
