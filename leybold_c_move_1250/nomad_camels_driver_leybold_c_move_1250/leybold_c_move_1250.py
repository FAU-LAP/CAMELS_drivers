from nomad_camels.main_classes import device_class

from .leybold_c_move_1250_ophyd import Leybold_C_Move_1250


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="leybold_c_move_1250",
            tags=["valve", "flow"],
            ophyd_device=Leybold_C_Move_1250,
            ophyd_class_name="Leybold_C_Move_1250",
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
            "Leybold C Move 1250",
            data,
            settings_dict,
            config_dict,
            additional_info,
        )
        self.comboBox_connection_type.addItem("Local VISA")
        self.load_settings()
