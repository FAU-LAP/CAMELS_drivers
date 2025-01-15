from .opc_ua_instrument_ophyd import make_ophyd_class

from nomad_camels.main_classes import device_class
from nomad_camels.ui_widgets.add_remove_table import AddRemoveTable
from PySide6.QtWidgets import QLabel, QLineEdit


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="opc_ua_instrument",
            virtual=False,
            tags=["opc", "ua"],
            directory="opc_ua_instrument",
            ophyd_device=None,
            ophyd_class_name="make_ophyd_instance",
            **kwargs,
        )

    def update_driver(self):
        if "variables" not in self.settings or not self.settings["variables"]:
            return

        if "Browse Path" in self.settings["variables"] and any(
            bp == "" for bp in self.settings["variables"]["Browse Path"]
        ):
            raise ValueError(
                "A Browse Path is required for each variable. It should look something like '0:Objects/2:MyObject/2:MyVariable'"
            )

        variables = self.settings["variables"]
        self.ophyd_class = make_ophyd_class(variables)
        self.ophyd_instance = self.ophyd_class(
            variables,
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
            "opc_ua_instrument",
            data,
            settings_dict,
            config_dict,
            additional_info,
        )
        variable_info = [
            "Name",
            "variable-Type",
            "Browse Path",
            "Unit",
            "Description",
        ]
        comboboxes = {
            "variable-Type": [
                "read-only",
                "set",
            ],
        }
        if "variables" not in self.settings_dict:
            self.settings_dict["variables"] = {}

        if "url" not in self.settings_dict:
            self.settings_dict["url"] = "opc.tcp://localhost:4840/freeopcua/server/"
        if "namespace" not in self.settings_dict:
            self.settings_dict["namespace"] = "http://examples.freeopcua.github.io"

        # Label and line edit for the OPC UA server URL
        self.url_label = QLabel("URL:")
        self.url_line_edit = QLineEdit(self.settings_dict["url"])

        # Label and line edit for the OPC UA server namespace
        self.namespace_label = QLabel("Namespace:")
        self.namespace_line_edit = QLineEdit(self.settings_dict["namespace"])

        # Load the settings into the widgets
        # Table for adding and removing OPC UA variables
        self.variable_table = AddRemoveTable(
            headerLabels=variable_info,
            comboBoxes=comboboxes,
            tableData=self.settings_dict["variables"],
        )
        self.url_line_edit.setText(self.settings_dict["url"])
        self.namespace_line_edit.setText(self.settings_dict["namespace"])

        self.layout().addWidget(self.url_label, 20, 0)
        self.layout().addWidget(self.url_line_edit, 20, 1)
        self.layout().addWidget(self.namespace_label, 21, 0)
        self.layout().addWidget(self.namespace_line_edit, 21, 1)
        self.layout().addWidget(self.variable_table, 30, 0, 1, 5)
        self.load_settings()

    def get_settings(self):
        self.settings_dict["variables"] = self.variable_table.update_table_data()
        self.settings_dict["url"] = self.url_line_edit.text()
        self.settings_dict["namespace"] = self.namespace_line_edit.text()
        return super().get_settings()


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
