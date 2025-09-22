from .picoquant_TRPL_ophyd import Picoquant_TRPL

from nomad_camels.main_classes import device_class


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="picoquant_TRPL",
            virtual=False,
            tags=[],
            ophyd_device=Picoquant_TRPL,
            ophyd_class_name="Picoquant_TRPL",
            **kwargs
        )
        self.settings["meas_mode"] = "Histogram"
        self.config["acquisition_time"] = 1
        self.config["sync_edge"] = 1
        self.config["sync_level"] = -300
        self.config["sync_offset"] = 0
        self.config["chan1_edge"] = 1
        self.config["chan1_level"] = -120
        self.config["chan1_offset"] = 0
        self.config["resolution"] = 1e-9
        self.config["chan_stop"] = 5


class subclass_config(device_class.Simple_Config):
    def __init__(
        self,
        parent=None,
        data="",
        settings_dict=None,
        config_dict=None,
        additional_info=None,
    ):
        comboboxes = {"meas_mode": ["Histogram", "T2", "T3"]}
        super().__init__(
            parent,
            "Picoquant TRPL",
            data,
            settings_dict,
            config_dict,
            additional_info,
            comboBoxes=comboboxes,
        )
        self.load_settings()
