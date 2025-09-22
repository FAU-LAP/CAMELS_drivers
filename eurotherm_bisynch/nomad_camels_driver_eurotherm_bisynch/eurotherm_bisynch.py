from .eurotherm_bisynch_ophyd import Eurotherm_Bisynch

from nomad_camels.main_classes import device_class


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="eurotherm_bisynch",
            virtual=False,
            tags=["function generator", "voltage", "frequency"],
            ophyd_device=Eurotherm_Bisynch,
            ophyd_class_name="Eurotherm_Bisynch",
            **kwargs
        )
        self.config['proportional_val'] = 0
        self.config['integral_val'] = 0
        self.config['derivative_val'] = 0
        self.config['max_output'] = 0


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
            "Eurotherm Bisynch",
            data,
            settings_dict,
            config_dict,
            additional_info,
        )
        self.comboBox_connection_type.addItem("Local VISA")
        self.load_settings()
        # self.connector.set_only_resource_name()
