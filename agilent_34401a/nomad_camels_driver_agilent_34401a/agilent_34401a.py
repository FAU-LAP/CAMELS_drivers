from .agilent_34401a_ophyd import Agilent_34401

from nomad_camels.main_classes import device_class

from PySide6.QtWidgets import QGridLayout, QLabel, QLineEdit


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="agilent_34401a",
            virtual=False,
            tags=["DMM", "voltage", "current"],
            ophyd_device=Agilent_34401,
            ophyd_class_name="Agilent_34401",
            **kwargs
        )
        self.config["nPLC"] = "1"


class subclass_config(device_class.Simple_Config):
    def __init__(
        self,
        parent=None,
        data="",
        settings_dict=None,
        config_dict=None,
        additional_info=None,
    ):
        comboboxes = {"nPLC": ["0.006", "0.02", "0.06", "0.2", "1", "2", "10", "100"]}
        super().__init__(
            parent,
            "Agilent 34401",
            data,
            settings_dict,
            config_dict,
            additional_info,
            comboBoxes=comboboxes,
        )
        self.comboBox_connection_type.addItem("Local VISA")
        # self.sub_widget = subclass_config_sub(config_dict=self.config_dict, parent=self)
        # self.layout().addWidget(self.sub_widget, 20, 0, 1, 5)
        self.load_settings()

    # def get_config(self):
    #     super().get_config()
    #     return self.sub_widget.get_config()


# class subclass_config_sub(device_class.Device_Config_Sub):
#     def __init__(self, config_dict=None, parent=None, settings_dict=None):
#         super().__init__(parent=parent, settings_dict=settings_dict,
#                          config_dict=config_dict)
#         self.config_dict = config_dict
#         layout = QGridLayout()
#         layout.setContentsMargins(0,0,0,0)
#         self.setLayout(layout)

#         label = QLabel('# PLC')
#         self.lineEdit_nPLC = QLineEdit('1')
#         if 'nPLC' in config_dict:
#             self.lineEdit_nPLC.setText(str(config_dict['nPLC']))

#         layout.addWidget(label, 0, 0)
#         layout.addWidget(self.lineEdit_nPLC, 0, 1)

#     def get_config(self):
#         self.config_dict['nPLC'] = float(self.lineEdit_nPLC.text())
#         return self.config_dict
