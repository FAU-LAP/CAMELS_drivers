from .adc_x418_ophyd import Adc_X418

from nomad_camels.main_classes import device_class

class subclass(device_class.Device):
	def __init__(self, **kwargs):
		super().__init__(
			name="adc_x418",
			virtual=False,
			tags=[],
			directory="adc_x418",
			ophyd_device=Adc_X418,
			ophyd_class_name="Adc_X418",
			**kwargs
		)
		self.config["set_decimal_places_all_channels"] = 4
		self.config["set_range_channel_1"] = 10.24
		self.config["set_range_channel_2"] = 10.24
		self.config["set_range_channel_3"] = 10.24
		self.config["set_range_channel_4"] = 10.24
		self.config["set_range_channel_5"] = 10.24
		self.config["set_range_channel_6"] = 10.24
		self.config["set_range_channel_7"] = 10.24
		self.config["set_range_channel_8"] = 10.24
		self.settings["host_ip"] = "192.168.1.2"
		self.settings["port"] = 80
		self.settings["byte_length"] = 10000
		self.settings["use_admin_credentials"] = True
		self.settings["user_password"] = False


class subclass_config(device_class.Simple_Config):
	def __init__(
		self,
		parent=None,
		data="",
		settings_dict=None,
		config_dict=None,
		additional_info=None
	):
		labels = {
			"host_ip": "Host IP",
			"port": "Port",
			"byte_length": "Byte length",
			"set_decimal_places_all_channels": "Number of digits after . (all channels)",
			"set_range_channel_1": "Range of channel 1 (V)",
			"set_range_channel_2": "Range of channel 2 (V)",
			"set_range_channel_3": "Range of channel 3 (V)",
			"set_range_channel_4": "Range of channel 4 (V)",
			"set_range_channel_5": "Range of channel 5 (V)",
			"set_range_channel_6": "Range of channel 6 (V)",
			"set_range_channel_7": "Range of channel 7 (V)",
			"set_range_channel_8": "Range of channel 8 (V)",
			"use_admin_credentials": "Use admin credentials (necessary for changing settings of X418)",
			"user_password": "User password has been set (recommended for public networks)",
		}
		super().__init__(
			parent,
			"adc_x418",
			data,
			settings_dict,
			config_dict,
			additional_info,
			labels=labels,
		)
		self.load_settings()
