from .openCV_generic_ophyd import Opencv_Generic

from nomad_camels.main_classes import device_class


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="openCV_generic",
            virtual=False,
            tags=[],
            directory="openCV_generic",
            ophyd_device=Opencv_Generic,
            ophyd_class_name="Opencv_Generic",
            **kwargs,
        )
        self.settings["camera_index"] = 0


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
            parent, "openCV_generic", data, settings_dict, config_dict, additional_info
        )
        self.load_settings()
