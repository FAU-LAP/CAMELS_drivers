from nomad_camels_driver_keithley_2000.keithley_2000_ophyd import Keithley_2000

from nomad_camels.main_classes import device_class

class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(name='keithley_2000', virtual=False,
                         tags=['DMM', 'voltage', 'current', 'resistance'],
                         ophyd_device=Keithley_2000,
                         ophyd_class_name='Keithley_2000', **kwargs)
        self.config['NPLC'] = 1



class subclass_config(device_class.Simple_Config):
    def __init__(self, parent=None, data='', settings_dict=None,
                 config_dict=None, additional_info=None):
        super().__init__(parent, 'Keithley 2000', data, settings_dict,
                         config_dict, additional_info)
        self.comboBox_connection_type.addItem('Local VISA')
        self.load_settings()
