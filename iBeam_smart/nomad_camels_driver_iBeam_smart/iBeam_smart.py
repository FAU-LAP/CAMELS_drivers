from .iBeam_smart_ophyd import Ibeam_Smart

from nomad_camels.main_classes import device_class
from serial import SerialException
import re
from pylablib.devices import Toptica
from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QLineEdit,
    QCheckBox,
    QLabel,
    QPushButton,
    QTabWidget,
)
from .iBeam_smart_ophyd import make_ophyd_class
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

bold_font = QFont()
bold_font.setBold(True)


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="iBeam_smart",
            virtual=False,
            tags=["laser", "toptica", "ibeam"],
            directory="iBeam_smart",
            ophyd_device=None,
            ophyd_class_name="make_ophyd_instance_iBeam",
            **kwargs,
        )
        self.config["use_FINE"] = False
        self.config["use_SKILL"] = False
        self.config["use_FINE_type"] = "FINE A"
        self.config["use_SKILL_type"] = "1"

    def update_driver(self):
        if not "channels" in self.settings or not self.settings["channels"]:
            return
        self.ophyd_class = make_ophyd_class(self.settings["channels"])
        self.ophyd_instance = self.ophyd_class(
            channels=self.settings["channels"],
            baudrate=self.settings["baudrate"],
            name="test",
        )
        config, passive_config = get_configs_from_ophyd(self.ophyd_instance)
        for key, value in config.items():
            if key not in self.config:
                self.config[key] = value
        for key, value in passive_config.items():
            if key not in self.passive_config:
                self.passive_config[key] = value

    def get_channels(self):
        self.update_driver()
        return super().get_channels()


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
            "use_FINE_type": ["FINE A", "FINE B"],
            "use_SKILL_type": ["1", "2"],
        }
        labels = {
            "use_FINE": "Use FINE",
            "use_SKILL": "Use SKILL",
            "use_FINE_type": "FINE type",
            "use_SKILL_type": "SKILL type",
        }
        if "channels" in settings_dict:
            channels = settings_dict.pop("channels")
        else:
            channels = {}
        if "Com_port" in settings_dict:
            com_port = settings_dict.pop("Com_port")
        else:
            com_port = ""
        if "baudrate" in settings_dict:
            baudrate = settings_dict.pop("baudrate")
        else:
            baudrate = "115200"
        super().__init__(
            parent,
            "iBeam_smart",
            data,
            settings_dict,
            config_dict,
            additional_info,
            comboBoxes=comboBoxes,
            labels=labels,
        )
        self.settings_dict["channels"] = channels
        self.settings_dict["Com_port"] = com_port
        self.get_iBeam_channels_label = QLabel("")
        self.layout().addWidget(self.get_iBeam_channels_label, 21, 0, 1, 5)
        self.channels = []
        self.load_settings()
        self.comboBox_connection_type.addItem("Local VISA")
        self.load_settings()
        self.connector.set_only_resource_name()
        self.connector.lineEdit_baud.setHidden(False)
        self.connector.lineEdit_baud.setText(baudrate)
        self.get_iBeam_channels()
        self.connector.comboBox_port.currentIndexChanged.connect(
            self.get_iBeam_channels
        )

    def get_iBeam_channels(self):
        self.setCursor(Qt.WaitCursor)
        try:
            com_port = re.match(
                "ASRL(\d+)", self.connector.comboBox_port.currentText()
            ).group(1)
            self.settings_dict["Com_port"] = com_port
            laser = Toptica.TopticaIBeam(
                (f"COM{com_port}", self.connector.lineEdit_baud.text())
            )
            channels_number = laser.get_channels_number()
            laser.close()
            self.channels = [f"{i}" for i in range(1, channels_number + 1)]
            self.settings_dict["channels"] = self.channels

            self.get_iBeam_channels_label.setText(
                f"Number of available channels: {channels_number}"
            )
            self.setCursor(Qt.ArrowCursor)
        except:
            self.get_iBeam_channels_label.setText(
                f"Failed to get the number of available channels. Check if you have selected the correct ASRL(COM) port."
            )
            self.setCursor(Qt.ArrowCursor)
            return

    def get_settings(self):
        settings = super().get_settings()
        settings["baudrate"] = self.connector.lineEdit_baud.text()
        return settings


def get_configs_from_ophyd(ophyd_instance):
    config = {}
    passive_config = {}
    for comp in ophyd_instance.walk_components():
        name = comp.item.attr
        dev_class = comp.item.cls
        if name in ophyd_instance.configuration_attrs:
            if device_class.check_output(dev_class):
                config.update({f"{name}": 0})
            else:
                passive_config.update({f"{name}": 0})
    return config, passive_config
