from nomad_camels_driver_pi_stage_e709.pi_stage_e709_ophyd import PI_E709, get_available_stages
from nomad_camels.main_classes import device_class

from PySide6.QtWidgets import QLabel, QComboBox

class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(name='pi_stage_e709', virtual=False,
                         # Change the tags to fit your device
                         tags=['Function', 'Sine', 'Waveform', 'Generator', 'Voltage'],
                         ophyd_device=PI_E709,
                         ophyd_class_name='PI_E709', **kwargs)
        self.settings['autozero_on_start'] = True
        self.settings['resource'] = ''
        self.config['servo_on'] = True



class subclass_config(device_class.Simple_Config):
    """
    Automatically creates a GUI for the configuration values given here.
    This is perfect for simple devices with just a few settings.
    """
    def __init__(self, parent=None, data='', settings_dict=None,
                 config_dict=None, additional_info=None):
        # sub_set = dict(settings_dict)
        # sub_set.pop('resource')
        stages = get_available_stages()
        if not stages:
            stages = ['No stage found!']
        comboboxes = {'resource': stages}
        super().__init__(parent, 'pi_stage_e709', data, settings_dict,
                         config_dict, additional_info, comboBoxes=comboboxes,
                         labels=None)
        # label = QLabel('select instrument:')
        # self.comboBox_instrument = QComboBox()
        # if not stages:
        #     self.comboBox_connection_type.addItem('NO STAGE FOUND!')
        # else:
        #     self.comboBox_instrument.addItems(stages)
        # if 'resource' in settings_dict and settings_dict['resource'] in stages:
        #     self.comboBox_instrument.setCurrentText(settings_dict['resource'])
        # self.layout().addWidget(label, 5, 0)
        # self.layout().addWidget(self.comboBox_instrument, 5, 1, 1, 4)
        self.load_settings()
    
    # def get_settings(self):
    #     self.settings_dict['resource'] = self.comboBox_instrument.currentText()
    #     return super().get_settings()
