from .ADALM1000_ophyd import Adalm1000

from nomad_camels.main_classes import device_class


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="ADALM1000",
            virtual=False,
            tags=["SMU"],
            directory="ADALM1000",
            ophyd_device=Adalm1000,
            ophyd_class_name="Adalm1000",
            **kwargs
        )
        self.config["device_number"] = "0"
        self.config["n_samples"] = 100001
        self.main_thread_only = True


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
            "device_number": "Device number",
            "n_samples": "Number of samples",
        }
        super().__init__(
            parent,
            "ADALM1000",
            data,
            settings_dict,
            config_dict,
            additional_info,
            labels=labels,
        )
        self.load_settings()
