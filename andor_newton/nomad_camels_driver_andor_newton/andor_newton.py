from nomad_camels.main_classes import device_class
from nomad_camels.ui_widgets.add_remove_table import AddRemoveTable
from nomad_camels.ui_widgets.path_button_edit import Path_Button_Edit
from nomad_camels.ui_widgets.warn_popup import WarnPopup
from .andor_newton_config import Ui_andor_newton_config
from .andor_newton_ophyd import Andor_Newton, get_cameras
from PySide6.QtWidgets import QComboBox, QLabel
from PySide6.QtCore import Qt, Signal


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="andor_newton",
            virtual=False,
            tags=[
                "Camera",
                "spectrometer",
                "CCD",
                "spectrum",
                "Andor",
            ],
            directory="andor_newton",
            ophyd_device=Andor_Newton,
            ophyd_class_name="Andor_Newton",
            **kwargs,
        )
        self.config["set_temperature"] = -60
        self.config["shutter_mode"] = "auto"
        self.config["exposure_time"] = 1
        self.config["readout_mode"] = "FVB - full vertical binning"
        self.config["preamp_gain"] = 4
        self.config["horizontal_binning"] = 1
        self.config["hs_speed"] = 0.05
        self.config["vs_speed"] = 25.7
        self.config["multi_tracks"] = {}
        self.config["shutter_ttl_open"] = "low"


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
            "Andor Newton",
            data,
            settings_dict=settings_dict,
            config_dict=config_dict,
            additional_info=additional_info,
            **kwargs,
        )
        self.dll_path = Path_Button_Edit()
        if "dll_path" in settings_dict:
            self.dll_path.line.setText(settings_dict["dll_path"])
        self.comboBox_camera = QComboBox()
        self.update_dll()
        if "camera" in self.settings_dict:
            if isinstance(self.settings_dict["camera"], int):
                self.comboBox_camera.setCurrentIndex(self.settings_dict["camera"])
            else:
                self.comboBox_camera.setCurrentText(self.settings_dict["camera"])
        self.layout().addWidget(
            QLabel("Path to dll (atmcd64d_legacy.dll or atmcd64d.dll)"), 17, 0, 1, 5
        )
        self.layout().addWidget(self.dll_path, 18, 0, 1, 5)
        self.layout().addWidget(QLabel("Camera:"), 19, 0)
        self.layout().addWidget(self.comboBox_camera, 19, 1, 1, 4)
        self.dll_path.path_changed.connect(self.update_dll)

        self.sub_widget = subclass_config_sub(
            config_dict=config_dict, parent=parent, settings_dict=settings_dict
        )
        self.layout().addWidget(self.sub_widget, 20, 0, 1, 5)
        self.load_settings()

    def update_dll(self):
        self.setCursor(Qt.WaitCursor)
        cam_list = []
        dll_path = self.dll_path.get_path()
        if dll_path:
            import pylablib

            pylablib.par["devices/dlls/andor_sdk2"] = dll_path
            from pylablib.devices import Andor

            try:
                cam_list = get_cameras()
            except Exception as e:
                WarnPopup(self, f"Dll could not be loaded\n{e}", "dll not loaded")
        self.comboBox_camera.clear()
        if cam_list:
            self.comboBox_camera.addItems(cam_list)
        else:
            self.comboBox_camera.addItem("No camera detected or wrong dll!")
        self.setCursor(Qt.ArrowCursor)

    def get_config(self):
        self.config_dict.update(self.sub_widget.get_config())
        return super().get_config()

    def get_settings(self):
        self.settings_dict["dll_path"] = self.dll_path.get_path()
        self.settings_dict["camera"] = self.comboBox_camera.currentText()
        return super().get_settings()


