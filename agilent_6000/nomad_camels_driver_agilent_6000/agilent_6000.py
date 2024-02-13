from .agilent_6000_ophyd import Agilent_6000, waveform_functions, meas_sources

from nomad_camels.main_classes import device_class
from .agilent_6000_manual_control import Agilent_6000_Manual_Control, Agilent_6000_Manual_Control_Config



class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(name='agilent_6000', virtual=False,
                         tags=['oscilloscope', 'voltage', 'current'],
                         ophyd_device=Agilent_6000,
                         ophyd_class_name='Agilent_6000',
                         non_channel_functions=['disable_front_panel', 'enable_front_panel'],
                         **kwargs)
        self.config['invert_colors'] = False
        self.config['grayscale'] = False
        self.config['image_type'] = 'png'
        self.config['acquisition_type'] = 'normal'
        self.config['n_averages'] = 8
        self.config['timebase_offset'] = 0
        self.config['trigger_mode'] = 'normal'

        self.config['ac_coupling_1'] = False
        self.config['ac_coupling_2'] = False
        self.config['ac_coupling_3'] = False
        self.config['ac_coupling_4'] = False
        self.config['probe_attenuation_1'] = 10
        self.config['probe_attenuation_2'] = 10
        self.config['probe_attenuation_3'] = 10
        self.config['probe_attenuation_4'] = 10

        self.config['waveform_meas_source'] = 'channel 1'
        self.config['waveform_meas_source_2'] = 'none'
        self.config['waveform_meas_function'] = 'frequency'

        self.controls = {'Agilent_6000_Manual_Control': [Agilent_6000_Manual_Control, Agilent_6000_Manual_Control_Config]}

class subclass_config(device_class.Simple_Config):
    def __init__(self, parent=None, data='', settings_dict=None,
                 config_dict=None, additional_info=None):
        comboboxes = {'image_type': ['png', 'bmp'],
                      'acquisition_type': ['normal', 'average', 'peak_detect', 'high_resolution'],
                      'trigger_mode': ['normal', 'auto'],
                      'waveform_meas_source': list(meas_sources.keys()),
                      'waveform_meas_source_2': list(meas_sources.keys()) + ["none"],
                      'waveform_meas_function': list(waveform_functions.keys())}
        super().__init__(parent, 'Agilent 6000', data, settings_dict,
                         config_dict, additional_info, comboBoxes=comboboxes)
        self.comboBox_connection_type.addItem('Local VISA')
        self.load_settings()
