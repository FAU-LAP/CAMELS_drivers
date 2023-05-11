from nomad_camels_driver_instrument_name.instrument_name_ophyd import instrument_name
from nomad_camels.main_classes import device_class

class subclass(device_class.Device):
    def __init__(self, **kwargs):
        files = []
        req = []
        super().__init__(name='instrument_name', virtual=False,
                         tags=['Function', 'Sine', 'Waveform', 'Generator', 'Voltage'],
                         directory='instrument_name',
                         ophyd_device=instrument_name,
                         ophyd_class_name='instrument_name', **kwargs)



class subclass_config(device_class.Simple_Config):
    def __init__(self, parent=None, data='', settings_dict=None,
                 config_dict=None, ioc_dict=None, additional_info=None):
        super().__init__(parent, 'instrument name', data, settings_dict,
                         config_dict, ioc_dict, additional_info)
        self.comboBox_connection_type.addItem('Local VISA')
        self.load_settings()
