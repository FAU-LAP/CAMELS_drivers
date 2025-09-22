from .mks_g_series_ophyd import MKS_G_Series
from nomad_camels.main_classes import device_class


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="mks_g_series",
            virtual=False,
            tags=[],
            ophyd_device=MKS_G_Series,
            ophyd_class_name="MKS_G_Series",
            **kwargs
        )


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
            "MKS G-Series",
            data,
            settings_dict,
            config_dict,
            additional_info,
        )
        self.comboBox_connection_type.addItem("Local VISA")
        self.load_settings()
        self.connector.set_only_resource_name()
