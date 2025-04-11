from .zurichinstruments_uhfli_600_ophyd import Zurichinstruments_Uhfli_600, trigger_dict

from nomad_camels.main_classes import device_class

class subclass(device_class.Device):
	def __init__(self, **kwargs):
		super().__init__(name="zurichinstruments_uhfli_600", virtual=False, tags=[], directory="zurichinstruments_uhfli_600", ophyd_device=Zurichinstruments_Uhfli_600, ophyd_class_name="Zurichinstruments_Uhfli_600", **kwargs)
		

		self.config["In_1_Range"] = 1
		self.config["In_1_Scaling_Value"] = 1
		self.config["In_1_AC"] = False
		self.config["In_1_50_Ohm"] = True

		self.config["In_2_Range"] = 1
		self.config["In_2_Scaling_Value"] = 1
		self.config["In_2_AC"] = False
		self.config["In_2_50_Ohm"] = True
		
		
		self.config["Demod_4_Mode"] = "Manual"
		self.config["Demod_8_Mode"] = "Manual"
		
		self.config["Demod_1_Harmonics"] = 1
		self.config["Demod_1_Phase"] = 0
		self.config["Demod_1_Input"] = "Sig In 1"
		self.config["Demod_1_LP_Order"] = 3
		#self.config["Demod_1_LP_BW_TC"] = ""
		#self.config["Demod_1_LP_BW_Value"] = 0
		self.config["Demod_1_LP_TC_Value"] = 810.5e-6
		self.config["Demod_1_Sinc"] = False
		self.config["Demod_1_Data_Trans"] = True
		self.config["Demod_1_Data_Trans_Value"] = 1.717e3
		self.config["Demod_1_Data_Trans_Trigger"] = "Continuous"

		self.config["Demod_2_Harmonics"] = 1
		self.config["Demod_2_Phase"] = 0
		self.config["Demod_2_Input"] = "Sig In 1"
		self.config["Demod_2_LP_Order"] = 3
		#self.config["Demod_2_LP_BW_TC"] = ""
		#self.config["Demod_2_LP_BW_Value"] = 0
		self.config["Demod_2_LP_TC_Value"] = 810.5e-6
		self.config["Demod_2_Sinc"] = False
		self.config["Demod_2_Data_Trans"] = False
		self.config["Demod_2_Data_Trans_Value"] = 1.717e3
		self.config["Demod_2_Data_Trans_Trigger"] = "Continuous"

		self.config["Demod_3_Harmonics"] = 1
		self.config["Demod_3_Phase"] = 0
		self.config["Demod_3_Input"] = "Sig In 1"
		self.config["Demod_3_LP_Order"] = 3
		#self.config["Demod_3_LP_BW_TC"] = ""
		#self.config["Demod_3_LP_BW_Value"] = 0
		self.config["Demod_3_LP_TC_Value"] = 810.5e-6
		self.config["Demod_3_Sinc"] = False
		self.config["Demod_3_Data_Trans"] = False
		self.config["Demod_3_Data_Trans_Value"] = 1.717e3
		self.config["Demod_3_Data_Trans_Trigger"] = "Continuous"

		self.config["Demod_4_Harmonics"] = 1
		self.config["Demod_4_Phase"] = 0
		self.config["Demod_4_Input"] = "Sig In 1"
		self.config["Demod_4_LP_Order"] = 3
		#self.config["Demod_4_LP_BW_TC"] = ""
		#self.config["Demod_4_LP_BW_Value"] = 0
		self.config["Demod_4_LP_TC_Value"] = 810.5e-6
		self.config["Demod_4_Sinc"] = False
		self.config["Demod_4_Data_Trans"] = False
		self.config["Demod_4_Data_Trans_Value"] = 1.717e3
		self.config["Demod_4_Data_Trans_Trigger"] = "Continuous"

		self.config["Demod_5_Harmonics"] = 1
		self.config["Demod_5_Phase"] = 0
		self.config["Demod_5_Input"] = "Sig In 2"
		self.config["Demod_5_LP_Order"] = 3
		#self.config["Demod_5_LP_BW_TC"] = ""
		#self.config["Demod_5_LP_BW_Value"] = 0
		self.config["Demod_5_LP_TC_Value"] = 810.5e-6
		self.config["Demod_5_Sinc"] = False
		self.config["Demod_5_Data_Trans"] = False
		self.config["Demod_5_Data_Trans_Value"] = 1.717e3
		self.config["Demod_5_Data_Trans_Trigger"] = "Continuous"

		self.config["Demod_6_Harmonics"] = 1
		self.config["Demod_6_Phase"] = 0
		self.config["Demod_6_Input"] = "Sig In 2"
		self.config["Demod_6_LP_Order"] = 3
		#self.config["Demod_6_LP_BW_TC"] = ""
		#self.config["Demod_6_LP_BW_Value"] = 0
		self.config["Demod_6_LP_TC_Value"] = 810.5e-6
		self.config["Demod_6_Sinc"] = False
		self.config["Demod_6_Data_Trans"] = False
		self.config["Demod_6_Data_Trans_Value"] = 1.717e3
		self.config["Demod_6_Data_Trans_Trigger"] = "Continuous"

		self.config["Demod_7_Harmonics"] = 1
		self.config["Demod_7_Phase"] = 0
		self.config["Demod_7_Input"] = "Sig In 2"
		self.config["Demod_7_LP_Order"] = 3
		#self.config["Demod_7_LP_BW_TC"] = ""
		#self.config["Demod_7_LP_BW_Value"] = 0
		self.config["Demod_7_LP_TC_Value"] = 810.5e-6
		self.config["Demod_7_Sinc"] = False
		self.config["Demod_7_Data_Trans"] = False
		self.config["Demod_7_Data_Trans_Value"] = 1.717e3
		self.config["Demod_7_Data_Trans_Trigger"] = "Continuous"

		self.config["Demod_8_Harmonics"] = 1
		self.config["Demod_8_Phase"] = 0
		self.config["Demod_8_Input"] = "Sig In 2"
		self.config["Demod_8_LP_Order"] = 3
		#self.config["Demod_8_LP_BW_TC"] = ""
		#self.config["Demod_8_LP_BW_Value"] = 0
		self.config["Demod_8_LP_TC_Value"] = 810.5e-6
		self.config["Demod_8_Sinc"] = False
		self.config["Demod_8_Data_Trans"] = False
		self.config["Demod_8_Data_Trans_Value"] = 1.717e3
		self.config["Demod_8_Data_Trans_Trigger"] = "Continuous"


		self.settings["port_number"] = 8004
		self.settings["serial_number"] = ''
		self.settings["connection_type"] = 'USB'


