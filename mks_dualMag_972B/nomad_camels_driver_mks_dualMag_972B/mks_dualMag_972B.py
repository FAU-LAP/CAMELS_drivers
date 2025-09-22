from .mks_dualMag_972B_ophyd import MKS_DualMag_972B, pressure_units, gas_types
from nomad_camels.main_classes import device_class


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="mks_dualMag_972B",
            virtual=False,
            tags=[],
            ophyd_device=MKS_DualMag_972B,
            ophyd_class_name="MKS_DualMag_972B",
            **kwargs
        )
        self.config["pressure_unit"] = "mBar"
        self.config["gas_type"] = "Argon"


class subclass_config(device_class.Simple_Config):
    def __init__(
        self,
        parent=None,
        data="",
        settings_dict=None,
        config_dict=None,
        additional_info=None,
    ):
        comboboxes = {
            "pressure_unit": pressure_units.keys(),
            "gas_type": gas_types.keys(),
        }
        super().__init__(
            parent,
            "MKS DualMag 972B",
            data,
            settings_dict,
            config_dict,
            additional_info,
            comboBoxes=comboboxes,
        )
        self.comboBox_connection_type.addItem("Local VISA")
        self.load_settings()
        self.connector.set_only_resource_name()
