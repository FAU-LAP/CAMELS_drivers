from .andor_shamrock_500_config import Ui_andor_shamrock500_config
from nomad_camels.utility import variables_handling
from nomad_camels.main_classes import device_class


class subclass_config_sub(device_class.Device_Config_Sub, Ui_andor_shamrock500_config):
    def __init__(self, config_dict=None, parent=None, settings_dict=None):
        super().__init__(
            parent=parent, config_dict=config_dict, settings_dict=settings_dict
        )
        self.setupUi(self)
        devs = list(variables_handling.devices.keys())
        self.comboBox_camera.addItems(devs)
        self.load_config()

    def load_config(self):
        if "set_grating_number" in self.config_dict:
            self.set_grating_number.setValue(self.config_dict["set_grating_number"])
        if "center_wavelength" in self.config_dict:
            self.initial_wavelength.setValue(self.config_dict["center_wavelength"])
        if "input_port" in self.config_dict:
            self.input_port.setCurrentText(self.config_dict["input_port"])
        if "output_port" in self.config_dict:
            self.output_port.setCurrentText(self.config_dict["output_port"])
        if "input_slit_size" in self.config_dict:
            self.input_slit_size.setValue(self.config_dict["input_slit_size"])
        if "output_slit_size" in self.config_dict:
            self.output_slit_size.setValue(self.config_dict["output_slit_size"])
        devs = list(variables_handling.devices.keys())
        if (
            "!non_string!_camera" in self.config_dict
            and self.config_dict["!non_string!_camera"] in devs
        ):
            self.comboBox_camera.setCurrentText(self.config_dict["!non_string!_camera"])
        if "horizontal_cam_flip" in self.config_dict:
            self.checkBox_horizontal_flip.setChecked(
                self.config_dict["horizontal_cam_flip"]
            )
        if "wavelength" in self.config_dict:
            wl = self.config_dict["wavelength"]
            self.lineEdit_wl_end.setText(f"{max(wl):.2f}")
            self.lineEdit_wl_start.setText(f"{min(wl):.2f}")
            self.lineEdit_wl_end.setHidden(False)
            self.lineEdit_wl_start.setHidden(False)
        else:
            self.lineEdit_wl_end.setHidden(True)
            self.lineEdit_wl_start.setHidden(True)

    def get_config(self):
        self.config_dict["set_grating_number"] = self.set_grating_number.value()
        self.config_dict["center_wavelength"] = self.initial_wavelength.value()
        self.config_dict["input_port"] = self.input_port.currentText()
        self.config_dict["output_port"] = self.output_port.currentText()
        self.config_dict["!non_string!_camera"] = self.comboBox_camera.currentText()
        self.config_dict["input_slit_size"] = self.input_slit_size.value()
        self.config_dict["output_slit_size"] = self.output_slit_size.value()
        self.config_dict["horizontal_cam_flip"] = (
            self.checkBox_horizontal_flip.isChecked()
        )
        return super().get_config()
