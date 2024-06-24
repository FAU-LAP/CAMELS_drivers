from .zurich_instruments_HDAWG_ophyd import Zurich_Instruments_Hdawg

from nomad_camels.main_classes import device_class
from nomad_camels.ui_widgets.path_button_edit import Path_Button_Edit


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="zurich_instruments_HDAWG",
            virtual=False,
            tags=["AWG", "zh"],
            directory="zurich_instruments_HDAWG",
            ophyd_device=Zurich_Instruments_Hdawg,
            ophyd_class_name="Zurich_Instruments_Hdawg",
            **kwargs
        )
        self.settings["device_id"] = "dev0000"
        self.settings["server_host"] = "127.0.0.1"
        self.settings["port"] = 8000
        self.settings["awg_index"] = 0
        # self.config["sequence_file"] = Path_Button_Edit


class subclass_config(device_class.Simple_Config):
    def __init__(
        self,
        parent=None,
        data="",
        settings_dict=None,
        config_dict=None,
        additional_info=None,
    ):
        labels = {
            "device_id": "Device ID",
            "server_host": "Server Host",
            "port": "Port",
            "awg_index": "AWG Index",
        }
        # We remove the sequence_file from the settings_dict and store it in a separate variable
        # This prevents us from having a double display of the path both as a settings field and a PathEditButton in the GUI 
        if "sequence_file" in settings_dict:
            sequence_file = settings_dict.pop("sequence_file")
        else:
            sequence_file = ""
        super().__init__(
            parent,
            "zurich_instruments_HDAWG",
            data,
            settings_dict,
            config_dict,
            additional_info,
            labels=labels,
        )
        self.settings_dict["sequence_file"] = sequence_file
        self.load_settings()

        # Path selection for file containing the sequence
        self.sequence_file_path = Path_Button_Edit()
        if "sequence_file" in settings_dict:
            self.sequence_file_path.line.setText(settings_dict["sequence_file"])
        self.layout().addWidget(self.sequence_file_path, 18, 0, 1, 5)

    def get_settings(self):
        self.settings_dict["sequence_file"] = self.sequence_file_path.get_path()
        return super().get_settings()
