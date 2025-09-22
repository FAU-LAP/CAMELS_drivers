from PySide6.QtWidgets import QLabel, QLineEdit


from nomad_camels.main_classes import device_class
from nomad_camels.ui_widgets.add_remove_table import AddRemoveTable
from nomad_camels.ui_widgets.path_button_edit import Path_Button_Edit

from .labview_cryo_ophyd import make_ophyd_class


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="labview_cryo",
            virtual=False,
            tags=[],
            directory="labview_cryo",
            ophyd_device=None,
            ophyd_class_name="make_ophyd_instance_labview_cryo",
            **kwargs,
        )
        self.main_thread_only = True

    def update_driver(self):
        if "variables" not in self.settings or not self.settings["variables"]:
            return

        variables = self.settings["variables"]
        self.ophyd_class = make_ophyd_class(variables)
        self.ophyd_instance = self.ophyd_class(
            # variables,
            name="test",
        )

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
            "labview_cryo",
            data,
            settings_dict,
            config_dict,
            additional_info,
        )
        table_data = {
            "varaible_name": settings_dict.get("variables", []),
        }
        self.variables_table = AddRemoveTable(
            headerLabels=["varaible_name"], tableData=table_data, title="Variables"
        )
        self.variables_table.setToolTip(
            "Make sure to define the variables in the order they appear in the file."
        )

        self.file_name_label = QLabel("File Name:")
        self.file_name_input = Path_Button_Edit(
            path=self.settings_dict.get("file_name", "")
        )
        self.delimiter_label = QLabel("Delimiter:")
        self.delimiter_input = QLineEdit(text=self.settings_dict.get("delimiter", ","))

        self.layout().addWidget(self.file_name_label, 10, 0)
        self.layout().addWidget(self.file_name_input, 10, 1)
        self.layout().addWidget(self.delimiter_label, 11, 0)
        self.layout().addWidget(self.delimiter_input, 11, 1)
        self.layout().addWidget(self.variables_table, 12, 0, 1, 2)

    def get_settings(self):
        self.settings_dict["file_name"] = self.file_name_input.get_path()
        self.settings_dict["delimiter"] = self.delimiter_input.text()
        self.settings_dict["variables"] = self.variables_table.update_table_data()[
            "varaible_name"
        ]
        return super().get_settings()
