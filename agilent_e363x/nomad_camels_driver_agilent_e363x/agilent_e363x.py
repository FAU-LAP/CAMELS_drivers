from .agilent_e363x_ophyd import Agilent_E363X

from nomad_camels.main_classes import device_class


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(name='agilent_e363x', virtual=False,
                         tags=['Power Supply', 'voltage', 'current'],
                         ophyd_device=Agilent_E363X,
                         ophyd_class_name='Agilent_E363X', **kwargs)
        self.config['current_limit_1'] = 0
        self.config['current_limit_2'] = 0
        self.config['current_limit_3'] = 0


class subclass_config(device_class.Simple_Config):
    def __init__(self, parent=None, data='', settings_dict=None,
                 config_dict=None, additional_info=None):
        super().__init__(parent, 'Agilent E363X', data, settings_dict,
                         config_dict, additional_info)
        self.comboBox_connection_type.addItem('Local VISA')
        self.load_settings()
        self.connector.set_only_resource_name()
