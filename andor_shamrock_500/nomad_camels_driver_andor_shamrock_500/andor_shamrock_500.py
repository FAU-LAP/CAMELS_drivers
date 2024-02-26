from nomad_camels.main_classes import device_class
from .andor_shamrock_500_ophyd import Andor_Shamrock_500
from nomad_camels.ui_widgets.path_button_edit import Path_Button_Edit
from nomad_camels.ui_widgets.warn_popup import WarnPopup
from PySide6.QtWidgets import QComboBox, QLabel
from PySide6.QtCore import Qt
from .andor_shamrock_500_manual_control import (
    Andor_Manual_Control,
    Andor_Manual_Control_Config,
)
from .andor_shamrock_500_config_sub import subclass_config_sub


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="andor_shamrock_500",
            virtual=False,
            tags=["spectrometer", "spectrum", "Andor"],
            directory="andor_shamrock_500",
            ophyd_device=Andor_Shamrock_500,
            ophyd_class_name="Andor_Shamrock_500",
            **kwargs,
        )
        self.config["set_grating_number"] = 1
        self.config["center_wavelength"] = 800
        self.config["input_port"] = "direct"
        self.config["output_port"] = "direct"
        self.config["!non_string!_camera"] = ""
        self.config["input_slit_size"] = 10
        self.config["output_slit_size"] = 10

        self.controls = {
            "Andor_Manual_Control": [Andor_Manual_Control, Andor_Manual_Control_Config]
        }

    def get_necessary_devices(self):
        return [self.config["!non_string!_camera"]]


class subclass_config(device_class.Device_Config):
    def __init__(
        self,
        parent=None,
        data="",
        settings_dict=None,
        config_dict=None,
        additional_info=None,
        **kwargs,
    ):
        super().__init__(
            parent,
            "Andor Shamrock 500",
            data,
            settings_dict=settings_dict,
            config_dict=config_dict,
            additional_info=additional_info,
            **kwargs,
        )
        self.sub_widget = subclass_config_sub(
            config_dict=config_dict, parent=parent, settings_dict=settings_dict
        )
        dll_label = QLabel(
            "Path to dll (atspectrograph.dll or ShamrockCIF64.dll or ShamrockCIF.dll)"
        )
        self.dll_path = Path_Button_Edit()
        label_spec = QLabel("Spectrometer:")
        self.comboBox_spectrometer = QComboBox()
        self.spectrometer_list = []
        if "dll_path" in settings_dict:
            self.dll_path.line.setText(settings_dict["dll_path"])
        self.update_dll()
        if (
            "spectrometer" in settings_dict
            and settings_dict["spectrometer"] in self.spectrometer_list
        ):
            self.comboBox_spectrometer.setCurrentText(settings_dict["spectrometer"])
        self.layout().addWidget(dll_label, 17, 0, 1, 5)
        self.layout().addWidget(self.dll_path, 18, 0, 1, 5)
        self.layout().addWidget(label_spec, 19, 0)
        self.layout().addWidget(self.comboBox_spectrometer, 19, 1, 1, 4)
        self.dll_path.path_changed.connect(self.update_dll)

        self.layout().addWidget(self.sub_widget, 20, 0, 1, 5)
        self.load_settings()

    def update_dll(self):
        self.setCursor(Qt.WaitCursor)
        dll_path = self.dll_path.get_path()
        if dll_path:
            import pylablib

            pylablib.par["devices/dlls/andor_shamrock"] = dll_path
            from pylablib.devices import Andor

            try:
                self.spectrometer_list = Andor.list_shamrock_spectrographs()
            except Exception as e:
                WarnPopup(self, f"Dll could not be loaded\n{e}", "dll not loaded")
        self.comboBox_spectrometer.clear()
        if self.spectrometer_list:
            self.comboBox_spectrometer.addItems(self.spectrometer_list)
        else:
            self.comboBox_spectrometer.addItem("No spectrometer detected or wrong dll!")
        self.setCursor(Qt.ArrowCursor)

    def get_config(self):
        self.config_dict.update(self.sub_widget.get_config())
        return super().get_config()

    def get_settings(self):
        self.settings_dict["dll_path"] = self.dll_path.get_path()
        self.settings_dict["spectrometer"] = self.comboBox_spectrometer.currentText()
        return super().get_settings()
