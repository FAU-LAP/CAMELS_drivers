# https://pymeasure.readthedocs.io/en/latest/dev/adding_instruments/channels.html

import pkgutil
import inspect
import importlib
import pymeasure.instruments

from nomad_camels.main_classes import device_class
from nomad_camels.ui_widgets.add_remove_table import AddRemoveDialoge

from PySide6.QtWidgets import QLabel, QComboBox, QPushButton

from .pymeasure_instruments_ophyd import (
    get_driver_information,
    make_pymeasure_instruments_ophyd_class,
)

# dict with shape {module_name: [module, [package_names]]}
instrument_modules = {}
for importer, modname, ispkg in pkgutil.iter_modules(pymeasure.instruments.__path__):
    if ispkg:
        module = importlib.import_module(f"pymeasure.instruments.{modname}")
        instrument_classes = [
            name for name, obj in inspect.getmembers(module) if inspect.isclass(obj)
        ]
        instrument_modules[module.__name__.split(".")[-1]] = instrument_classes


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="pymeasure_instruments",
            virtual=False,
            ophyd_device=None,
            ophyd_class_name="make_pymeasure_instruments_ophyd_instance",
            **kwargs,
        )

    def get_channels(self):
        if (
            not "manufacturer" in self.settings
            or not "instrument" in self.settings
            or not "settings" in self.settings
            or not "controls" in self.settings
            or not "measurements" in self.settings
            or not "channels" in self.settings
            or not "config_info" in self.settings
        ):
            return
        manufacturer = self.settings["manufacturer"]
        instrument = self.settings["instrument"]
        settings = self.settings["settings"]
        controls = self.settings["controls"]
        measurements = self.settings["measurements"]
        channels = self.settings["channels"]
        config_info = self.settings["config_info"]
        self.ophyd_class = make_pymeasure_instruments_ophyd_class(
            instrument,
            manufacturer,
            controls,
            measurements,
            settings,
            channels,
            config_info,
        )
        self.ophyd_instance = self.ophyd_class(name="test")
        config, passive_config = device_class.get_configs(self.ophyd_instance)
        for key, value in config.items():
            if key not in self.config:
                self.config[key] = value
        for key, value in passive_config.items():
            if key not in self.config:
                self.config[key] = value
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
        self.comboBox_connection_type.addItem("Local VISA")
        self.load_settings()
        self.connector.set_only_resource_name()
        label_manufacturer = QLabel("Manufacturer")
        label_instrument = QLabel("Instrument")
        self.comboBox_manufacturer = NoScrollQComboBox()
        self.comboBox_instrument = NoScrollQComboBox()
        self.comboBox_manufacturer.addItems(list(instrument_modules.keys()))
        self.doclabel = QLabel()
        self.select_config_button = QPushButton("select configs / channels")

        self.sub_widget = None

        self.current_info = {}
        self.config_info = {
            "name": [],
            "is channel": [],
            "provide read (if channel)": [],
        }

        self.layout().addWidget(label_manufacturer, 20, 0)
        self.layout().addWidget(self.comboBox_manufacturer, 20, 1)
        self.layout().addWidget(label_instrument, 20, 2)
        self.layout().addWidget(self.comboBox_instrument, 20, 3, 1, 2)
        self.layout().addWidget(self.doclabel, 21, 0, 1, 5)
        self.layout().addWidget(self.select_config_button, 22, 0, 1, 5)

        if "manufacturer" in self.settings_dict:
            self.comboBox_manufacturer.setCurrentText(
                self.settings_dict["manufacturer"]
            )
        if "instrument" in self.settings_dict:
            self.comboBox_instrument.setCurrentText(self.settings_dict["instrument"])
        if "measurements" in self.settings_dict:
            self.current_info["measurements"] = self.settings_dict["measurements"]
        if "controls" in self.settings_dict:
            self.current_info["controls"] = self.settings_dict["controls"]
        if "settings" in self.settings_dict:
            self.current_info["settings"] = self.settings_dict["settings"]
        if "channels" in self.settings_dict:
            self.current_info["channels"] = self.settings_dict["channels"]
        if "config_info" in self.settings_dict:
            self.config_info = self.settings_dict["config_info"]

        self.select_config_button.clicked.connect(self.select_configs)
        self.comboBox_manufacturer.currentIndexChanged.connect(
            self.update_instrument_combobox
        )
        self.comboBox_instrument.currentIndexChanged.connect(
            self.update_driver_information
        )
        self.update_instrument_combobox()

    def update_instrument_combobox(self):
        manufacturer = self.comboBox_manufacturer.currentText()
        self.comboBox_instrument.clear()
        self.comboBox_instrument.addItems(instrument_modules[manufacturer])
        self.update_driver_information()

    def update_driver_information(self):
        manufacturer = self.comboBox_manufacturer.currentText()
        instrument = self.comboBox_instrument.currentText()
        if manufacturer and instrument:
            info = get_driver_information(manufacturer, instrument)
            docstring = info["docstring"]
            if "\n\n" in docstring:
                docstring = docstring.split("\n\n")[0]
            elif "\n" in docstring:
                docstring = docstring.split("\n")[0]
            self.doclabel.setText(docstring)
            if manufacturer != self.settings_dict.get(
                "manufacturer", ""
            ) or instrument != self.settings_dict.get("instrument", ""):
                self.current_info = info
                self.config_info = {
                    "name": [],
                    "is channel": [],
                    "provide read (if channel)": [],
                }
            self.update_config_selection()

    def select_configs(self):
        config_info = {}

        headerLabels = ["name", "is channel", "provide read (if channel)"]
        tableData = {"name": [], "is channel": [], "provide read (if channel)": []}
        for key in self.current_info["controls"]:
            if key in self.config_info["name"]:
                tableData["name"].append(self.config_info["name"])
                tableData["is channel"].append(self.config_info["is channel"])
                tableData["provide read (if channel)"].append(
                    self.config_info["provide read (if channel)"]
                )
            else:
                tableData["name"].append(key)
                tableData["is channel"].append(False)
                tableData["provide read (if channel)"].append(True)
        config_selection = AddRemoveDialoge(
            headerLabels=headerLabels,
            editables=[],
            checkables=[1, 2],
            tableData=tableData,
            title="Select set and read as channels",
        )
        config_selection.table.addButton.setHidden(True)
        config_selection.table.removeButton.setHidden(True)
        if config_selection.exec():
            config_info = config_selection.table.update_table_data()

        headerLabels = ["name", "is channel"]
        tableData = {"name": [], "is channel": []}
        for key in self.current_info["settings"]:
            if key in self.config_info["name"]:
                tableData["name"].append(self.config_info["name"])
                tableData["is channel"].append(self.config_info["is channel"])
            else:
                tableData["name"].append(key)
                tableData["is channel"].append(False)
        for key in self.current_info["measurements"]:
            if key in self.config_info["name"]:
                tableData["name"].append(self.config_info["name"])
                tableData["is channel"].append(self.config_info["is channel"])
            else:
                tableData["name"].append(key)
                tableData["is channel"].append(False)
        config_selection = AddRemoveDialoge(
            headerLabels=headerLabels,
            editables=[],
            checkables=[1],
            tableData=tableData,
            title="Select set / read only as channels",
        )
        config_selection.table.addButton.setHidden(True)
        config_selection.table.removeButton.setHidden(True)
        if config_selection.exec():
            n = 0
            for key, value in config_selection.table.update_table_data().items():
                config_info[key] += value
                n = len(value)
            config_info["provide read (if channel)"] += [False] * n
        self.config_info = config_info

        self.update_config_selection()

    def update_config_selection(self):
        if self.sub_widget:
            self.sub_widget.deleteLater()
        comboboxes = make_comboboxes(self.current_info)
        ophyd_class = make_pymeasure_instruments_ophyd_class(
            self.comboBox_instrument.currentText(),
            self.comboBox_manufacturer.currentText(),
            self.current_info["controls"],
            self.current_info["measurements"],
            self.current_info["settings"],
            self.current_info["channels"],
            self.config_info,
        )
        if not ophyd_class:
            return
        removers = []
        for key in self.config_dict:
            if key not in self.config_info["name"]:
                removers.append(key)
        for key in removers:
            self.config_dict.pop(key)
        _, configs = device_class.get_configs(ophyd_class(name="test"))
        for key, value in configs.items():
            if key not in self.config_dict:
                self.config_dict[key] = value
        self.sub_widget = device_class.Simple_Config_Sub(
            config_dict=self.config_dict,
            comboBoxes=comboboxes,
        )
        self.layout().addWidget(self.sub_widget, 23, 0, 1, 5)

    def get_settings(self):
        settings = super().get_settings()
        settings["manufacturer"] = self.comboBox_manufacturer.currentText()
        settings["instrument"] = self.comboBox_instrument.currentText()
        settings["controls"] = self.current_info["controls"]
        settings["measurements"] = self.current_info["measurements"]
        settings["settings"] = self.current_info["settings"]
        settings["channels"] = self.current_info["channels"]
        settings["config_info"] = self.config_info
        return settings

    def get_config(self):
        config = super().get_config()
        if self.sub_widget:
            config.update(self.sub_widget.get_config())
        return config


def make_comboboxes(info_package):
    comboboxes = {}
    for name, info in info_package["controls"].items():
        if info["discrete"] and not info["boolean"]:
            comboboxes[name] = info["values"]
    for name, info in info_package["settings"].items():
        if info["discrete"] and not info["boolean"]:
            comboboxes[name] = info["values"]
    for channel, channel_info in info_package["channels"].items():
        comboboxes.update(make_comboboxes(channel_info))
    return comboboxes


class NoScrollQComboBox(QComboBox):
    def wheelEvent(self, event):
        # Ignore the event, effectively disabling mouse wheel scrolling
        event.ignore()
