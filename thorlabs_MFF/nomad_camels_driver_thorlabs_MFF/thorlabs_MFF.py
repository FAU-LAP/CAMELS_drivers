from nomad_camels_driver_thorlabs_MFF.thorlabs_MFF_ophyd import Thorlabs_MFF
from nomad_camels.main_classes import device_class
from pylablib.devices.Thorlabs.kinesis import list_kinesis_devices

class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(name='thorlabs_MFF', virtual=False,
                         tags=['Rotation Stage'],
                         ophyd_device=Thorlabs_MFF,
                         ophyd_class_name='Thorlabs_MFF', **kwargs)
        self.settings['serial_number'] = ''
        self.config['transit_time'] = 1.5

class subclass_config(device_class.Simple_Config):
    def __init__(self, parent=None, data='', settings_dict=None,
                 config_dict=None, additional_info=None):
        kinesis_devs = list_kinesis_devices()
        availables = []
        sn = None
        if 'serial_number' in settings_dict:
            sn = settings_dict['serial_number']
        for dev in kinesis_devs:
            name = f'{dev[1]} - {dev[0]}'
            availables.append(name)
            if sn == dev[0]:
                settings_dict['serial_number'] = name
        comboboxes = {'serial_number': availables}
        super().__init__(parent, 'Thorlabs MFF', data, settings_dict,
                         config_dict, additional_info, comboBoxes=comboboxes)
        self.load_settings()

    def get_settings(self):
        settings = super().get_settings()
        sn = settings['serial_number']
        if sn:
            sn = sn.split('-')[-1][1:]
            settings['serial_number'] = sn
        return settings
