from nomad_camels.main_classes import device_class
from .demo_source_measure_unit_ophyd import Demo_SMU

from nomad_camels_sandbox.server_signals import ServerConnection
from nomad_camels_sandbox.digitaltwins.experiment import all_experiments


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
        self.config["compliance_1"] = 0.1
        self.config["compliance_2"] = 0.1
        self.settings["experiment"] = "diode_on_heater"


class subclass_config(device_class.Simple_Config):
    def __init__(
        self,
        parent=None,
        data="",
        settings_dict=None,
        config_dict=None,
        additional_info=None,
    ):
        comboBoxes = {"experiment": all_experiments}
        labels = {
            "NPLC1": "NPLC channel 1",
            "NPLC2": "NPLC channel 2",
            "compliance_1": "Compliance channel 1",
            "compliance_2": "Compliance channel 2",
        }
        super().__init__(
            parent,
            "SandboxForCAMELS Demo Source-Measure Unit",
            data,
            settings_dict,
            config_dict,
            additional_info,
            labels=labels,
            comboBoxes=comboBoxes,
        )

    def connection_type_changed(self):
        conn_old = self.connector
        self.connector = ServerConnection()
        self.connector.load_settings(self.settings_dict)
        self.layout().replaceWidget(conn_old, self.connector)
        conn_old.deleteLater()
