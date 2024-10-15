from .korad_3005p_ophyd import Korad_3005P

from nomad_camels.main_classes import device_class

class subclass(device_class.Device):
	def __init__(self, **kwargs):
		super().__init__(name="korad_3005p", virtual=False, tags=['voltage', 'current'], directory="korad_3005p", ophyd_device=Korad_3005P, ophyd_class_name="Korad_3005P", **kwargs)


class subclass_config(device_class.Simple_Config):
	def __init__(self, parent=None, data="", settings_dict=None, config_dict=None, additional_info=None):
		super().__init__(parent, "korad_3005p", data, settings_dict, config_dict, additional_info)
		self.comboBox_connection_type.addItem("Local VISA")
		self.load_settings()
