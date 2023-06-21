from .gap_burner_arduino_ophyd import Gap_Burner_Arduino
from nomad_camels.main_classes import device_class

class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(name='gap_burner_arduino', virtual=False,
                         tags=['Arduino', 'voltage', 'current', 'burn'],
                         ophyd_device=Gap_Burner_Arduino,
                         ophyd_class_name='Gap_Burner_Arduino', **kwargs)
        self.config["ramp_time"] = 400
        self.config["offset"] = 1200
        self.config["min_current"] = 0
        self.config["min_voltage"] = 600
        self.config["dac_ref_zero"] = 0
        self.config["dac_zero"] = 400



class subclass_config(device_class.Simple_Config):
    def __init__(self, parent=None, data='', settings_dict=None,
                 config_dict=None, additional_info=None):
        super().__init__(parent, 'Gap Burner - Arduino', data, settings_dict,
                         config_dict, additional_info)
        self.comboBox_connection_type.addItem('Local VISA')
        self.load_settings()
