import sys
import os
from .fabry_perot_calculator_ophyd import Fabry_Perot_Calculator
from nomad_camels.ui_widgets.path_button_edit import Path_Button_Edit
from nomad_camels.ui_widgets.add_remove_table import AddRemoveTable
from nomad_camels.utility import variables_handling
from nomad_camels.ui_widgets.warn_popup import WarnPopup
from PySide6.QtWidgets import QComboBox, QLabel, QFrame
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
        self.settings["background_data_path"] = "background data path"
        self.settings["reflectivity_data_path"] = "Reflectivity path"
        self.settings["plot_savepath"] = ""
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
            "Fabry_Perot_Calculator",
            data,
            settings_dict,
            config_dict,
            additional_info,
        )
        self.add_remove_table_materials = AddRemoveTable(
            headerLabels=[
                "Material",
                "Refractive Index",
                "Thickness (m)",
                "Fit start",
                "Fit min",
                "Fit max",
            ]
        )
        self.comboBox_spectrometer = QComboBox()
        self.comboBox_spectrometer.addItems(list(variables_handling.devices.keys()))
        if "!non_string!_spectrometer" in self.config_dict:
            self.comboBox_spectrometer.setCurrentText(
                self.config_dict["!non_string!_spectrometer"]
            )
        self.reflectivity_data_path = Path_Button_Edit()
        self.background_data_path = Path_Button_Edit()
        if "reflectivity_data_path" in self.settings_dict:
            self.reflectivity_data_path.set_path(
                self.settings_dict["reflectivity_data_path"]
            )
        if "background_data_path" in self.settings_dict:
            self.background_data_path.set_path(
                self.settings_dict["background_data_path"]
            )
        if "materials" in self.settings_dict:
            self.add_remove_table_materials.change_table_data(
                self.settings_dict["materials"]
            )
        self.layout().addWidget(QLabel("Reflectivity data path"), 20, 0)
        self.layout().addWidget(self.reflectivity_data_path, 20, 1, 1, 4)
        self.layout().addWidget(QLabel("Background data path"), 21, 0)
        self.layout().addWidget(self.background_data_path, 21, 1, 1, 4)
        self.layout().addWidget(QLabel("Spectrometer"), 22, 0)
        self.layout().addWidget(self.comboBox_spectrometer, 22, 1, 1, 4)
        # Add Remove Table to define the material stack you want to calculate the reflectivity for
        # Create horizontal line to separate the next section
        h_line = QFrame()
        h_line.setFrameShape(QFrame.HLine)
        h_line.setFrameShadow(QFrame.Sunken)
        self.layout().addWidget(h_line, 23, 0, 1, 5)
        self.layout().addWidget(QLabel("Material stack"), 24, 0, 1, 5)
        self.layout().addWidget(self.add_remove_table_materials, 25, 0, 1, 5)
        # Savepath for the plots of the data and fits
        self.plot_savepath = Path_Button_Edit(select_directory=True)
        if "plot_savepath" in self.settings_dict:
            self.plot_savepath.set_path(self.settings_dict["plot_savepath"])
        self.layout().addWidget(QLabel("Plot savepath"), 26, 0)
        self.layout().addWidget(self.plot_savepath, 26, 1, 1, 4)

        self.load_settings()

    def get_config(self):
        self.config_dict["!non_string!_spectrometer"] = (
            self.comboBox_spectrometer.currentText()
        )
        return super().get_config()

    def get_settings(self):
        self.settings_dict["reflectivity_data_path"] = (
            self.reflectivity_data_path.get_path()
        )
        self.settings_dict["background_data_path"] = (
            self.background_data_path.get_path()
        )
        self.settings_dict["materials"] = (
            self.add_remove_table_materials.update_table_data()
        )
        self.settings_dict["plot_savepath"] = self.plot_savepath.get_path()
        return super().get_settings()
