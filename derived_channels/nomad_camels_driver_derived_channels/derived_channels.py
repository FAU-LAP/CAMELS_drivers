from .derived_channels_ophyd import make_ophyd_class

from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QTabWidget,
    QCheckBox,
    QLabel,
    QLineEdit,
    QComboBox,
    QSpacerItem,
    QSplitter,
    QSizePolicy,
)

from nomad_camels.main_classes import device_class
from nomad_camels.utility import variables_handling
from nomad_camels.ui_widgets.channels_check_table import Channels_Check_Table
from nomad_camels.ui_widgets.add_remove_table import AddRemoveTable
from nomad_camels.ui_widgets.variable_tool_tip_box import Variable_Box


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="derived_channels",
            virtual=False,
            ophyd_device=None,
            ophyd_class_name="make_ophyd_instance_derived_channels",
            **kwargs,
        )
        self.settings["signal_info"] = {}
        self.main_thread_only = True

    def update_driver(self):
        signal_info = self.settings.get("signal_info", {})
        self.ophyd_class = make_ophyd_class(signal_info)
        self.ophyd_instance = self.ophyd_class(
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

    def get_necessary_devices(self):
        devices = []
        for signal in self.settings["signal_info"].values():
            for channel in signal.get("derived_from", []):
                dev = variables_handling.channels[channel].device
                if dev not in devices:
                    devices.append(dev)
        return devices


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
            "Derived Signals",
            data,
            settings_dict,
            config_dict,
            additional_info,
        )
        self.sub_widget = subclass_config_sub(
            settings_dict=settings_dict, parent=self, config_dict=config_dict
        )
        self.sub_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout().addWidget(self.sub_widget, 5, 0, 1, 5)
        self.load_settings()

    def get_settings(self):
        return self.sub_widget.get_settings()

    def get_config(self):
        return self.sub_widget.get_config()


class subclass_config_sub(QSplitter):
    def __init__(self, settings_dict=None, parent=None, config_dict=None):
        super().__init__(parent)

        self.signal_info = settings_dict.get("signal_info", {})
        table_data = {"Channel Name": list(self.signal_info.keys())}
        self.signal_table = AddRemoveTable(
            tableData=table_data,
            parent=self,
            headerLabels=["Channel Name"],
        )

        self.signal_tabs = QTabWidget(self)

        self.addWidget(self.signal_table)
        self.addWidget(self.signal_tabs)
        self.build_tabs()
        self.last_signal_names = list(self.signal_info.keys())

        self.signal_table.table_model.itemChanged.connect(self.build_tabs)
        self.signal_table.removed.connect(self.build_tabs)

    def build_tabs(self, item=None):
        if item is not None:
            if isinstance(item, int):
                name = self.signal_tabs.tabText(item)
                if name in self.signal_info:
                    self.signal_info.pop(name)
            else:
                signal_name = item.text()
                if signal_name not in self.signal_info:
                    self.signal_info[signal_name] = {
                        "derived_from": [],
                        "write_access": False,
                        "description": "",
                        "unit": "",
                        "read_formula": "",
                        "write_formula": "",
                    }
                # get position of the signal in the table
                position = item.row()
                if position < len(self.last_signal_names):
                    old_name = self.last_signal_names[position]
                    if old_name != signal_name and old_name in self.signal_info:
                        self.signal_info[signal_name] = self.signal_info[old_name]
                        self.signal_info.pop(old_name)
        self.signal_tabs.clear()
        for signal_name, signal_info in self.signal_info.items():
            tab = Signal_Tab(signal_info=signal_info)
            self.signal_tabs.addTab(tab, signal_name)
        self.last_signal_names = list(self.signal_info.keys())

    def get_config(self):
        return {}

    def get_settings(self):
        signal_info = {}
        for i in range(self.signal_tabs.count()):
            tab = self.signal_tabs.widget(i)
            signal_name = self.signal_tabs.tabText(i)
            signal_info[signal_name] = tab.get_info()
        return {"signal_info": signal_info}


class Signal_Tab(QWidget):
    def __init__(self, signal_info=None, parent=None):
        super().__init__(parent)
        layout = QGridLayout(self)
        self.setLayout(layout)

        self.check_writable = QCheckBox("Writeable")
        self.check_writable.setChecked(signal_info.get("write_access", False))
        self.check_writable.stateChanged.connect(self.read_write_changed)
        self.label_read_formula = QLabel("Calculation Formula:")
        self.label_write_formula = QLabel("Calculation Formula:")
        self.label_description = QLabel("Description:")
        self.label_unit = QLabel("Unit:")
        self.label_write_channel = QLabel("Write Channel:")

        self.read_formula = Variable_Box()
        self.read_formula.setText(signal_info.get("read_formula", ""))
        self.write_formula = QLineEdit()
        self.write_formula.setText(signal_info.get("write_formula", ""))
        self.description = QLineEdit(signal_info.get("description", ""))
        self.unit = QLineEdit(signal_info.get("unit", ""))

        self.write_channel_combo = QComboBox()
        self.write_channel_combo.addItems(
            list(variables_handling.get_output_channels())
        )
        write_tooltip = "The calculated value will be written to this channel."
        self.label_write_channel.setToolTip(write_tooltip)
        self.write_channel_combo.setToolTip(write_tooltip)
        self.write_formula.setToolTip(
            'How to calculate the output value. Use "x" for the input value.\nExample: "x * 2" will double the input value.'
        )

        channels = signal_info.get("derived_from", [])
        if len(channels) == 1:
            self.write_channel_combo.setCurrentText(channels[0])

        info_dict = {"channel": channels}
        self.channel_table = Channels_Check_Table(
            parent=self,
            headerLabels=["read?", "channel"],
            use_aliases=False,
            info_dict=info_dict,
        )
        self.spacer = QSpacerItem(
            0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.read_write_changed()

        layout.addWidget(self.check_writable, 0, 0, 1, 2)
        layout.addWidget(self.label_read_formula, 1, 0)
        layout.addWidget(self.read_formula, 1, 1)
        layout.addWidget(self.label_write_formula, 2, 0)
        layout.addWidget(self.write_formula, 2, 1)
        layout.addWidget(self.label_description, 3, 0)
        layout.addWidget(self.description, 3, 1)
        layout.addWidget(self.label_unit, 4, 0)
        layout.addWidget(self.unit, 4, 1)
        layout.addWidget(self.label_write_channel, 5, 0)
        layout.addWidget(self.write_channel_combo, 5, 1)
        layout.addWidget(self.channel_table, 10, 0, 1, 2)
        layout.addItem(self.spacer, 15, 0, 1, 2)

    def read_write_changed(self):
        writable = self.check_writable.isChecked()
        self.read_formula.setHidden(writable)
        self.label_read_formula.setHidden(writable)
        self.write_formula.setHidden(not writable)
        self.label_write_formula.setHidden(not writable)
        self.channel_table.setHidden(writable)
        self.write_channel_combo.setHidden(not writable)
        self.label_write_channel.setHidden(not writable)

    def get_info(self):
        """
        Collects the information from the tab and returns it as a dictionary.
        """
        writable = self.check_writable.isChecked()
        info = {
            "write_access": writable,
            "read_formula": self.read_formula.text(),
            "write_formula": self.write_formula.text(),
            "description": self.description.text(),
            "unit": self.unit.text(),
        }
        if not writable:
            info["derived_from"] = self.channel_table.get_info()["channel"]
        else:
            info["derived_from"] = [self.write_channel_combo.currentText()]
        return info


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
