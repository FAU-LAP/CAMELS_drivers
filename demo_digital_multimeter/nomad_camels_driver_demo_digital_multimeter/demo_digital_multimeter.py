from nomad_camels_driver_demo_digital_multimeter.demo_digital_multimeter_ophyd import (
    Demo_DMM,
)

from nomad_camels.main_classes import device_class
from nomad_camels_sandbox.server_signals import ServerConnection


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="demo_digital_multimeter",
            virtual=False,
            tags=["DMM", "voltage", "current", "resistance"],
            ophyd_device=Demo_DMM,
            ophyd_class_name="Demo_DMM",
            **kwargs
        )
        self.config["NPLC"] = 1


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
            parent, "SandboxForCAMELS Demo Digital Multimeter", data, settings_dict, config_dict, additional_info
        )
        self.comboBox_connection_type.addItem("Local VISA")
        self.load_settings()

    def connection_type_changed(self):
        conn_old = self.connector
        self.connector = ServerConnection()
        self.connector.load_settings(self.settings_dict)
        self.layout().replaceWidget(conn_old, self.connector)
        conn_old.deleteLater()