class subclass_config(device_class.Simple_Config):
	def __init__(self, parent=None, data="", settings_dict=None, config_dict=None, additional_info=None):
		demod_inputs = ['Sig In 1', 'Sig In 2', 'Trigger 1', 'Trigger 2', 'Aux Out 1', 'Aux Out 2', 'Aux Out 3', 'Aux Out 4', 'Aux In 1', 'Aux In 2']

		comboBoxes = {
			'Demod_1_Input': demod_inputs,
			'Demod_2_Input': demod_inputs,
			'Demod_3_Input': demod_inputs,
			'Demod_4_Input': demod_inputs,
			'Demod_5_Input': demod_inputs,
			'Demod_6_Input': demod_inputs,
			'Demod_7_Input': demod_inputs,
			'Demod_8_Input': demod_inputs,

			'Demod_4_Mode' : ['Manual', 'Ext_Ref', 'ExtRef Low BW', 'ExtRef High BW'],

			'Demod_8_Mode' : ['Manual', 'Ext_Ref', 'ExtRef Low BW', 'ExtRef High BW']
		}
		super().__init__(parent, "zurichinstruments_uhfli_600", data, settings_dict, config_dict, additional_info, comboBoxes=comboBoxes)
		
		# self.sub_widget.config_checks['Out_1_50_Ohm'].stateChanged().connect(self.out_1_range_change)
		# self.sub_widget.config_floats['In_1_Scaling_Value'].currentTextChanged().connect(lambda: self.set_into_range(channel=1))

		self.load_settings()

	def set_input_scaling_into_range(self, channel):
		value = float(self.sub_widget.config_floats[f'In_{channel}_Scaling_Value'])
		if value < 1e-12:
			value = 1e-12
		elif value > 1e9:
			value = 1e9
		self.sub_widget.config_floats[f'In_{channel}_Scaling_Value'].setText(str(value))

	def set_input_range_into_range(self, channel):
		value = float(self.sub_widget.config_floats[f'In_{channel}_Range'])
		if value < 0.01:
			value = 0.01
		elif value > 1.5:
			value = 1.5
		self.sub_widget.config_floats[f'In_{channel}_Range'].setText(str(value))
	
	def out_1_range_change(self):
		self.sub_widget.config_combos['Out_1_Range'].clear()
		if self.sub_widget.config_checks['Out_1_50_Ohm'].isChecked():
			items = ['750 mV', '75 mV']
		else:
			items = ['1.5 V', '150 mV']
		self.sub_widget.config_combos['Out_1_Range'].addItems(items)

