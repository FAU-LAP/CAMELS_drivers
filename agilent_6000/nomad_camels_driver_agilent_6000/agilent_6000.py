from .agilent_6000_ophyd import Agilent_6000

from nomad_camels.main_classes import device_class

from PySide6.QtWidgets import QGridLayout, QLabel, QLineEdit


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(name='agilent_6000', virtual=False,
                         tags=['oscilloscope', 'voltage', 'current'],
                         ophyd_device=Agilent_6000,
                         ophyd_class_name='Agilent_6000', **kwargs)
        self.config['invert_colors'] = False
        self.config['grayscale'] = False
        self.config['image_type'] = 'png'

class subclass_config(device_class.Simple_Config):
    def __init__(self, parent=None, data='', settings_dict=None,
                 config_dict=None, additional_info=None):
        comboboxes = {'image_type': ['png', 'jpg', 'bmp', 'tif'],
                      }
        super().__init__(parent, 'Agilent 6000', data, settings_dict,
                         config_dict, additional_info, comboBoxes=comboboxes)
        self.comboBox_connection_type.addItem('Local VISA')
        self.load_settings()
