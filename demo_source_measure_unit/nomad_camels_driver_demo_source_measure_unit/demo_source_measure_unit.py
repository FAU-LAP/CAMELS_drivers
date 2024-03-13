from nomad_camels.main_classes import device_class
from .demo_source_measure_unit_ophyd import Demo_SMU

import sys

sys.path.append(r"C:\Users\od93yces\FAIRmat")
sys.path.append(r"C:\Users\od93yces\FAIRmat\CAMELS_sandbox")
sys.path.append(r"C:\Users\od93yces\FAIRmat\CAMELS_sandbox\CAMELS_sandbox")
from nomad_camels_sandbox.server_signals import ServerConnection


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="demo_source_measure_unit",
            virtual=False,
            tags=["SMU", "voltage", "current", "resistance"],
            ophyd_device=Demo_SMU,
            ophyd_class_name="Demo_SMU",
            **kwargs,
        )
        self.config["NPLC1"] = 1
        self.config["NPLC2"] = 1


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
            "Keysight B2912A",
            data,
            settings_dict,
            config_dict,
            additional_info,
        )

    def connection_type_changed(self):
        conn_old = self.connector
        self.connector = ServerConnection()
        self.connector.load_settings(self.settings_dict)
        self.layout().replaceWidget(conn_old, self.connector)
        conn_old.deleteLater()
