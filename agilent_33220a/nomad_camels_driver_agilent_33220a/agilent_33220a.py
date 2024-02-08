from .agilent_33220a_ophyd import Agilent_33220A

from nomad_camels.main_classes import device_class


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(name='agilent_33220a', virtual=False,
                         tags=['function generator', 'voltage', 'frequency'],
                         ophyd_device=Agilent_33220A,
                         ophyd_class_name='Agilent_33220A', **kwargs)
        self.config['amplitude_unit'] = 'VPP'
        self.config['waveform'] = 'sinusoid'
        self.config['output_impedance'] = '50'


class subclass_config(device_class.Simple_Config):
    def __init__(self, parent=None, data='', settings_dict=None,
                    config_dict=None, additional_info=None):
            comboboxes = {'amplitude_unit': ['VPP', 'VRMS', 'DBM'],
                        'waveform': ['sinusoid', 'square', 'ramp', 'pulse', 'noise', 'dc', 'triangle',
                                     'sinc', 'negative ramp', 'exponential rise', 'exponential fall', 'cardiac'],
                        'output_impedance': ['50', 'highZ'],}
            super().__init__(parent, 'Agilent 33220A', data, settings_dict,
                            config_dict, additional_info, comboBoxes=comboboxes)
            self.comboBox_connection_type.addItem('Local VISA')
            self.load_settings()
            self.connector.set_only_resource_name()

