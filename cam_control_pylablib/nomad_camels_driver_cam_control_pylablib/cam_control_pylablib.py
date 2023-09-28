from nomad_camels_driver_cam_control_pylablib.cam_control_pylablib_ophyd import Cam_Control_Pylablib
from nomad_camels.main_classes import device_class


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(name='cam_control_pylablib', virtual=False,
                         tags=['Camera'],
                         ophyd_device=Cam_Control_Pylablib,
                         ophyd_class_name='Cam_Control_Pylablib',
                         non_channel_functions=['start_saving', 'stop_saving', 'save_snapshot', 'grab_background'],
                         **kwargs)
        self.config['exposure_time'] = 100  # in ms
        self.settings['overwrite_exposure_time'] = True
        self.settings['host_ip'] = '127.0.0.1'
        self.settings['port'] = 18923
        self.settings['byte_length'] = 9000000



class subclass_config(device_class.Simple_Config):
    def __init__(self, parent=None, data='', settings_dict=None,
                 config_dict=None, additional_info=None):
        labels = {'host_ip': 'Host IP',
                  'port': 'Port',
                  'byte_length': 'Byte length',
                  'exposure_time': 'Exposure time (ms)',
                  'overwrite_exposure_time': 'Overwrite exposure time'
                  }
        super().__init__(parent, 'Cam Control', data, settings_dict,
                         config_dict, additional_info,labels=labels )
        self.load_settings()
