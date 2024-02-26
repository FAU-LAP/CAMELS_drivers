from .mechonics_cu30cl_ophyd import Mechonics_CU30CL
from nomad_camels.main_classes import device_class


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="mechonics_cu30cl",
            virtual=False,
            tags=["Stage"],
            ophyd_device=Mechonics_CU30CL,
            ophyd_class_name="Mechonics_CU30CL",
            non_channel_functions=[
                "find_reference",
                "stop_movement",
                "manual_move_start_x",
                "manual_move_start_y",
                "manual_move_start_z",
            ],
            **kwargs
        )
        self.config["speed_x"] = 100
        self.config["speed_y"] = 100
        self.config["speed_z"] = 100
        self.config["resolution_x"] = 0.02
        self.config["resolution_y"] = 0.02
        self.config["resolution_z"] = 0.02
        self.config["orientation_x"] = 0
        self.config["orientation_y"] = 0
        self.config["orientation_z"] = 0
        self.config["timeconstant"] = 200

        self.settings["ax_X"] = True
        self.settings["ax_Y"] = True
        self.settings["ax_Z"] = True
        self.settings["threshold_x"] = 3
        self.settings["threshold_y"] = 3
        self.settings["threshold_z"] = 3
        self.settings["time_threshold_x"] = 5
        self.settings["time_threshold_y"] = 5
        self.settings["time_threshold_z"] = 5

    def get_settings(self):
        settings = dict(super().get_settings())
        removes = []
        rmX = "ax_X" not in settings or not settings["ax_X"]
        rmY = "ax_Y" not in settings or not settings["ax_Y"]
        rmZ = "ax_Z" not in settings or not settings["ax_Z"]
        for key in settings:
            if (rmX and "x" in key) or (rmY and "y" in key) or (rmZ and "z" in key):
                removes.append(key)
        for r in removes:
            settings.pop(r)
        return settings

    def get_config(self):
        settings = self.get_settings()
        config_dict = dict(super().get_config())
        removes = []
        rmX = "ax_X" not in settings or not settings["ax_X"]
        rmY = "ax_Y" not in settings or not settings["ax_Y"]
        rmZ = "ax_Z" not in settings or not settings["ax_Z"]
        for key in config_dict:
            if (rmX and "x" in key) or (rmY and "y" in key) or (rmZ and "z" in key):
                removes.append(key)
        for r in removes:
            config_dict.pop(r)
        return config_dict

    def get_channels(self):
        channels = dict(super().get_channels())
        settings = self.get_settings()
        removes = []
        rmX = "ax_X" not in settings or not settings["ax_X"]
        rmY = "ax_Y" not in settings or not settings["ax_Y"]
        rmZ = "ax_Z" not in settings or not settings["ax_Z"]
        for key in channels:
            if (rmX and "x" in key) or (rmY and "y" in key) or (rmZ and "z" in key):
                removes.append(key)
        for r in removes:
            channels.pop(r)
        return channels


class subclass_config(device_class.Simple_Config):
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
            "Mechonics CU30CL",
            data,
            settings_dict,
            config_dict,
            additional_info,
        )
        self.load_settings()
