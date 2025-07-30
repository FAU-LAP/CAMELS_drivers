from .standford_research_GS_384_ophyd import Standford_Research_Gs_384

from nomad_camels.main_classes import device_class

class subclass(device_class.Device):
	def __init__(self, **kwargs):
		super().__init__(name="standford_research_GS_384", virtual=False, tags=['microwave', 'radiowave', 'signal', 'generator'], directory="standford_research_GS_384", ophyd_device=Standford_Research_Gs_384, ophyd_class_name="Standford_Research_Gs_384", **kwargs)


class subclass_config(device_class.Simple_Config):
	def __init__(self, parent=None, data="", settings_dict=None, config_dict=None, additional_info=None):
		super().__init__(parent, "standford_research_GS_384", data, settings_dict, config_dict, additional_info)
		self.comboBox_connection_type.addItem("Local VISA")
		self.load_settings()
