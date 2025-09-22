from .agilent_81101a_puls_generator_ophyd import Agilent_81101A_Puls_Generator

from nomad_camels.main_classes import device_class


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="agilent_81101a_puls_generator",
            virtual=False,
            tags=["puls", "generator"],
            directory="agilent_81101a_puls_generator",
            ophyd_device=Agilent_81101A_Puls_Generator,
            ophyd_class_name="Agilent_81101A_Puls_Generator",
            **kwargs
        )
        self.config["set_puls_amplitude"] = 2.5
        self.config["set_puls_offset"] = 0
        self.config["set_puls_transition"] = 6


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
            "set_puls_amplitude": "Pulse Amplitude in V",
            "set_puls_offset": "Pulse Offset in V",
            "set_puls_transition": "Pulse transition in ns",
        }
        super().__init__(
            parent,
            "agilent_81101a_puls_generator",
            data,
            settings_dict,
            config_dict,
            additional_info,
            labels=labels,
        )
        self.comboBox_connection_type.addItem("Local VISA")
        self.load_settings()
