from nomad_camels_driver_trinamic_tmcm_1110.trinamic_tmcm_1110_ophyd import TMCM_1110, reference_search_modes, step_mode
from nomad_camels.main_classes import device_class

import pyvisa
from PySide6.QtWidgets import QLabel, QComboBox, QLineEdit, QCheckBox

class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(name='trinamic_tmcm_1110', virtual=False,
                         tags=['Function', 'Sine', 'Waveform', 'Generator', 'Voltage'],
                         ophyd_device=TMCM_1110,
                         ophyd_class_name='TMCM_1110', **kwargs)
        self.config['ref_search_mode'] = 'left switch'
        self.config['right_lim_switch_disable'] = True
        self.config['left_lim_switch_disable'] = True
        self.config['ref_search_speed'] = 100
        self.config['ref_switch_speed'] = 10
        self.config['max_acceleration'] = 100
        self.config['max_velocity'] = 100
        self.config['power_down_delay'] = 2000
        self.config['standby_current'] = 0
        self.config['max_current'] = 200
        self.config['freewheeling_delay'] = 2000
        self.config['pulse_divisor'] = 4
        self.config['ramp_divisor'] = 7
        self.config['soft_stop_flag'] = True
        self.config['microstep_resolution'] = '8 micro'
        self.settings['connection_port'] = ''
        self.settings['motor_number'] = 0
        self.settings['search_reference_on_start'] = True



class subclass_config(device_class.Simple_Config):
    """
    Automatically creates a GUI for the configuration values given here.
    This is perfect for simple devices with just a few settings.
    """
    def __init__(self, parent=None, data='', settings_dict=None,
                 config_dict=None, additional_info=None):
        rm = pyvisa.ResourceManager()
        ports = rm.list_resources()
        comboboxes = {'ref_search_mode': list(reference_search_modes.keys()),
                      'microstep_resolution': list(step_mode.keys()),
                      'connection_port': ports}
        super().__init__(parent, 'trinamic_tmcm_1110', data, settings_dict,
                         config_dict, additional_info, comboBoxes=comboboxes,
                         labels=None)
        self.load_settings()