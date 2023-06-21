from nomad_camels.main_classes import device_class

class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class subclass_config(device_class.Device_Config):
    def __init__(self, parent=None, data='', settings_dict=None, additional_info=None):
        super().__init__(parent, 'Keithley 220', data, settings_dict, additional_info)
        self.load_settings()

# TODO This device is not implemented at all! Do not build!