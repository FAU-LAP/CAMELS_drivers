from .openCV_instrument_ophyd import OpenCV_Instrument

from nomad_camels.main_classes import device_class


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="openCV_instrument",
            virtual=False,
            tags=[],
            directory="openCV_instrument",
            ophyd_device=OpenCV_Instrument,
            ophyd_class_name="OpenCV_Instrument",
            **kwargs,
        )
        self.settings["camera_index"] = 0
        self.settings["display_image"] = True


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
            parent, "openCV_instrument", data, settings_dict, config_dict, additional_info
        )
        self.load_settings()
