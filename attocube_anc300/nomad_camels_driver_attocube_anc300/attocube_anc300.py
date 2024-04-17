from .attocube_anc300_ophyd import make_attocube_anc300_class
from pylablib.devices import Attocube
from nomad_camels.main_classes import device_class
from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QLineEdit,
    QCheckBox,
    QLabel,
    QPushButton,
    QTabWidget,
    QComboBox,
)
import pyvisa
import re


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="attocube_anc300",
            virtual=False,
            tags=["positioning", "stage"],
            directory="attocube_anc300",
            ophyd_device=None,
            ophyd_class_name="make_attocube_anc300_instance",
            **kwargs,
        )
        self.settings["connection_type"] = "Ethernet"

    def update_driver(self):
        if (
            not "available_axis_numbers" in self.settings
            or not self.settings["available_axis_numbers"]
        ):
            return
        # make_attocube_anc300_class is a function that returns a class with components that are generated at runtime
        # here we pass the connection_type to the make_attocube_anc300_class which creates the class
        self.ophyd_class = make_attocube_anc300_class(
            self.settings["available_axis_numbers"]
        )
        # now we create an instance of the class
        # name="test" prevents the instrument driver from actually trying to connect directly to the physical instrument
        self.ophyd_instance = self.ophyd_class(
            available_axis_numbers=self.settings["available_axis_numbers"],
            ip_address=self.settings["ip_address"],
            port=self.settings["port"],
            com_port=self.settings["com_port"],
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
        comboBoxes = {"connection_type": ["Ethernet", "USB"]}
        labels = {"connection_type": "Connection type"}
        # If ip_address is already found in the settings window, we dont want to create a GUI
        # element for it, so we pop it and then call super
        if "ip_address" in settings_dict:
            ip_address = settings_dict.pop("ip_address")
        else:
            ip_address = "192.168.1.1"
        if "port" in settings_dict:
            port = settings_dict.pop("port")
        else:
            port = "7230"
        if "com_port" in settings_dict:
            com_port = settings_dict.pop("com_port")
        else:
            com_port = ""
        if "available_axis_numbers" in settings_dict:
            available_axis_numbers = settings_dict.pop("available_axis_numbers")
        else:
            available_axis_numbers = ""
        super().__init__(
            parent,
            "attocube_anc300",
            data,
            settings_dict,
            config_dict,
            additional_info,
            comboBoxes=comboBoxes,
            labels=labels,
        )
        self.settings_dict["available_axis_numbers"] = available_axis_numbers
        self.settings_dict["ip_address"] = ip_address
        self.settings_dict["port"] = port
        self.settings_dict["com_port"] = com_port

        self.load_settings()
        self.sub_widget.setting_combos["connection_type"].currentIndexChanged.connect(
            self.change_connection_type
        )
        self.widget_ip_address_label = QLabel("IP Address")
        self.widget_ip_address = QLineEdit(str(ip_address))
        self.widget_ip_address.textChanged.connect(self.update_ip_address)
        self.layout().addWidget(self.widget_ip_address, 11, 1, 1, 5)
        self.layout().addWidget(self.widget_ip_address_label, 11, 0, 1, 1)

        self.widget_port_label = QLabel("Port")
        self.widget_port = QLineEdit(str(port))
        self.widget_port.textChanged.connect(self.update_port)
        self.layout().addWidget(self.widget_port, 12, 1, 1, 5)
        self.layout().addWidget(self.widget_port_label, 12, 0, 1, 1)

        self.widget_com_port_label = QLabel("COM Port")
        self.widget_com_port = QComboBox()
        self.widget_com_port.setCurrentText(str(com_port))
        self.widget_com_port.currentIndexChanged.connect(self.update_com_port)
        self.layout().addWidget(self.widget_com_port, 13, 1, 1, 5)
        self.layout().addWidget(self.widget_com_port_label, 13, 0, 1, 1)

        rm = pyvisa.ResourceManager()
        self.ports = rm.list_resources()
        self.widget_com_port.addItems(self.ports)
        self.change_connection_type(
            conn_type=self.sub_widget.setting_combos["connection_type"].currentText()
        )

    def change_connection_type(self, conn_type=None):
        if conn_type == "USB":
            self.widget_ip_address.setHidden(True)
            self.widget_ip_address_label.setHidden(True)
            self.widget_port.setHidden(True)
            self.widget_port_label.setHidden(True)
            self.widget_com_port.setHidden(False)
            self.widget_com_port_label.setHidden(False)
        elif conn_type == "Ethernet":
            self.widget_ip_address.setHidden(False)
            self.widget_ip_address_label.setHidden(False)
            self.widget_port.setHidden(False)
            self.widget_port_label.setHidden(False)
            self.widget_com_port.setHidden(True)
            self.widget_com_port_label.setHidden(True)
        else:
            if self.sub_widget.setting_combos["connection_type"].currentText() == "USB":
                self.widget_ip_address.setHidden(True)
                self.widget_ip_address_label.setHidden(True)
                self.widget_port.setHidden(True)
                self.widget_port_label.setHidden(True)
                self.widget_com_port.setHidden(False)
                self.widget_com_port_label.setHidden(False)
            if (
                self.sub_widget.setting_combos["connection_type"].currentText()
                == "Ethernet"
            ):
                self.widget_ip_address.setHidden(False)
                self.widget_ip_address_label.setHidden(False)
                self.widget_port.setHidden(False)
                self.widget_port_label.setHidden(False)
                self.widget_com_port.setHidden(True)
                self.widget_com_port_label.setHidden(True)

    def get_settings(self):
        settings = super().get_settings()
        settings["connection_type"] = self.sub_widget.setting_combos[
            "connection_type"
        ].currentText()
        try:
            settings["com_port"] = int(
                re.match("ASRL(\d+)", self.widget_com_port.currentText()).group(1)
            )
        except AttributeError:
            settings["com_port"] = None
            self.widget_com_port.setCurrentText("No COM Port available")

        settings["ip_address"] = self.widget_ip_address.text()
        settings["port"] = int(self.widget_port.text())
        if settings["connection_type"] == "USB":
            atc = Attocube.ANC300(f"COM{settings['com_port']}")
            self.settings_dict["available_axis_numbers"] = atc.get_all_axes()
        elif settings["connection_type"] == "Ethernet":
            atc = Attocube.ANC300(
                (self.settings_dict["ip_address"], int(self.settings_dict["port"]))
            )
            self.settings_dict["available_axis_numbers"] = atc.get_all_axes()

        return settings

    def update_com_port(self):
        try:
            self.settings_dict["com_port"] = int(
                re.match("ASRL(\d+)", self.widget_com_port.currentText()).group(1)
            )
        except AttributeError:
            self.settings_dict["com_port"] = None
            self.widget_com_port.setCurrentText("No COM Port available")

    def update_port(self):
        self.settings_dict["port"] = int(self.widget_port.text())

    def update_ip_address(self):
        self.settings_dict["ip_address"] = self.widget_ip_address.text()


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
