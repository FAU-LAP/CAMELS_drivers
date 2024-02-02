from .agilent_6000_ophyd import Agilent_6000

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

        self.controls = {'Agilent_6000_Manual_Control': [Agilent_6000_Manual_Control, Agilent_6000_Manual_Control_Config]}

class subclass_config(device_class.Simple_Config):
    def __init__(self, parent=None, data='', settings_dict=None,
                 config_dict=None, additional_info=None):
        comboboxes = {'image_type': ['png', 'bmp'],
                      }
        super().__init__(parent, 'Agilent 6000', data, settings_dict,
                         config_dict, additional_info, comboBoxes=comboboxes)
        self.comboBox_connection_type.addItem('Local VISA')
        self.load_settings()
