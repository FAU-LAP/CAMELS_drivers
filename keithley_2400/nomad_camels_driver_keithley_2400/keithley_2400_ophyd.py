from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.visa_signal import VISA_Signal, VISA_Signal_RO, VISA_Device

class Keithley_2400(VISA_Device):
	measure_voltage = Cpt(VISA_Signal_RO, name="measure_voltage", parse=r'^([+-].*),[+-].*,[+-].*,[+-].*,[+-].*$', parse_return_type="float", metadata={"units": "V", "description": "Measures voltage using FETC?"})
	measure_current = Cpt(VISA_Signal_RO, name="measure_current", parse=r'^[+-].*,([+-].*),[+-].*,[+-].*,[+-].*$', parse_return_type="float", metadata={"units": "A", "description": "Measures current using FETC?"})
	set_voltage = Cpt(VISA_Signal, name="set_voltage", parse_return_type=None, metadata={"units": "V", "description": "Sets voltage to desired value"})
	set_current = Cpt(VISA_Signal, name="set_current", parse_return_type=None, metadata={"units": "A", "description": "Sets current to desired value"})
	current_compliance = Cpt(VISA_Signal, name="current_compliance", write=":CURR:PROT {value}", parse_return_type=None, kind="config", metadata={"units": "V", "description": "Maximum allowed current"})
	voltage_compliance = Cpt(VISA_Signal, name="voltage_compliance", write=":VOLT:PROT {value}", parse_return_type=None, kind="config", metadata={"units": "A", "description": "Maximum allowed voltage"})
	current_range = Cpt(VISA_Signal, name="current_range", parse_return_type=None, kind="config", metadata={"units": "V", "description": "Sets measurement range"})
	voltage_range = Cpt(VISA_Signal, name="voltage_range", parse_return_type=None, kind="config", metadata={"units": "A", "description": "Sets measurements range"})

	device_id = Cpt(VISA_Signal_RO, name="device_id", query="*IDN?", parse_return_type="str", kind="config", metadata={"units": "", "description": ""})

	def __init__(self, prefix="", *, name, kind=None, read_attrs=None, configuration_attrs=None, parent=None, resource_name="", write_termination="\r\n", read_termination="\r\n", baud_rate=9600, **kwargs):
		super().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs, configuration_attrs=configuration_attrs, parent=parent, resource_name=resource_name, baud_rate=baud_rate, read_termination=read_termination, write_termination=write_termination, **kwargs)
		self.measure_voltage.query = self.measure_voltage_query_function
		self.measure_current.query = self.measure_current_query_function
		self.set_voltage.write = self.set_voltage_write_function
		self.set_current.write = self.set_current_write_function
		self.current_range.write = self.current_range_write_function
		self.voltage_range.write = self.voltage_range_write_function
		if name == 'test':
			return
		self.source_function = None
		self.measure_function = None
		self.output_on = False

	def measure_voltage_query_function(self):
		if self.measure_function != 'voltage':
			self.visa_instrument.write(':CONF:VOLT')
			self.measure_function = 'voltage'
		else:
			pass
		return ':READ?'

	def measure_current_query_function(self):
		if self.measure_function != 'current':
			self.visa_instrument.write(':CONF:CURR')
			self.measure_function = 'current'
		else:
			pass
		return ':READ?'

	def set_voltage_write_function(self, value):
		if self.source_function != 'voltage':
			self.visa_instrument.write(':SOUR:FUNC VOLT')
			self.source_function = 'voltage'
		else:
			pass
		if self.output_on:
			pass
		else:
			self.visa_instrument.write(':OUTP 1')
		return f':SOUR:VOLT {value}'

	def set_current_write_function(self, value):
		if self.source_function != 'current':
			self.visa_instrument.write(':SOUR:FUNC CURR')
			self.source_function = 'current'
		else:
			pass
		if self.output_on:
			pass
		else:
			self.visa_instrument.write(':OUTP 1')
		return f':SOUR:CURR {value}'

	def current_range_write_function(self, value):
		return f':CURR:RANG {value}'

	def voltage_range_write_function(self, value):
		return f':VOLT:RANG {value}'


	def finalize_steps(self):
		self.visa_instrument.write('OUTP 0')

