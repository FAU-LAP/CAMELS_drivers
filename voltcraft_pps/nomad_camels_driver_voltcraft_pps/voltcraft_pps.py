import copy

from PySide6.QtWidgets import QLineEdit, QLabel, QComboBox

from nomad_camels.main_classes import device_class

from .voltcraft_pps_ophyd import Voltcraft_PPS


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="voltcraft_pps",
            tags=["power supply", "voltage"],
            ophyd_device=Voltcraft_PPS,
            ophyd_class_name="Voltcraft_PPS",
            **kwargs
        )


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
            parent, "Voltcraft PPS", data, settings_dict, config_dict, additional_info
        )
        self.comboBox_connection_type.addItem("Local VISA")
        self.lineEdit_R = QLineEdit()
        self.lineEdit_R.setText(str(config_dict["setR"]))
        self.labelR = QLabel("Resistance:")
        labelOutput = QLabel("Output mode:")

        self.layout().addWidget(labelOutput, 20, 0)
        self.layout().addWidget(self.labelR, 20, 2)
        self.layout().addWidget(self.lineEdit_R, 20, 3, 1, 2)

        self.load_settings()

    def get_config(self):
        super().get_config()
        r = self.lineEdit_R.text()
        self.config_dict["setR"] = float(r) if r else 0
        return self.config_dict
