from nomad_camels.main_classes import device_class
from nomad_camels.ui_widgets.path_button_edit import Path_Button_Edit

from .SweepMe_device_ophyd import (
    get_driver,
    get_ports,
    special_keys,
    make_ophyd_class,
    make_valid_python_identifier,
)

from PySide6.QtWidgets import QLabel
import os


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="SweepMe_device",
            virtual=False,
            ophyd_device=None,
            ophyd_class_name="make_ophyd_instance",
            **kwargs,
        )
        self.settings["driver"] = ""
        self.settings["port"] = ""

    def update_driver(self):
        if not "driver" in self.settings or not self.settings["driver"]:
            return
        driver_path = self.settings["driver"]
        driver_name = os.path.basename(driver_path)
        class_name = make_valid_python_identifier(f"SweepMe_{driver_name}")
        self.ophyd_class = make_ophyd_class(driver_path, class_name)
        self.ophyd_instance = self.ophyd_class(driver=driver_path, name="test")
        config, passive_config = get_configs_from_ophyd(self.ophyd_instance)
        for key, value in config.items():
            if key not in self.config:
                self.config[key] = value
        for key, value in passive_config.items():
            if key not in self.config:
                self.config[key] = value

    def get_channels(self):
        self.update_driver()
        return super().get_channels()


class subclass_config(device_class.Device_Config):
    def __init__(
        self,
        parent=None,
        device_name="",
        data="",
        settings_dict=None,
        config_dict=None,
        additional_info=None,
    ):
        super().__init__(
            parent, device_name, data, settings_dict, config_dict, additional_info
        )
        label_driver = QLabel("Select SweepMe! driver:")
        self.driver_selection = Path_Button_Edit(select_directory=True)
        if "driver" in self.settings_dict:
            self.driver_selection.set_path(self.settings_dict["driver"])
        self.layout().addWidget(label_driver, 20, 0)
        self.layout().addWidget(self.driver_selection, 20, 1, 1, 4)
        self.sub_widget = None

        self.driver_selection.path_changed.connect(self.driver_changed)
        self.driver_changed()

    def get_settings(self):
        settings = super().get_settings()
        settings["driver"] = self.driver_selection.get_path()
        config = {}
        if self.sub_widget:
            config = self.sub_widget.get_config()
        if "Port" in config:
            settings["port"] = config["Port"]
        return settings

    def get_config(self):
        config = super().get_config()
        if self.sub_widget:
            config.update(self.sub_widget.get_config())
        if "Port" in config:
            config.pop("Port")
        return config

    def driver_changed(self):
        try:
            driver = get_driver(self.driver_selection.get_path())
        except Exception as e:
            print(e)
            return
        comboboxes = {}
        labels = {}
        if not driver.port_manager and "Port" in self.config_dict:
            self.config_dict.pop("Port")
        elif driver.port_manager and "Port" not in self.config_dict:
            self.config_dict.update({"Port": ""})
        if driver.port_manager:
            ports = get_ports(driver)
            comboboxes.update({"Port": ports})
        parameters = driver.set_GUIparameter()
        removers = []
        for key in self.config_dict:
            if key not in list(parameters.keys()) + ["Port"]:
                removers.append(key)
        for key in removers:
            self.config_dict.pop(key)

        for key, value in parameters.items():
            if key in special_keys:
                continue
            name = make_valid_python_identifier(key)
            if name != key:
                labels.update({name: key})
            islist = False
            if isinstance(value, list):
                comboboxes.update({name: value})
                islist = True
            if name not in self.config_dict:
                if islist:
                    self.config_dict.update({name: value[0]})
                else:
                    self.config_dict.update({name: parameters[key]})

        if self.sub_widget:
            self.sub_widget.deleteLater()
        self.sub_widget = device_class.Simple_Config_Sub(
            config_dict=self.config_dict,
            comboBoxes=comboboxes,
            labels=labels,
        )
        self.layout().addWidget(self.sub_widget, 25, 0, 1, 5)


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
