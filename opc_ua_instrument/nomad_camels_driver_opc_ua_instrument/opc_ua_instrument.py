from .opc_ua_instrument_ophyd import make_ophyd_class

from nomad_camels.main_classes import device_class
from nomad_camels.ui_widgets.add_remove_table import AddRemoveTable
from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox

# For variable node discovery
import re
from asyncua.sync import Client
from asyncua import ua
from asyncua import Node, Client as OPCUAClient


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="opc_ua_instrument",
            virtual=False,
            tags=["opc", "ua"],
            directory="opc_ua_instrument",
            ophyd_device=None,
            ophyd_class_name="make_ophyd_instance_opc_ua",
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
        self.url_line_edit.setToolTip(
            "Enter the URL of the OPC UA server. The default is 'opc.tcp://localhost:4840/freeopcua/server/'."
        )

        # Label and line edit for the OPC UA server namespace
        self.namespace_label = QLabel("Namespace:")
        self.namespace_line_edit = QLineEdit(self.settings_dict["namespace"])
        self.namespace_line_edit.setToolTip(
            "Enter the namespace of the OPC UA server. The default is 'http://examples.freeopcua.github.io'."
        )

        # Add button and texteditfield. When button is pressed all opc ua variables matching the text of the texteditfield are added to the table
        self.search_label = QLabel("Search fro variables:")
        self.search_line_edit = QLineEdit()
        self.search_line_edit.setToolTip(
            "Enter a regex pattern to search for variables. Variables that match the pattern will be added to the table below."
        )
        self.search_button = QPushButton("Fetch and Add")
        self.search_button.setToolTip(
            "Connect to the OPC UA server and add variables that match the search string to the list below."
        )

        # Connect button to the method that fetches variables and adds them to the table
        self.search_button.clicked.connect(self.add_matching_variables)

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

        # Place the "Search variables" field and button
        self.layout().addWidget(self.search_label, 22, 0)
        self.layout().addWidget(self.search_button, 22, 1)
        self.layout().addWidget(self.search_line_edit, 22, 2)

        self.layout().addWidget(self.variable_table, 50, 0, 1, 5)
        self.load_settings()

    def get_settings(self):
        self.settings_dict["variables"] = self.variable_table.update_table_data()
        self.settings_dict["url"] = self.url_line_edit.text()
        self.settings_dict["namespace"] = self.namespace_line_edit.text()
        return super().get_settings()

    def discover_opc_variables(
        self,
        node: Node,
        client: OPCUAClient,
        results=None,
        path: str = "",
        regex_pattern: str = ".*",
    ) -> dict[str, str]:
        if results is None:
            results = {}
        # Get the display name or node id
        display_name = node.read_browse_name().to_string()
        node_id = node.nodeid.to_string()

        # Check if the node is a variable
        current_path = f"{path}/{display_name}" if path else display_name

        if node.read_node_class() == 2:
            # Build the current node path
            print(
                f"Node ID: {node_id}, Path: {current_path}, class: {node.read_node_class()}"
            )
            if re.search(regex_pattern, current_path) or re.search(
                regex_pattern, node_id
            ):
                results[current_path] = node_id
                print("Found variable!", "!" * 25)
                print(
                    f"Node ID: {node_id}, Path: {current_path}, class: {node.read_node_class()}"
                )

        # Get the children of the current node
        children = node.get_children()
        for child in children:
            self.discover_opc_variables(
                child, client, results, current_path, regex_pattern
            )

        return results

    def add_matching_variables(self):
        """
        2) When "Fetch and Add" is clicked, connect to the OPC UA server (using
           the URL and namespace from the line edits), find any variables
           matching the search string, and add them to the table.
        """
        search_text = self.search_line_edit.text().strip()
        if not search_text:
            QMessageBox.warning(self, "No Search Text", "Please enter text to search.")
            return

        opc_url = self.url_line_edit.text().strip()
        # Connect to the OPC UA server
        client = Client(url=opc_url)
        client.connect()

        found_variables = self.discover_opc_variables(
            node=client.nodes.objects, client=client, regex_pattern=search_text
        )

        if not found_variables:
            QMessageBox.information(
                self,
                "No Matches",
                "No variables found. Make sure your pattern is correct.",
            )
            return

        # Add found variables to the table
        for var in found_variables:
            # var is with its key being the browse path and the value being the node id. We want to add the browse path to the table.
            self.variable_table.add(["", "read-only", var, "", ""])


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