class subclass_config_sub(device_class.Device_Config_Sub, Ui_andor_newton_config):
    config_changed = Signal(object, str)

    def __init__(self, config_dict=None, parent=None, settings_dict=None):
        super().__init__(
            parent=parent, config_dict=config_dict, settings_dict=settings_dict
        )
        self.setupUi(self)
        tableData = {}
        if "multi_tracks" in config_dict:
            tableData = config_dict["multi_tracks"]
        self.track_table = AddRemoveTable(
            headerLabels=["Start", "End"], tableData=tableData, title="Tracks"
        )
        self.tracks_frame.layout().addWidget(self.track_table)
        self.load_config()
        self.set_temperature.lineEdit().returnPressed.connect(
            lambda x=None, y="set_temperature": self.config_changed.emit(x, y)
        )
        self.comboBox_shutter_mode.currentTextChanged.connect(
            lambda x=None, y="shutter_mode": self.config_changed.emit(x, y)
        )
        self.comboBox_shutter_ttl.currentTextChanged.connect(
            lambda x=None, y="shutter_ttl_open": self.config_changed.emit(x, y)
        )
        self.exposure_time.lineEdit().returnPressed.connect(
            lambda x=None, y="exposure_time": self.config_changed.emit(x, y)
        )
        self.comboBox_readout_mode.currentTextChanged.connect(
            lambda x=None, y="readout_mode": self.config_changed.emit(x, y)
        )
        self.preamp_gain.lineEdit().returnPressed.connect(
            lambda x=None, y="preamp_gain": self.config_changed.emit(x, y)
        )
        self.horizontal_binning.lineEdit().returnPressed.connect(
            lambda x=None, y="horizontal_binning": self.config_changed.emit(x, y)
        )
        self.hs_speed.lineEdit().returnPressed.connect(
            lambda x=None, y="hs_speed": self.config_changed.emit(x, y)
        )
        self.vs_speed.lineEdit().returnPressed.connect(
            lambda x=None, y="vs_speed": self.config_changed.emit(x, y)
        )
        # self.track_table.table.clicked.connect(lambda x=None, y='multi_tracks': self.config_changed.emit(x,y))

    def load_config(self):
        tableData = {}
        if "multi_tracks" in self.config_dict:
            tableData = self.config_dict["multi_tracks"]
        self.track_table.change_table_data(tableData)
        if "set_temperature" in self.config_dict:
            self.set_temperature.setValue(self.config_dict["set_temperature"])
        if "get_temperature" in self.config_dict:
            self.lineEdit_current_temperature.setText(
                f'{self.config_dict["get_temperature"]:.2f}'
            )
            self.lineEdit_current_temperature.setHidden(False)
            if "temperature_status" in self.config_dict:
                from nomad_camels.utility import variables_handling

                color = (
                    "green"
                    if self.config_dict["temperature_status"] == "stabilized"
                    else "red"
                )
                self.lineEdit_current_temperature.setStyleSheet(
                    f"background-color: rgb{variables_handling.get_color(color, True)}"
                )
        else:
            self.lineEdit_current_temperature.setHidden(True)
        if "shutter_mode" in self.config_dict:
            self.comboBox_shutter_mode.setCurrentText(self.config_dict["shutter_mode"])
        if "shutter_ttl_open" in self.config_dict:
            self.comboBox_shutter_ttl.setCurrentText(
                self.config_dict["shutter_ttl_open"]
            )
        if "exposure_time" in self.config_dict:
            self.exposure_time.setValue(self.config_dict["exposure_time"])
        if "readout_mode" in self.config_dict:
            self.comboBox_readout_mode.setCurrentText(self.config_dict["readout_mode"])
        if "preamp_gain" in self.config_dict:
            self.preamp_gain.setValue(self.config_dict["preamp_gain"])
        if "horizontal_binning" in self.config_dict:
            self.horizontal_binning.setValue(self.config_dict["horizontal_binning"])
        if "hs_speed" in self.config_dict:
            self.hs_speed.setValue(self.config_dict["hs_speed"])
        if "vs_speed" in self.config_dict:
            self.vs_speed.setValue(self.config_dict["vs_speed"])

    def get_config(self):
        self.config_dict["set_temperature"] = self.set_temperature.value()
        self.config_dict["shutter_mode"] = self.comboBox_shutter_mode.currentText()
        self.config_dict["shutter_ttl_open"] = self.comboBox_shutter_ttl.currentText()
        self.config_dict["exposure_time"] = self.exposure_time.value()
        self.config_dict["readout_mode"] = self.comboBox_readout_mode.currentText()
        self.config_dict["preamp_gain"] = self.preamp_gain.value()
        self.config_dict["horizontal_binning"] = self.horizontal_binning.value()
        self.config_dict["hs_speed"] = self.hs_speed.value()
        self.config_dict["vs_speed"] = self.vs_speed.value()
        self.config_dict["multi_tracks"] = self.track_table.update_table_data()
        return super().get_config()
