from nomad_camels_driver_thorlabs_K10CR1.thorlabs_K10CR1_ophyd import Thorlabs_K10CR1
from nomad_camels.main_classes import device_class
from pylablib.devices.Thorlabs.kinesis import list_kinesis_devices

class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(name='thorlabs_K10CR1', virtual=False,
                         tags=['Rotation Stage'],
                         ophyd_device=Thorlabs_K10CR1,
                         ophyd_class_name='Thorlabs_K10CR1', **kwargs)
        self.settings['serial_number'] = ''
        self.settings['home_on_start'] = True

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
        super().__init__(parent, 'Thorlabs K10CR1', data, settings_dict,
                         config_dict, additional_info, comboBoxes=comboboxes)
        self.load_settings()

    def get_settings(self):
        settings = super().get_settings()
        sn = settings['serial_number']
        if sn:
            sn = sn.split('-')[-1][1:]
            settings['serial_number'] = sn
        return settings
