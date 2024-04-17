# https://pymeasure.readthedocs.io/en/latest/dev/adding_instruments/channels.html

import pkgutil
import inspect
import importlib
import pymeasure.instruments

from nomad_camels.main_classes import device_class
from nomad_camels.ui_widgets.add_remove_table import AddRemoveDialoge

from PySide6.QtWidgets import QLabel, QComboBox, QPushButton

from .pymeasure_instruments_ophyd import get_driver_information

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
        label_manufacturer = QLabel("Manufacturer")
        label_instrument = QLabel("Instrument")
        self.comboBox_manufacturer = NoScrollQComboBox()
        self.comboBox_instrument = NoScrollQComboBox()
        self.comboBox_manufacturer.addItems(list(instrument_modules.keys()))
        self.comboBox_manufacturer.currentIndexChanged.connect(
            self.update_instrument_combobox
        )
        self.comboBox_instrument.currentIndexChanged.connect(
            self.update_driver_information
        )
        self.doclabel = QLabel()
        self.select_config_button = QPushButton("select configs / channels")

        self.current_info = {}
        self.config_info = {}

        self.layout().addWidget(label_manufacturer, 20, 0)
        self.layout().addWidget(self.comboBox_manufacturer, 20, 1)
        self.layout().addWidget(label_instrument, 20, 2)
        self.layout().addWidget(self.comboBox_instrument, 20, 3, 1, 2)
        self.layout().addWidget(self.doclabel, 21, 0, 1, 5)
        self.layout().addWidget(self.select_config_button, 22, 0, 1, 5)

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
            self.current_info = info
            self.config_info = {}
            self.select_configs()

    def select_configs(self):
        headerLabels = ["name", "is channel", "provide read (if channel)"]
        tableData = {}
        for key, value in self.current_info["controls"].items():
            tableData[key] = [key, False, True]
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
            self.config_info = config_selection.table.update_table_data()

        headerLabels = ["name", "is channel"]
        tableData = {}
        for key, value in self.current_info["settings"].items():
            tableData[key] = [key, False]
        config_selection = AddRemoveDialoge(
            headerLabels=headerLabels,
            editables=[],
            checkables=[1],
            tableData=tableData,
            title="Select set only as channels",
        )
        config_selection.table.addButton.setHidden(True)
        config_selection.table.removeButton.setHidden(True)
        if config_selection.exec():
            self.config_info = config_selection.table.update_table_data()

        self.update_config_selection()

    def update_config_selection(self):
        pass


class NoScrollQComboBox(QComboBox):
    def wheelEvent(self, event):
        # Ignore the event, effectively disabling mouse wheel scrolling
        event.ignore()
