from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.custom_function_signal import Custom_Function_Signal, Custom_Function_SignalRO
from nomad_camels.bluesky_handling.visa_signal import VISA_Signal, VISA_Signal_RO, VISA_Device

class Korad_3005P(VISA_Device):
	read_current_output_setting = Cpt(VISA_Signal_RO, name="read_current_output_setting", query="ISET1?\n", parse_return_type="float", metadata={"units": "A", "description": "Returns the output current setting"})
	read_voltage_output_setting = Cpt(VISA_Signal_RO, name="read_voltage_output_setting", query="VSET1?\n", parse_return_type="float", metadata={"units": "V", "description": "Returns the output voltage setting"})
	read_current_output_actual = Cpt(VISA_Signal_RO, name="read_current_output_actual", query="IOUT1?\n", parse_return_type="float", metadata={"units": "A", "description": "Returns the actual output current"})
	read_voltage_output_actual = Cpt(VISA_Signal_RO, name="read_voltage_output_actual", query="VOUT1?\n", parse_return_type="float", metadata={"units": "V", "description": "Returns the actual output voltage"})
	set_output_current = Cpt(VISA_Signal, name="set_output_current", write="ISET1:{value}", parse_return_type=None, metadata={"units": "A", "description": "Sets the output current"})
	set_output_voltage = Cpt(VISA_Signal, name="set_output_voltage", write="VSET1:{value}", parse_return_type=None, metadata={"units": "V", "description": "Sets the output voltage"})
	output = Cpt(VISA_Signal, name="output", write="OUT{value}", parse_return_type=None, metadata={"units": "", "description": "output: 0 OFF, 1 ON"})
	over_current_mode = Cpt(VISA_Signal, name="over_current_mode", write="OCP{value}", parse_return_type=None, metadata={"units": "", "description": "OCP: 0 OFF, 1 ON"})
	instrument_id = Cpt(VISA_Signal_RO, name="instrument_id", query="*IDN?\n", parse_return_type="str", kind="config", metadata={"units": "", "description": "Returns instrument ID"})
	status_string = Cpt(VISA_Signal_RO, name="status_string", query="STATUS?\n", parse_return_type="int", kind="config", metadata={"units": "", "description": "Returns instrument status as an 8 bit number"})

	def __init__(self, prefix="", *, name, kind=None, read_attrs=None, configuration_attrs=None, parent=None, resource_name="", write_termination="\r\n", read_termination="\r\n", baud_rate=9600, **kwargs):
		super().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs, configuration_attrs=configuration_attrs, parent=parent, resource_name=resource_name, baud_rate=baud_rate, read_termination=read_termination, write_termination=write_termination, **kwargs)

