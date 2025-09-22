from .epics_instrument_ophyd import make_ophyd_class

from nomad_camels.main_classes import device_class
from nomad_camels.ui_widgets.add_remove_table import AddRemoveTable


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="epics_instrument",
            virtual=False,
            tags=[
                "epics",
            ],
            directory="epics_instrument",
            ophyd_device=None,
            ophyd_class_name="make_ophyd_instance_epics",
            **kwargs,
        )

    def update_driver(self):
        if "pvs" not in self.settings or not self.settings["pvs"]:
            return

        pvs = self.settings["pvs"]
        self.ophyd_class = make_ophyd_class(pvs)
        self.ophyd_instance = self.ophyd_class(
            pvs,
            name="test",
        )
        config, passive_config = get_configs_from_ophyd(self.ophyd_instance)
        for key, value in config.items():
            if key not in self.config:
                self.config[key] = value
        for key, value in passive_config.items():
            if key not in self.passive_config:
                self.passive_config[key] = value

    def get_channels(self):
        self.update_driver()
        return super().get_channels()


class subclass_config(device_class.Device_Config):
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
            "epics_instrument",
            data,
            settings_dict,
            config_dict,
            additional_info,
        )
        pv_info = [
            "PV Short Name",
            "PV Full Name",
            "PV-Type",
            "Unit",
            "Description",
        ]
        comboboxes = {
            "PV-Type": [
                "read-only",
                "set",
            ],
        }
        if "pvs" not in self.settings_dict:
            self.settings_dict["pvs"] = {}

        # Table for adding and removing EPICS PVs
        self.pv_table = AddRemoveTable(
            headerLabels=pv_info,
            comboBoxes=comboboxes,
            tableData=self.settings_dict["pvs"],
        )
        self.layout().addWidget(self.pv_table, 30, 0, 1, 5)
        self.load_settings()

    def get_settings(self):
        self.settings_dict["pvs"] = self.pv_table.update_table_data()
        return super().get_settings()


def get_configs_from_ophyd(ophyd_instance):
    config = {}
    passive_config = {}
    for comp in ophyd_instance.walk_components():
        name = comp.item.attr
        dev_class = comp.item.cls
        if name in ophyd_instance.configuration_attrs:
            if device_class.check_output(dev_class):
                config.update({f"{name}": 0})
            else:
                passive_config.update({f"{name}": 0})
    return config, passive_config
