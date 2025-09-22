from ophyd import Component as Cpt
import numpy as np
from nomad_camels.bluesky_handling.custom_function_signal import Custom_Function_Signal, Custom_Function_SignalRO
from ophyd import Device
from zhinst.core import ziDAQServer


trigger_dict = {
	'Continuous': 0,
	'Input 3 - Rise': 1,
	'Input 3 - Fall': 2,
	'Input 3 - Both': 3,
	'Input 3 - High': 32,
	'Input 3 - Low': 16,
	'Input 4 - Rise': 4,
	'Input 4 - Fall': 8,
	'Input 4 - Both': 12,
	'Input 4 - High': 128,
	'Input 4 - Low': 64,
	'Input 4 - Rise': 5,
	'Input 4 - Fall': 10,
	'Input 4 - Both': 15,
	'Input 4 - High': 160,
	'Input 4 - Low': 80
}


class Zurichinstruments_Uhfli_600(Device):
	Out_1 = Cpt(Custom_Function_Signal, name="Out_1", metadata={"units": "", "description": "On/Off"})
	Out_1_50_Ohm = Cpt(Custom_Function_Signal, name="Out_1_50_Ohm", metadata={"units": "", "description": "50 Ohm On/Off"})
	Out_1_Range = Cpt(Custom_Function_Signal, name="Out_1_Range", metadata={"units": "V", "description": "Output Range"})
	Out_1_Offset = Cpt(Custom_Function_Signal, name="Out_1_Offset", metadata={"units": "V", "description": "Voltage Offset"})
	#Out_1_Amp_Type = Cpt(Custom_Function_Signal, name="Out_1_Amp_Type", metadata={"units": "", "description": "Vpk Vrms VdBm"})
	Out_1_Amp_Value = Cpt(Custom_Function_Signal, name="Out_1_Amp_Value", metadata={"units": "V", "description": "Sinus Amplitude"})
	Out_1_Amp = Cpt(Custom_Function_Signal, name="Out_1_Amp", metadata={"units": "", "description": "On/Off"})
	In_1_Range = Cpt(Custom_Function_Signal, name="In_1_Range", kind="config", metadata={"units": "V", "description": "Input Range"})
	In_1_Scaling_Value = Cpt(Custom_Function_Signal, name="In_1_Scaling_Value", kind="config", metadata={"units": "", "description": "Scaling Amount"})
	In_1_AC = Cpt(Custom_Function_Signal, name="In_1_AC", kind="config", metadata={"units": "", "description": "AC Mode On/Off"})
	In_1_50_Ohm = Cpt(Custom_Function_Signal, name="In_1_50_Ohm", kind="config", metadata={"units": "", "description": "50 Ohm / 1 Megaohm"})
	In_1_Diff = Cpt(Custom_Function_Signal, name="In_1_Diff", kind="config", metadata={"units": "", "description": "Off, Inverted, In1 - In2, In2 - In1"})


	Out_2 = Cpt(Custom_Function_Signal, name="Out_2", metadata={"units": "", "description": "On/Off"})
	Out_2_50_Ohm = Cpt(Custom_Function_Signal, name="Out_2_50_Ohm", kind="config", metadata={"units": "", "description": "50 Ohm On/Off"})
	Out_2_Range = Cpt(Custom_Function_Signal, name="Out_2_Range", metadata={"units": "V", "description": "Output Range"})
	Out_2_Offset = Cpt(Custom_Function_Signal, name="Out_2_Offset", metadata={"units": "V", "description": "Voltage Offset"})
	#Out_2_Amp_Type = Cpt(Custom_Function_Signal, name="Out_2_Amp_Type", metadata={"units": "", "description": "Vpk Vrms VdBm"})
	Out_2_Amp_Value = Cpt(Custom_Function_Signal, name="Out_2_Amp_Value", metadata={"units": "V", "description": "Sinus Amplitude"})
	Out_2_Amp = Cpt(Custom_Function_Signal, name="Out_2_Amp", metadata={"units": "", "description": "On/Off"})
	In_2_Range = Cpt(Custom_Function_Signal, name="In_2_Range", kind="config", metadata={"units": "V", "description": "Input Range"})
	In_2_Scaling_Value = Cpt(Custom_Function_Signal, name="In_2_Scaling_Value", kind="config", metadata={"units": "", "description": "Scaling Amount"})
	In_2_AC = Cpt(Custom_Function_Signal, name="In_2_AC", kind="config", metadata={"units": "", "description": "AC Mode On/Off"})
	In_2_50_Ohm = Cpt(Custom_Function_Signal, name="In_2_50_Ohm", kind="config", metadata={"units": "", "description": "50 Ohm / 1 Megaohm"})
	In_2_Diff = Cpt(Custom_Function_Signal, name="In_2_Diff", kind="config", metadata={"units": "", "description": "Off, Inverted, In1 - In2, In2 - In1"})

	Osc_1_Frequency = Cpt(Custom_Function_Signal, name="Osc_1_Frequency", metadata={"units": "Hz", "description": "Frequency of Oscillator"})
	Osc_2_Frequency = Cpt(Custom_Function_Signal, name="Osc_2_Frequency", metadata={"units": "Hz", "description": "Frequency of Oscillator"})
	
	Demod_4_Mode = Cpt(Custom_Function_Signal, name="Demod_4_Mode", kind="config", metadata={"units": "", "description": "Manual, ExtRef, ExtRef Low BW, ExtRef High BW"})
	Demod_8_Mode = Cpt(Custom_Function_Signal, name="Demod_8_Mode", kind="config", metadata={"units": "", "description": "Manual, ExtRef, ExtRef Low BW, ExtRef High BW"})
	
	Demod_1_Harmonics = Cpt(Custom_Function_Signal, name="Demod_1_Harmonics", kind="config", metadata={"units": "", "description": "Harmonic of Demodulator's Refrence Frequency"})
	Demod_1_Phase = Cpt(Custom_Function_Signal, name="Demod_1_Phase", kind="config", metadata={"units": "deg", "description": "Phase betweem Demodulator's Refrence Frequency and Output"})
	Demod_1_Input = Cpt(Custom_Function_Signal, name="Demod_1_Input", kind="config", metadata={"units": "", "description": "Input Signal Channel"})
	Demod_1_LP_Order = Cpt(Custom_Function_Signal, name="Demod_1_LP_Order", kind="config", metadata={"units": "", "description": "Order of Lowpass filter"})
	#Demod_1_LP_BW_TC = Cpt(Custom_Function_Signal, name="Demod_1_LP_BW_TC", kind="config", metadata={"units": "", "description": "Choose between TimeConstant, BandWidth at 3 dB or BandWidth at NoiseEquivalentPower"})
	#Demod_1_LP_BW_Value = Cpt(Custom_Function_Signal, name="Demod_1_LP_BW_Value", kind="config", metadata={"units": "Hz", "description": "Value of Integration Bandwidth"})
	Demod_1_LP_TC_Value = Cpt(Custom_Function_Signal, name="Demod_1_LP_TC_Value", kind="config", metadata={"units": "s", "description": "Value of Integration Time Constant"})
	Demod_1_Sinc = Cpt(Custom_Function_Signal, name="Demod_1_Sinc", kind="config", metadata={"units": "", "description": "Enable Sinc Filter"})
	Demod_1_Data_Trans = Cpt(Custom_Function_Signal, name="Demod_1_Data_Trans", kind="config", metadata={"units": "", "description": "Enable Data Transfer"})
	Demod_1_Data_Trans_Value = Cpt(Custom_Function_Signal, name="Demod_1_Data_Trans_Value", kind="config", metadata={"units": "Sa/s", "description": "Set sampling rate of Demodulator Samples/second"})
	Demod_1_Data_Trans_Trigger = Cpt(Custom_Function_Signal, name="Demod_1_Data_Trans_Trigger", kind="config", metadata={"units": "", "description": "Continous, Trigger Input 3, Trigger Input 4, Trigger Input 3/4"})
	
	Demod_2_Harmonics = Cpt(Custom_Function_Signal, name="Demod_2_Harmonics", kind="config", metadata={"units": "", "description": "Harmonic of Demodulator's Refrence Frequency"})
	Demod_2_Phase = Cpt(Custom_Function_Signal, name="Demod_2_Phase", kind="config", metadata={"units": "deg", "description": "Phase betweem Demodulator's Refrence Frequency and Output"})
	Demod_2_Input = Cpt(Custom_Function_Signal, name="Demod_2_Input", kind="config", metadata={"units": "", "description": "Input Signal Channel"})
	Demod_2_LP_Order = Cpt(Custom_Function_Signal, name="Demod_2_LP_Order", kind="config", metadata={"units": "", "description": "Order of Lowpass filter"})
	#Demod_2_LP_BW_TC = Cpt(Custom_Function_Signal, name="Demod_2_LP_BW_TC", kind="config", metadata={"units": "", "description": "Choose between TimeConstant, BandWidth at 3 dB or BandWidth at NoiseEquivalentPower"})
	#Demod_2_LP_BW_Value = Cpt(Custom_Function_Signal, name="Demod_2_LP_BW_Value", kind="config", metadata={"units": "Hz", "description": "Value of Integration Bandwidth"})
	Demod_2_LP_TC_Value = Cpt(Custom_Function_Signal, name="Demod_2_LP_TC_Value", kind="config", metadata={"units": "s", "description": "Value of Integration Time Constant"})
	Demod_2_Sinc = Cpt(Custom_Function_Signal, name="Demod_2_Sinc", kind="config", metadata={"units": "", "description": "Enable Sinc Filter"})
	Demod_2_Data_Trans = Cpt(Custom_Function_Signal, name="Demod_2_Data_Trans", kind="config", metadata={"units": "", "description": "Enable Data Transfer"})
	Demod_2_Data_Trans_Value = Cpt(Custom_Function_Signal, name="Demod_2_Data_Trans_Value", kind="config", metadata={"units": "Sa/s", "description": "Set sampling rate of Demodulator Samples/second"})
	Demod_2_Data_Trans_Trigger = Cpt(Custom_Function_Signal, name="Demod_2_Data_Trans_Trigger", kind="config", metadata={"units": "", "description": "Continous, Trigger Input 3, Trigger Input 4, Trigger Input 3/4"})
	
	Demod_3_Harmonics = Cpt(Custom_Function_Signal, name="Demod_3_Harmonics", kind="config", metadata={"units": "", "description": "Harmonic of Demodulator's Refrence Frequency"})
	Demod_3_Phase = Cpt(Custom_Function_Signal, name="Demod_3_Phase", kind="config", metadata={"units": "deg", "description": "Phase betweem Demodulator's Refrence Frequency and Output"})
	Demod_3_Input = Cpt(Custom_Function_Signal, name="Demod_3_Input", kind="config", metadata={"units": "", "description": "Input Signal Channel"})
	Demod_3_LP_Order = Cpt(Custom_Function_Signal, name="Demod_3_LP_Order", kind="config", metadata={"units": "", "description": "Order of Lowpass filter"})
	#Demod_3_LP_BW_TC = Cpt(Custom_Function_Signal, name="Demod_3_LP_BW_TC", kind="config", metadata={"units": "", "description": "Choose between TimeConstant, BandWidth at 3 dB or BandWidth at NoiseEquivalentPower"})
	#Demod_3_LP_BW_Value = Cpt(Custom_Function_Signal, name="Demod_3_LP_BW_Value", kind="config", metadata={"units": "Hz", "description": "Value of Integration Bandwidth"})
	Demod_3_LP_TC_Value = Cpt(Custom_Function_Signal, name="Demod_3_LP_TC_Value", kind="config", metadata={"units": "s", "description": "Value of Integration Time Constant"})
	Demod_3_Sinc = Cpt(Custom_Function_Signal, name="Demod_3_Sinc", kind="config", metadata={"units": "", "description": "Enable Sinc Filter"})
	Demod_3_Data_Trans = Cpt(Custom_Function_Signal, name="Demod_3_Data_Trans", kind="config", metadata={"units": "", "description": "Enable Data Transfer"})
	Demod_3_Data_Trans_Value = Cpt(Custom_Function_Signal, name="Demod_3_Data_Trans_Value", kind="config", metadata={"units": "Sa/s", "description": "Set sampling rate of Demodulator Samples/second"})
	Demod_3_Data_Trans_Trigger = Cpt(Custom_Function_Signal, name="Demod_3_Data_Trans_Trigger", kind="config", metadata={"units": "", "description": "Continous, Trigger Input 3, Trigger Input 4, Trigger Input 3/4"})
	
	Demod_4_Harmonics = Cpt(Custom_Function_Signal, name="Demod_4_Harmonics", kind="config", metadata={"units": "", "description": "Harmonic of Demodulator's Refrence Frequency"})
	Demod_4_Phase = Cpt(Custom_Function_Signal, name="Demod_4_Phase", kind="config", metadata={"units": "deg", "description": "Phase betweem Demodulator's Refrence Frequency and Output"})
	Demod_4_Input = Cpt(Custom_Function_Signal, name="Demod_4_Input", kind="config", metadata={"units": "", "description": "Input Signal Channel"})
	Demod_4_LP_Order = Cpt(Custom_Function_Signal, name="Demod_4_LP_Order", kind="config", metadata={"units": "", "description": "Order of Lowpass filter"})
	#Demod_4_LP_BW_TC = Cpt(Custom_Function_Signal, name="Demod_4_LP_BW_TC", kind="config", metadata={"units": "", "description": "Choose between TimeConstant, BandWidth at 3 dB or BandWidth at NoiseEquivalentPower"})
	#Demod_4_LP_BW_Value = Cpt(Custom_Function_Signal, name="Demod_4_LP_BW_Value", kind="config", metadata={"units": "Hz", "description": "Value of Integration Bandwidth"})
	Demod_4_LP_TC_Value = Cpt(Custom_Function_Signal, name="Demod_4_LP_TC_Value", kind="config", metadata={"units": "s", "description": "Value of Integration Time Constant"})
	Demod_4_Sinc = Cpt(Custom_Function_Signal, name="Demod_4_Sinc", kind="config", metadata={"units": "", "description": "Enable Sinc Filter"})
	Demod_4_Data_Trans = Cpt(Custom_Function_Signal, name="Demod_4_Data_Trans", kind="config", metadata={"units": "", "description": "Enable Data Transfer"})
	Demod_4_Data_Trans_Value = Cpt(Custom_Function_Signal, name="Demod_4_Data_Trans_Value", kind="config", metadata={"units": "Sa/s", "description": "Set sampling rate of Demodulator Samples/second"})
	Demod_4_Data_Trans_Trigger = Cpt(Custom_Function_Signal, name="Demod_4_Data_Trans_Trigger", kind="config", metadata={"units": "", "description": "Continous, Trigger Input 3, Trigger Input 4, Trigger Input 3/4"})
	
	Demod_5_Harmonics = Cpt(Custom_Function_Signal, name="Demod_5_Harmonics", kind="config", metadata={"units": "", "description": "Harmonic of Demodulator's Refrence Frequency"})
	Demod_5_Phase = Cpt(Custom_Function_Signal, name="Demod_5_Phase", kind="config", metadata={"units": "deg", "description": "Phase betweem Demodulator's Refrence Frequency and Output"})
	Demod_5_Input = Cpt(Custom_Function_Signal, name="Demod_5_Input", kind="config", metadata={"units": "", "description": "Input Signal Channel"})
	Demod_5_LP_Order = Cpt(Custom_Function_Signal, name="Demod_5_LP_Order", kind="config", metadata={"units": "", "description": "Order of Lowpass filter"})
	#Demod_5_LP_BW_TC = Cpt(Custom_Function_Signal, name="Demod_5_LP_BW_TC", kind="config", metadata={"units": "", "description": "Choose between TimeConstant, BandWidth at 3 dB or BandWidth at NoiseEquivalentPower"})
	#Demod_5_LP_BW_Value = Cpt(Custom_Function_Signal, name="Demod_5_LP_BW_Value", kind="config", metadata={"units": "Hz", "description": "Value of Integration Bandwidth"})
	Demod_5_LP_TC_Value = Cpt(Custom_Function_Signal, name="Demod_5_LP_TC_Value", kind="config", metadata={"units": "s", "description": "Value of Integration Time Constant"})
	Demod_5_Sinc = Cpt(Custom_Function_Signal, name="Demod_5_Sinc", kind="config", metadata={"units": "", "description": "Enable Sinc Filter"})
	Demod_5_Data_Trans = Cpt(Custom_Function_Signal, name="Demod_5_Data_Trans", kind="config", metadata={"units": "", "description": "Enable Data Transfer"})
	Demod_5_Data_Trans_Value = Cpt(Custom_Function_Signal, name="Demod_5_Data_Trans_Value", kind="config", metadata={"units": "Sa/s", "description": "Set sampling rate of Demodulator Samples/second"})
	Demod_5_Data_Trans_Trigger = Cpt(Custom_Function_Signal, name="Demod_5_Data_Trans_Trigger", kind="config", metadata={"units": "", "description": "Continous, Trigger Input 3, Trigger Input 4, Trigger Input 3/4"})
	
	Demod_6_Harmonics = Cpt(Custom_Function_Signal, name="Demod_6_Harmonics", kind="config", metadata={"units": "", "description": "Harmonic of Demodulator's Refrence Frequency"})
	Demod_6_Phase = Cpt(Custom_Function_Signal, name="Demod_6_Phase", kind="config", metadata={"units": "deg", "description": "Phase betweem Demodulator's Refrence Frequency and Output"})
	Demod_6_Input = Cpt(Custom_Function_Signal, name="Demod_6_Input", kind="config", metadata={"units": "", "description": "Input Signal Channel"})
	Demod_6_LP_Order = Cpt(Custom_Function_Signal, name="Demod_6_LP_Order", kind="config", metadata={"units": "", "description": "Order of Lowpass filter"})
	#Demod_6_LP_BW_TC = Cpt(Custom_Function_Signal, name="Demod_6_LP_BW_TC", kind="config", metadata={"units": "", "description": "Choose between TimeConstant, BandWidth at 3 dB or BandWidth at NoiseEquivalentPower"})
	#Demod_6_LP_BW_Value = Cpt(Custom_Function_Signal, name="Demod_6_LP_BW_Value", kind="config", metadata={"units": "Hz", "description": "Value of Integration Bandwidth"})
	Demod_6_LP_TC_Value = Cpt(Custom_Function_Signal, name="Demod_6_LP_TC_Value", kind="config", metadata={"units": "s", "description": "Value of Integration Time Constant"})
	Demod_6_Sinc = Cpt(Custom_Function_Signal, name="Demod_6_Sinc", kind="config", metadata={"units": "", "description": "Enable Sinc Filter"})
	Demod_6_Data_Trans = Cpt(Custom_Function_Signal, name="Demod_6_Data_Trans", kind="config", metadata={"units": "", "description": "Enable Data Transfer"})
	Demod_6_Data_Trans_Value = Cpt(Custom_Function_Signal, name="Demod_6_Data_Trans_Value", kind="config", metadata={"units": "Sa/s", "description": "Set sampling rate of Demodulator Samples/second"})
	Demod_6_Data_Trans_Trigger = Cpt(Custom_Function_Signal, name="Demod_6_Data_Trans_Trigger", kind="config", metadata={"units": "", "description": "Continous, Trigger Input 3, Trigger Input 4, Trigger Input 3/4"})
	
	Demod_7_Harmonics = Cpt(Custom_Function_Signal, name="Demod_7_Harmonics", kind="config", metadata={"units": "", "description": "Harmonic of Demodulator's Refrence Frequency"})
	Demod_7_Phase = Cpt(Custom_Function_Signal, name="Demod_7_Phase", kind="config", metadata={"units": "deg", "description": "Phase betweem Demodulator's Refrence Frequency and Output"})
	Demod_7_Input = Cpt(Custom_Function_Signal, name="Demod_7_Input", kind="config", metadata={"units": "", "description": "Input Signal Channel"})
	Demod_7_LP_Order = Cpt(Custom_Function_Signal, name="Demod_7_LP_Order", kind="config", metadata={"units": "", "description": "Order of Lowpass filter"})
	#Demod_7_LP_BW_TC = Cpt(Custom_Function_Signal, name="Demod_7_LP_BW_TC", kind="config", metadata={"units": "", "description": "Choose between TimeConstant, BandWidth at 3 dB or BandWidth at NoiseEquivalentPower"})
	#Demod_7_LP_BW_Value = Cpt(Custom_Function_Signal, name="Demod_7_LP_BW_Value", kind="config", metadata={"units": "Hz", "description": "Value of Integration Bandwidth"})
	Demod_7_LP_TC_Value = Cpt(Custom_Function_Signal, name="Demod_7_LP_TC_Value", kind="config", metadata={"units": "s", "description": "Value of Integration Time Constant"})
	Demod_7_Sinc = Cpt(Custom_Function_Signal, name="Demod_7_Sinc", kind="config", metadata={"units": "", "description": "Enable Sinc Filter"})
	Demod_7_Data_Trans = Cpt(Custom_Function_Signal, name="Demod_7_Data_Trans", kind="config", metadata={"units": "", "description": "Enable Data Transfer"})
	Demod_7_Data_Trans_Value = Cpt(Custom_Function_Signal, name="Demod_7_Data_Trans_Value", kind="config", metadata={"units": "Sa/s", "description": "Set sampling rate of Demodulator Samples/second"})
	Demod_7_Data_Trans_Trigger = Cpt(Custom_Function_Signal, name="Demod_7_Data_Trans_Trigger", kind="config", metadata={"units": "", "description": "Continous, Trigger Input 3, Trigger Input 4, Trigger Input 3/4"})
	
	Demod_8_Harmonics = Cpt(Custom_Function_Signal, name="Demod_8_Harmonics", kind="config", metadata={"units": "", "description": "Harmonic of Demodulator's Refrence Frequency"})
	Demod_8_Phase = Cpt(Custom_Function_Signal, name="Demod_8_Phase", kind="config", metadata={"units": "deg", "description": "Phase betweem Demodulator's Refrence Frequency and Output"})
	Demod_8_Input = Cpt(Custom_Function_Signal, name="Demod_8_Input", kind="config", metadata={"units": "", "description": "Input Signal Channel"})
	Demod_8_LP_Order = Cpt(Custom_Function_Signal, name="Demod_8_LP_Order", kind="config", metadata={"units": "", "description": "Order of Lowpass filter"})
	#Demod_8_LP_BW_TC = Cpt(Custom_Function_Signal, name="Demod_8_LP_BW_TC", kind="config", metadata={"units": "", "description": "Choose between TimeConstant, BandWidth at 3 dB or BandWidth at NoiseEquivalentPower"})
	#Demod_8_LP_BW_Value = Cpt(Custom_Function_Signal, name="Demod_8_LP_BW_Value", kind="config", metadata={"units": "Hz", "description": "Value of Integration Bandwidth"})
	Demod_8_LP_TC_Value = Cpt(Custom_Function_Signal, name="Demod_8_LP_TC_Value", kind="config", metadata={"units": "s", "description": "Value of Integration Time Constant"})
	Demod_8_Sinc = Cpt(Custom_Function_Signal, name="Demod_8_Sinc", kind="config", metadata={"units": "", "description": "Enable Sinc Filter"})
	Demod_8_Data_Trans = Cpt(Custom_Function_Signal, name="Demod_8_Data_Trans", kind="config", metadata={"units": "", "description": "Enable Data Transfer"})
	Demod_8_Data_Trans_Value = Cpt(Custom_Function_Signal, name="Demod_8_Data_Trans_Value", kind="config", metadata={"units": "Sa/s", "description": "Set sampling rate of Demodulator Samples/second"})
	Demod_8_Data_Trans_Trigger = Cpt(Custom_Function_Signal, name="Demod_8_Data_Trans_Trigger", kind="config", metadata={"units": "", "description": "Continous, Trigger Input 3, Trigger Input 4, Trigger Input 3/4"})

	Demod_1_X = Cpt(Custom_Function_SignalRO, name="Demod_1_X", metadata={"units": "", "description": "Read Demodulator 1"})
	Demod_1_Y = Cpt(Custom_Function_SignalRO, name="Demod_1_Y", metadata={"units": "", "description": "Read Demodulator 1"})
	Demod_1_timeStamp = Cpt(Custom_Function_SignalRO, name="Demod_1_timeStamp", metadata={"units": "", "description": "Read Demodulator 1"})
	Demod_1_frequency = Cpt(Custom_Function_SignalRO, name="Demod_1_frequency", metadata={"units": "", "description": "Read Demodulator 1"})
	Demod_1_dioBits = Cpt(Custom_Function_SignalRO, name="Demod_1_dioBits", metadata={"units": "", "description": "Read Demodulator 1"})
	Demod_1_phaseMeas = Cpt(Custom_Function_SignalRO, name="Demod_1_phaseMeas", metadata={"units": "", "description": "Read Demodulator 1"})
	Demod_1_trigger = Cpt(Custom_Function_SignalRO, name="Demod_1_trigger", metadata={"units": "", "description": "Read Demodulator 1"})
	Demod_1_AuxIn0 = Cpt(Custom_Function_SignalRO, name="Demod_1_AuxIn0", metadata={"units": "", "description": "Read Demodulator 1"})
	Demod_1_AuxIn1 = Cpt(Custom_Function_SignalRO, name="Demod_1_AuxIn1", metadata={"units": "", "description": "Read Demodulator 1"})

	Demod_2_X = Cpt(Custom_Function_SignalRO, name="Demod_2_X", metadata={"units": "", "description": "Read Demodulator 2"})
	Demod_2_Y = Cpt(Custom_Function_SignalRO, name="Demod_2_Y", metadata={"units": "", "description": "Read Demodulator 2"})
	Demod_2_timeStamp = Cpt(Custom_Function_SignalRO, name="Demod_2_timeStamp", metadata={"units": "", "description": "Read Demodulator 2"})
	Demod_2_frequency = Cpt(Custom_Function_SignalRO, name="Demod_2_frequency", metadata={"units": "", "description": "Read Demodulator 2"})
	Demod_2_dioBits = Cpt(Custom_Function_SignalRO, name="Demod_2_dioBits", metadata={"units": "", "description": "Read Demodulator 2"})
	Demod_2_phaseMeas = Cpt(Custom_Function_SignalRO, name="Demod_2_phaseMeas", metadata={"units": "", "description": "Read Demodulator 2"})
	Demod_2_trigger = Cpt(Custom_Function_SignalRO, name="Demod_2_trigger", metadata={"units": "", "description": "Read Demodulator 2"})
	Demod_2_AuxIn0 = Cpt(Custom_Function_SignalRO, name="Demod_2_AuxIn0", metadata={"units": "", "description": "Read Demodulator 2"})
	Demod_2_AuxIn1 = Cpt(Custom_Function_SignalRO, name="Demod_2_AuxIn1", metadata={"units": "", "description": "Read Demodulator 2"})

	Demod_3_X = Cpt(Custom_Function_SignalRO, name="Demod_3_X", metadata={"units": "", "description": "Read Demodulator 3"})
	Demod_3_Y = Cpt(Custom_Function_SignalRO, name="Demod_3_Y", metadata={"units": "", "description": "Read Demodulator 3"})
	Demod_3_timeStamp = Cpt(Custom_Function_SignalRO, name="Demod_3_timeStamp", metadata={"units": "", "description": "Read Demodulator 3"})
	Demod_3_frequency = Cpt(Custom_Function_SignalRO, name="Demod_3_frequency", metadata={"units": "", "description": "Read Demodulator 3"})
	Demod_3_dioBits = Cpt(Custom_Function_SignalRO, name="Demod_3_dioBits", metadata={"units": "", "description": "Read Demodulator 3"})
	Demod_3_phaseMeas = Cpt(Custom_Function_SignalRO, name="Demod_3_phaseMeas", metadata={"units": "", "description": "Read Demodulator 3"})
	Demod_3_trigger = Cpt(Custom_Function_SignalRO, name="Demod_3_trigger", metadata={"units": "", "description": "Read Demodulator 3"})
	Demod_3_AuxIn0 = Cpt(Custom_Function_SignalRO, name="Demod_3_AuxIn0", metadata={"units": "", "description": "Read Demodulator 3"})
	Demod_3_AuxIn1 = Cpt(Custom_Function_SignalRO, name="Demod_3_AuxIn1", metadata={"units": "", "description": "Read Demodulator 3"})

	Demod_4_X = Cpt(Custom_Function_SignalRO, name="Demod_4_X", metadata={"units": "", "description": "Read Demodulator 4"})
	Demod_4_Y = Cpt(Custom_Function_SignalRO, name="Demod_4_Y", metadata={"units": "", "description": "Read Demodulator 4"})
	Demod_4_timeStamp = Cpt(Custom_Function_SignalRO, name="Demod_4_timeStamp", metadata={"units": "", "description": "Read Demodulator 4"})
	Demod_4_frequency = Cpt(Custom_Function_SignalRO, name="Demod_4_frequency", metadata={"units": "", "description": "Read Demodulator 4"})
	Demod_4_dioBits = Cpt(Custom_Function_SignalRO, name="Demod_4_dioBits", metadata={"units": "", "description": "Read Demodulator 4"})
	Demod_4_phaseMeas = Cpt(Custom_Function_SignalRO, name="Demod_4_phaseMeas", metadata={"units": "", "description": "Read Demodulator 4"})
	Demod_4_trigger = Cpt(Custom_Function_SignalRO, name="Demod_4_trigger", metadata={"units": "", "description": "Read Demodulator 4"})
	Demod_4_AuxIn0 = Cpt(Custom_Function_SignalRO, name="Demod_4_AuxIn0", metadata={"units": "", "description": "Read Demodulator 4"})
	Demod_4_AuxIn1 = Cpt(Custom_Function_SignalRO, name="Demod_4_AuxIn1", metadata={"units": "", "description": "Read Demodulator 4"})

	Demod_5_X = Cpt(Custom_Function_SignalRO, name="Demod_5_X", metadata={"units": "", "description": "Read Demodulator 5"})
	Demod_5_Y = Cpt(Custom_Function_SignalRO, name="Demod_5_Y", metadata={"units": "", "description": "Read Demodulator 5"})
	Demod_5_timeStamp = Cpt(Custom_Function_SignalRO, name="Demod_5_timeStamp", metadata={"units": "", "description": "Read Demodulator 5"})
	Demod_5_frequency = Cpt(Custom_Function_SignalRO, name="Demod_5_frequency", metadata={"units": "", "description": "Read Demodulator 5"})
	Demod_5_dioBits = Cpt(Custom_Function_SignalRO, name="Demod_5_dioBits", metadata={"units": "", "description": "Read Demodulator 5"})
	Demod_5_phaseMeas = Cpt(Custom_Function_SignalRO, name="Demod_5_phaseMeas", metadata={"units": "", "description": "Read Demodulator 5"})
	Demod_5_trigger = Cpt(Custom_Function_SignalRO, name="Demod_5_trigger", metadata={"units": "", "description": "Read Demodulator 5"})
	Demod_5_AuxIn0 = Cpt(Custom_Function_SignalRO, name="Demod_5_AuxIn0", metadata={"units": "", "description": "Read Demodulator 5"})
	Demod_5_AuxIn1 = Cpt(Custom_Function_SignalRO, name="Demod_5_AuxIn1", metadata={"units": "", "description": "Read Demodulator 5"})

	Demod_6_X = Cpt(Custom_Function_SignalRO, name="Demod_6_X", metadata={"units": "", "description": "Read Demodulator 6"})
	Demod_6_Y = Cpt(Custom_Function_SignalRO, name="Demod_6_Y", metadata={"units": "", "description": "Read Demodulator 6"})
	Demod_6_timeStamp = Cpt(Custom_Function_SignalRO, name="Demod_6_timeStamp", metadata={"units": "", "description": "Read Demodulator 6"})
	Demod_6_frequency = Cpt(Custom_Function_SignalRO, name="Demod_6_frequency", metadata={"units": "", "description": "Read Demodulator 6"})
	Demod_6_dioBits = Cpt(Custom_Function_SignalRO, name="Demod_6_dioBits", metadata={"units": "", "description": "Read Demodulator 6"})
	Demod_6_phaseMeas = Cpt(Custom_Function_SignalRO, name="Demod_6_phaseMeas", metadata={"units": "", "description": "Read Demodulator 6"})
	Demod_6_trigger = Cpt(Custom_Function_SignalRO, name="Demod_6_trigger", metadata={"units": "", "description": "Read Demodulator 6"})
	Demod_6_AuxIn0 = Cpt(Custom_Function_SignalRO, name="Demod_6_AuxIn0", metadata={"units": "", "description": "Read Demodulator 6"})
	Demod_6_AuxIn1 = Cpt(Custom_Function_SignalRO, name="Demod_6_AuxIn1", metadata={"units": "", "description": "Read Demodulator 6"})

	Demod_7_X = Cpt(Custom_Function_SignalRO, name="Demod_7_X", metadata={"units": "", "description": "Read Demodulator 7"})
	Demod_7_Y = Cpt(Custom_Function_SignalRO, name="Demod_7_Y", metadata={"units": "", "description": "Read Demodulator 7"})
	Demod_7_timeStamp = Cpt(Custom_Function_SignalRO, name="Demod_7_timeStamp", metadata={"units": "", "description": "Read Demodulator 7"})
	Demod_7_frequency = Cpt(Custom_Function_SignalRO, name="Demod_7_frequency", metadata={"units": "", "description": "Read Demodulator 7"})
	Demod_7_dioBits = Cpt(Custom_Function_SignalRO, name="Demod_7_dioBits", metadata={"units": "", "description": "Read Demodulator 7"})
	Demod_7_phaseMeas = Cpt(Custom_Function_SignalRO, name="Demod_7_phaseMeas", metadata={"units": "", "description": "Read Demodulator 7"})
	Demod_7_trigger = Cpt(Custom_Function_SignalRO, name="Demod_7_trigger", metadata={"units": "", "description": "Read Demodulator 7"})
	Demod_7_AuxIn0 = Cpt(Custom_Function_SignalRO, name="Demod_7_AuxIn0", metadata={"units": "", "description": "Read Demodulator 7"})
	Demod_7_AuxIn1 = Cpt(Custom_Function_SignalRO, name="Demod_7_AuxIn1", metadata={"units": "", "description": "Read Demodulator 7"})

	Demod_8_X = Cpt(Custom_Function_SignalRO, name="Demod_8_X", metadata={"units": "", "description": "Read Demodulator 8"})
	Demod_8_Y = Cpt(Custom_Function_SignalRO, name="Demod_8_Y", metadata={"units": "", "description": "Read Demodulator 8"})
	Demod_8_timeStamp = Cpt(Custom_Function_SignalRO, name="Demod_8_timeStamp", metadata={"units": "", "description": "Read Demodulator 8"})
	Demod_8_frequency = Cpt(Custom_Function_SignalRO, name="Demod_8_frequency", metadata={"units": "", "description": "Read Demodulator 8"})
	Demod_8_dioBits = Cpt(Custom_Function_SignalRO, name="Demod_8_dioBits", metadata={"units": "", "description": "Read Demodulator 8"})
	Demod_8_phaseMeas = Cpt(Custom_Function_SignalRO, name="Demod_8_phaseMeas", metadata={"units": "", "description": "Read Demodulator 8"})
	Demod_8_trigger = Cpt(Custom_Function_SignalRO, name="Demod_8_trigger", metadata={"units": "", "description": "Read Demodulator 8"})
	Demod_8_AuxIn0 = Cpt(Custom_Function_SignalRO, name="Demod_8_AuxIn0", metadata={"units": "", "description": "Read Demodulator 8"})
	Demod_8_AuxIn1 = Cpt(Custom_Function_SignalRO, name="Demod_8_AuxIn1", metadata={"units": "", "description": "Read Demodulator 8"})



	
	
	
	def __init__(self, prefix="", *, name, kind=None, read_attrs=None, configuration_attrs=None, parent=None, port_number=0, serial_number='', connection_type='USB', **kwargs):
		super().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs, configuration_attrs=configuration_attrs, parent=parent, **kwargs)
		self.Out_1.put_function = lambda value, n=1: self.Out_put_function(value, n)
		self.Out_2.put_function = lambda value, n=2: self.Out_put_function(value, n)

		self.Out_1_50_Ohm.put_function = lambda value, n=1: self.Out_50_Ohm_put_function(value, n)
		self.Out_2_50_Ohm.put_function = lambda value, n=2: self.Out_50_Ohm_put_function(value, n)

		self.Out_1_Range.put_function = lambda value, n=1: self.Out_Range_put_function(value, n)
		self.Out_2_Range.put_function = lambda value, n=2: self.Out_Range_put_function(value, n)

		self.Out_1_Offset.put_function = lambda value, n=1: self.Out_Offset_put_function(value, n)
		self.Out_2_Offset.put_function = lambda value, n=2: self.Out_Offset_put_function(value, n)

		#self.Out_1_Amp_Type.put_function = self.Out_1_Amp_Type_put_function

		self.Out_1_Amp_Value.put_function = lambda value, n=1: self.Out_Amp_Value_put_function(value, n)
		self.Out_2_Amp_Value.put_function = lambda value, n=2: self.Out_Amp_Value_put_function(value, n)

		self.Out_1_Amp.put_function = lambda value, n=1: self.Out_Amp_put_function(value, n)
		self.Out_2_Amp.put_function = lambda value, n=2: self.Out_Amp_put_function(value, n)

		self.In_1_Range.put_function = lambda value, n=1: self.In_Range_put_function(value, n)
		self.In_2_Range.put_function = lambda value, n=2: self.In_Range_put_function(value, n)

		self.In_1_Scaling_Value.put_function = lambda value, n=1: self.In_Scaling_Value_put_function(value, n)
		self.In_2_Scaling_Value.put_function = lambda value, n=2: self.In_Scaling_Value_put_function(value, n)

		self.In_1_AC.put_function = lambda value, n=1: self.In_AC_put_function(value, n)
		self.In_2_AC.put_function = lambda value, n=2: self.In_AC_put_function(value, n)

		self.In_1_50_Ohm.put_function = lambda value, n=1: self.In_50_Ohm_put_function(value, n)
		self.In_2_50_Ohm.put_function = lambda value, n=2: self.In_50_Ohm_put_function(value, n)
		
		self.In_1_Diff.put_function = lambda value, n=1: self.In_Diff_put_function(value, n)
		self.In_2_Diff.put_function = lambda value, n=2: self.In_Diff_put_function(value, n)
		

		self.Osc_1_Frequency.put_function = lambda value, n=1: self.Osc_Frequency_put_function(value, n)
		self.Osc_2_Frequency.put_function = lambda value, n=2: self.Osc_Frequency_put_function(value, n)
		
		self.Demod_4_Mode.put_function = lambda value, n=1: self.Demod_Mode_put_function(value, n)
		self.Demod_8_Mode.put_function = lambda value, n=2: self.Demod_Mode_put_function(value, n)

		self.Demod_1_Harmonics.put_function = lambda value, n=1: self.Demod_Harmonics_put_function(value, n)
		self.Demod_1_Phase.put_function = lambda value, n=1: self.Demod_Phase_put_function(value, n)
		self.Demod_1_Input.put_function = lambda value, n=1: self.Demod_Input_put_function(value, n)
		self.Demod_1_LP_Order.put_function = lambda value, n=1: self.Demod_LP_Order_put_function(value, n)
		#self.Demod_1_LP_BW_TC.put_function = lambda value, n=1: self.Demod_LP_BW_TC_put_function(value, n)
		#self.Demod_1_LP_BW_Value.put_function = lambda value, n=1: self.Demod_LP_BW_Value_put_function(value, n)
		self.Demod_1_LP_TC_Value.put_function = lambda value, n=1: self.Demod_LP_TC_Value_put_function(value, n)
		self.Demod_1_Sinc.put_function = lambda value, n=1: self.Demod_Sinc_put_function(value, n)
		self.Demod_1_Data_Trans.put_function = lambda value, n=1: self.Demod_Data_Trans_put_function(value, n)
		self.Demod_1_Data_Trans_Value.put_function = lambda value, n=1: self.Demod_Data_Trans_Value_put_function(value, n)
		self.Demod_1_Data_Trans_Trigger.put_function = lambda value, n=1: self.Demod_Data_Trans_Trigger_put_function(value, n)

		self.Demod_2_Harmonics.put_function = lambda value, n=2: self.Demod_Harmonics_put_function(value, n)
		self.Demod_2_Phase.put_function = lambda value, n=2: self.Demod_Phase_put_function(value, n)
		self.Demod_2_Input.put_function = lambda value, n=2: self.Demod_Input_put_function(value, n)
		self.Demod_2_LP_Order.put_function = lambda value, n=2: self.Demod_LP_Order_put_function(value, n)
		#self.Demod_2_LP_BW_TC.put_function = lambda value, n=2: self.Demod_LP_BW_TC_put_function(value, n)
		#self.Demod_2_LP_BW_Value.put_function = lambda value, n=2: self.Demod_LP_BW_Value_put_function(value, n)
		self.Demod_2_LP_TC_Value.put_function = lambda value, n=2: self.Demod_LP_TC_Value_put_function(value, n)
		self.Demod_2_Sinc.put_function = lambda value, n=2: self.Demod_Sinc_put_function(value, n)
		self.Demod_2_Data_Trans.put_function = lambda value, n=2: self.Demod_Data_Trans_put_function(value, n)
		self.Demod_2_Data_Trans_Value.put_function = lambda value, n=2: self.Demod_Data_Trans_Value_put_function(value, n)
		self.Demod_2_Data_Trans_Trigger.put_function = lambda value, n=2: self.Demod_Data_Trans_Trigger_put_function(value, n)

		self.Demod_3_Harmonics.put_function = lambda value, n=3: self.Demod_Harmonics_put_function(value, n)
		self.Demod_3_Phase.put_function = lambda value, n=3: self.Demod_Phase_put_function(value, n)
		self.Demod_3_Input.put_function = lambda value, n=3: self.Demod_Input_put_function(value, n)
		self.Demod_3_LP_Order.put_function = lambda value, n=3: self.Demod_LP_Order_put_function(value, n)
		#self.Demod_3_LP_BW_TC.put_function = lambda value, n=3: self.Demod_LP_BW_TC_put_function(value, n)
		#self.Demod_3_LP_BW_Value.put_function = lambda value, n=3: self.Demod_LP_BW_Value_put_function(value, n)
		self.Demod_3_LP_TC_Value.put_function = lambda value, n=3: self.Demod_LP_TC_Value_put_function(value, n)
		self.Demod_3_Sinc.put_function = lambda value, n=3: self.Demod_Sinc_put_function(value, n)
		self.Demod_3_Data_Trans.put_function = lambda value, n=3: self.Demod_Data_Trans_put_function(value, n)
		self.Demod_3_Data_Trans_Value.put_function = lambda value, n=3: self.Demod_Data_Trans_Value_put_function(value, n)
		self.Demod_3_Data_Trans_Trigger.put_function = lambda value, n=3: self.Demod_Data_Trans_Trigger_put_function(value, n)

		self.Demod_4_Harmonics.put_function = lambda value, n=4: self.Demod_Harmonics_put_function(value, n)
		self.Demod_4_Phase.put_function = lambda value, n=4: self.Demod_Phase_put_function(value, n)
		self.Demod_4_Input.put_function = lambda value, n=4: self.Demod_Input_put_function(value, n)
		self.Demod_4_LP_Order.put_function = lambda value, n=4: self.Demod_LP_Order_put_function(value, n)
		#self.Demod_4_LP_BW_TC.put_function = lambda value, n=4: self.Demod_LP_BW_TC_put_function(value, n)
		#self.Demod_4_LP_BW_Value.put_function = lambda value, n=4: self.Demod_LP_BW_Value_put_function(value, n)
		self.Demod_4_LP_TC_Value.put_function = lambda value, n=4: self.Demod_LP_TC_Value_put_function(value, n)
		self.Demod_4_Sinc.put_function = lambda value, n=4: self.Demod_Sinc_put_function(value, n)
		self.Demod_4_Data_Trans.put_function = lambda value, n=4: self.Demod_Data_Trans_put_function(value, n)
		self.Demod_4_Data_Trans_Value.put_function = lambda value, n=4: self.Demod_Data_Trans_Value_put_function(value, n)
		self.Demod_4_Data_Trans_Trigger.put_function = lambda value, n=4: self.Demod_Data_Trans_Trigger_put_function(value, n)

		self.Demod_5_Harmonics.put_function = lambda value, n=5: self.Demod_Harmonics_put_function(value, n)
		self.Demod_5_Phase.put_function = lambda value, n=5: self.Demod_Phase_put_function(value, n)
		self.Demod_5_Input.put_function = lambda value, n=5: self.Demod_Input_put_function(value, n)
		self.Demod_5_LP_Order.put_function = lambda value, n=5: self.Demod_LP_Order_put_function(value, n)
		#self.Demod_5_LP_BW_TC.put_function = lambda value, n=5: self.Demod_LP_BW_TC_put_function(value, n)
		#self.Demod_5_LP_BW_Value.put_function = lambda value, n=5: self.Demod_LP_BW_Value_put_function(value, n)
		self.Demod_5_LP_TC_Value.put_function = lambda value, n=5: self.Demod_LP_TC_Value_put_function(value, n)
		self.Demod_5_Sinc.put_function = lambda value, n=5: self.Demod_Sinc_put_function(value, n)
		self.Demod_5_Data_Trans.put_function = lambda value, n=5: self.Demod_Data_Trans_put_function(value, n)
		self.Demod_5_Data_Trans_Value.put_function = lambda value, n=5: self.Demod_Data_Trans_Value_put_function(value, n)
		self.Demod_5_Data_Trans_Trigger.put_function = lambda value, n=5: self.Demod_Data_Trans_Trigger_put_function(value, n)

		self.Demod_6_Harmonics.put_function = lambda value, n=6: self.Demod_Harmonics_put_function(value, n)
		self.Demod_6_Phase.put_function = lambda value, n=6: self.Demod_Phase_put_function(value, n)
		self.Demod_6_Input.put_function = lambda value, n=6: self.Demod_Input_put_function(value, n)
		self.Demod_6_LP_Order.put_function = lambda value, n=6: self.Demod_LP_Order_put_function(value, n)
		#self.Demod_6_LP_BW_TC.put_function = lambda value, n=6: self.Demod_LP_BW_TC_put_function(value, n)
		#self.Demod_6_LP_BW_Value.put_function = lambda value, n=6: self.Demod_LP_BW_Value_put_function(value, n)
		self.Demod_6_LP_TC_Value.put_function = lambda value, n=6: self.Demod_LP_TC_Value_put_function(value, n)
		self.Demod_6_Sinc.put_function = lambda value, n=6: self.Demod_Sinc_put_function(value, n)
		self.Demod_6_Data_Trans.put_function = lambda value, n=6: self.Demod_Data_Trans_put_function(value, n)
		self.Demod_6_Data_Trans_Value.put_function = lambda value, n=6: self.Demod_Data_Trans_Value_put_function(value, n)
		self.Demod_6_Data_Trans_Trigger.put_function = lambda value, n=6: self.Demod_Data_Trans_Trigger_put_function(value, n)

		self.Demod_7_Harmonics.put_function = lambda value, n=7: self.Demod_Harmonics_put_function(value, n)
		self.Demod_7_Phase.put_function = lambda value, n=7: self.Demod_Phase_put_function(value, n)
		self.Demod_7_Input.put_function = lambda value, n=7: self.Demod_Input_put_function(value, n)
		self.Demod_7_LP_Order.put_function = lambda value, n=7: self.Demod_LP_Order_put_function(value, n)
		#self.Demod_7_LP_BW_TC.put_function = lambda value, n=7: self.Demod_LP_BW_TC_put_function(value, n)
		#self.Demod_7_LP_BW_Value.put_function = lambda value, n=7: self.Demod_LP_BW_Value_put_function(value, n)
		self.Demod_7_LP_TC_Value.put_function = lambda value, n=7: self.Demod_LP_TC_Value_put_function(value, n)
		self.Demod_7_Sinc.put_function = lambda value, n=7: self.Demod_Sinc_put_function(value, n)
		self.Demod_7_Data_Trans.put_function = lambda value, n=7: self.Demod_Data_Trans_put_function(value, n)
		self.Demod_7_Data_Trans_Value.put_function = lambda value, n=7: self.Demod_Data_Trans_Value_put_function(value, n)
		self.Demod_7_Data_Trans_Trigger.put_function = lambda value, n=7: self.Demod_Data_Trans_Trigger_put_function(value, n)

		self.Demod_8_Harmonics.put_function = lambda value, n=8: self.Demod_Harmonics_put_function(value, n)
		self.Demod_8_Phase.put_function = lambda value, n=8: self.Demod_Phase_put_function(value, n)
		self.Demod_8_Input.put_function = lambda value, n=8: self.Demod_Input_put_function(value, n)
		self.Demod_8_LP_Order.put_function = lambda value, n=8: self.Demod_LP_Order_put_function(value, n)
		#self.Demod_8_LP_BW_TC.put_function = lambda value, n=8: self.Demod_LP_BW_TC_put_function(value, n)
		#self.Demod_8_LP_BW_Value.put_function = lambda value, n=8: self.Demod_LP_BW_Value_put_function(value, n)
		self.Demod_8_LP_TC_Value.put_function = lambda value, n=8: self.Demod_LP_TC_Value_put_function(value, n)
		self.Demod_8_Sinc.put_function = lambda value, n=8: self.Demod_Sinc_put_function(value, n)
		self.Demod_8_Data_Trans.put_function = lambda value, n=8: self.Demod_Data_Trans_put_function(value, n)
		self.Demod_8_Data_Trans_Value.put_function = lambda value, n=8: self.Demod_Data_Trans_Value_put_function(value, n)
		self.Demod_8_Data_Trans_Trigger.put_function = lambda value, n=8: self.Demod_Data_Trans_Trigger_put_function(value, n)


#read functions
		self.Demod_1_X.read_function = lambda n=1: self.Demod_Read_Data_X_read_function(n)
		self.Demod_1_X.trigger_function = lambda n=1: self.Demod_Read_Data_trigger_function(n)

		self.Demod_1_Y.read_function = lambda n=1: self.Demod_Read_Data_Y_read_function(n)		
		self.Demod_1_Y.trigger_function = lambda n=1: self.Demod_Read_Data_trigger_function(n)

		self.Demod_1_phaseMeas.read_function = lambda n=1: self.Demod_Read_Data_Y_read_function(n)
		self.Demod_1_phaseMeas.trigger_function = lambda n=1: self.Demod_Read_Data_trigger_function(n)

		self.Demod_1_timeStamp.read_function = lambda n=1: self.Demod_Read_Data_timeStamp_read_function(n)
		self.Demod_1_phaseMeas.trigger_function = lambda n=1: self.Demod_Read_Data_trigger_function(n)

		self.Demod_1_frequency.read_function = lambda n=1: self.Demod_Read_Data_frequency_read_function(n)
		self.Demod_1_frequency.trigger_function = lambda n=1: self.Demod_Read_Data_trigger_function(n)

		self.Demod_1_dioBits.read_function = lambda n=1: self.Demod_Read_Data_dioBits_read_function(n)
		self.Demod_1_dioBits.trigger_function = lambda n=1: self.Demod_Read_Data_trigger_function(n)

		self.Demod_1_trigger.read_function = lambda n=1: self.Demod_Read_Data_trigger_read_function(n)
		self.Demod_1_trigger.trigger_function = lambda n=1: self.Demod_Read_Data_trigger_function(n)

		self.Demod_1_AuxIn0.read_function = lambda n=1: self.Demod_Read_Data_AuxIn0_read_function(n)
		self.Demod_1_AuxIn0.trigger_function = lambda n=1: self.Demod_Read_Data_trigger_function(n)

		self.Demod_1_AuxIn1.read_function = lambda n=1: self.Demod_Read_Data_AuxIn1_read_function(n)
		self.Demod_1_AuxIn1.trigger_function = lambda n=1: self.Demod_Read_Data_trigger_function(n)



		self.Demod_2_X.read_function = lambda n=2: self.Demod_Read_Data_X_read_function(n)
		self.Demod_2_X.trigger_function = lambda n=2: self.Demod_Read_Data_trigger_function(n)

		self.Demod_2_Y.read_function = lambda n=2: self.Demod_Read_Data_Y_read_function(n)		
		self.Demod_2_Y.trigger_function = lambda n=2: self.Demod_Read_Data_trigger_function(n)

		self.Demod_2_phaseMeas.read_function = lambda n=2: self.Demod_Read_Data_Y_read_function(n)
		self.Demod_2_phaseMeas.trigger_function = lambda n=2: self.Demod_Read_Data_trigger_function(n)

		self.Demod_2_timeStamp.read_function = lambda n=2: self.Demod_Read_Data_timeStamp_read_function(n)
		self.Demod_2_phaseMeas.trigger_function = lambda n=2: self.Demod_Read_Data_trigger_function(n)

		self.Demod_2_frequency.read_function = lambda n=2: self.Demod_Read_Data_frequency_read_function(n)
		self.Demod_2_frequency.trigger_function = lambda n=2: self.Demod_Read_Data_trigger_function(n)

		self.Demod_2_dioBits.read_function = lambda n=2: self.Demod_Read_Data_dioBits_read_function(n)
		self.Demod_2_dioBits.trigger_function = lambda n=2: self.Demod_Read_Data_trigger_function(n)

		self.Demod_2_trigger.read_function = lambda n=2: self.Demod_Read_Data_trigger_read_function(n)
		self.Demod_2_trigger.trigger_function = lambda n=2: self.Demod_Read_Data_trigger_function(n)

		self.Demod_2_AuxIn0.read_function = lambda n=2: self.Demod_Read_Data_AuxIn0_read_function(n)
		self.Demod_2_AuxIn0.trigger_function = lambda n=2: self.Demod_Read_Data_trigger_function(n)

		self.Demod_2_AuxIn1.read_function = lambda n=2: self.Demod_Read_Data_AuxIn1_read_function(n)
		self.Demod_2_AuxIn1.trigger_function = lambda n=2: self.Demod_Read_Data_trigger_function(n)



		self.Demod_3_X.read_function = lambda n=3: self.Demod_Read_Data_X_read_function(n)
		self.Demod_3_X.trigger_function = lambda n=3: self.Demod_Read_Data_trigger_function(n)

		self.Demod_3_Y.read_function = lambda n=3: self.Demod_Read_Data_Y_read_function(n)		
		self.Demod_3_Y.trigger_function = lambda n=3: self.Demod_Read_Data_trigger_function(n)

		self.Demod_3_phaseMeas.read_function = lambda n=3: self.Demod_Read_Data_Y_read_function(n)
		self.Demod_3_phaseMeas.trigger_function = lambda n=3: self.Demod_Read_Data_trigger_function(n)

		self.Demod_3_timeStamp.read_function = lambda n=3: self.Demod_Read_Data_timeStamp_read_function(n)
		self.Demod_3_phaseMeas.trigger_function = lambda n=3: self.Demod_Read_Data_trigger_function(n)

		self.Demod_3_frequency.read_function = lambda n=3: self.Demod_Read_Data_frequency_read_function(n)
		self.Demod_3_frequency.trigger_function = lambda n=3: self.Demod_Read_Data_trigger_function(n)

		self.Demod_3_dioBits.read_function = lambda n=3: self.Demod_Read_Data_dioBits_read_function(n)
		self.Demod_3_dioBits.trigger_function = lambda n=3: self.Demod_Read_Data_trigger_function(n)

		self.Demod_3_trigger.read_function = lambda n=3: self.Demod_Read_Data_trigger_read_function(n)
		self.Demod_3_trigger.trigger_function = lambda n=3: self.Demod_Read_Data_trigger_function(n)

		self.Demod_3_AuxIn0.read_function = lambda n=3: self.Demod_Read_Data_AuxIn0_read_function(n)
		self.Demod_3_AuxIn0.trigger_function = lambda n=3: self.Demod_Read_Data_trigger_function(n)

		self.Demod_3_AuxIn1.read_function = lambda n=3: self.Demod_Read_Data_AuxIn1_read_function(n)
		self.Demod_3_AuxIn1.trigger_function = lambda n=3: self.Demod_Read_Data_trigger_function(n)



		self.Demod_4_X.read_function = lambda n=4: self.Demod_Read_Data_X_read_function(n)
		self.Demod_4_X.trigger_function = lambda n=4: self.Demod_Read_Data_trigger_function(n)

		self.Demod_4_Y.read_function = lambda n=4: self.Demod_Read_Data_Y_read_function(n)		
		self.Demod_4_Y.trigger_function = lambda n=4: self.Demod_Read_Data_trigger_function(n)

		self.Demod_4_phaseMeas.read_function = lambda n=4: self.Demod_Read_Data_Y_read_function(n)
		self.Demod_4_phaseMeas.trigger_function = lambda n=4: self.Demod_Read_Data_trigger_function(n)

		self.Demod_4_timeStamp.read_function = lambda n=4: self.Demod_Read_Data_timeStamp_read_function(n)
		self.Demod_4_phaseMeas.trigger_function = lambda n=4: self.Demod_Read_Data_trigger_function(n)

		self.Demod_4_frequency.read_function = lambda n=4: self.Demod_Read_Data_frequency_read_function(n)
		self.Demod_4_frequency.trigger_function = lambda n=4: self.Demod_Read_Data_trigger_function(n)

		self.Demod_4_dioBits.read_function = lambda n=4: self.Demod_Read_Data_dioBits_read_function(n)
		self.Demod_4_dioBits.trigger_function = lambda n=4: self.Demod_Read_Data_trigger_function(n)

		self.Demod_4_trigger.read_function = lambda n=4: self.Demod_Read_Data_trigger_read_function(n)
		self.Demod_4_trigger.trigger_function = lambda n=4: self.Demod_Read_Data_trigger_function(n)

		self.Demod_4_AuxIn0.read_function = lambda n=4: self.Demod_Read_Data_AuxIn0_read_function(n)
		self.Demod_4_AuxIn0.trigger_function = lambda n=4: self.Demod_Read_Data_trigger_function(n)

		self.Demod_4_AuxIn1.read_function = lambda n=4: self.Demod_Read_Data_AuxIn1_read_function(n)
		self.Demod_4_AuxIn1.trigger_function = lambda n=4: self.Demod_Read_Data_trigger_function(n)



		self.Demod_5_X.read_function = lambda n=5: self.Demod_Read_Data_X_read_function(n)
		self.Demod_5_X.trigger_function = lambda n=5: self.Demod_Read_Data_trigger_function(n)

		self.Demod_5_Y.read_function = lambda n=5: self.Demod_Read_Data_Y_read_function(n)		
		self.Demod_5_Y.trigger_function = lambda n=5: self.Demod_Read_Data_trigger_function(n)

		self.Demod_5_phaseMeas.read_function = lambda n=5: self.Demod_Read_Data_Y_read_function(n)
		self.Demod_5_phaseMeas.trigger_function = lambda n=5: self.Demod_Read_Data_trigger_function(n)

		self.Demod_5_timeStamp.read_function = lambda n=5: self.Demod_Read_Data_timeStamp_read_function(n)
		self.Demod_5_phaseMeas.trigger_function = lambda n=5: self.Demod_Read_Data_trigger_function(n)

		self.Demod_5_frequency.read_function = lambda n=5: self.Demod_Read_Data_frequency_read_function(n)
		self.Demod_5_frequency.trigger_function = lambda n=5: self.Demod_Read_Data_trigger_function(n)

		self.Demod_5_dioBits.read_function = lambda n=5: self.Demod_Read_Data_dioBits_read_function(n)
		self.Demod_5_dioBits.trigger_function = lambda n=5: self.Demod_Read_Data_trigger_function(n)

		self.Demod_5_trigger.read_function = lambda n=5: self.Demod_Read_Data_trigger_read_function(n)
		self.Demod_5_trigger.trigger_function = lambda n=5: self.Demod_Read_Data_trigger_function(n)

		self.Demod_5_AuxIn0.read_function = lambda n=5: self.Demod_Read_Data_AuxIn0_read_function(n)
		self.Demod_5_AuxIn0.trigger_function = lambda n=5: self.Demod_Read_Data_trigger_function(n)

		self.Demod_5_AuxIn1.read_function = lambda n=5: self.Demod_Read_Data_AuxIn1_read_function(n)
		self.Demod_5_AuxIn1.trigger_function = lambda n=5: self.Demod_Read_Data_trigger_function(n)



		self.Demod_6_X.read_function = lambda n=6: self.Demod_Read_Data_X_read_function(n)
		self.Demod_6_X.trigger_function = lambda n=6: self.Demod_Read_Data_trigger_function(n)

		self.Demod_6_Y.read_function = lambda n=6: self.Demod_Read_Data_Y_read_function(n)		
		self.Demod_6_Y.trigger_function = lambda n=6: self.Demod_Read_Data_trigger_function(n)

		self.Demod_6_phaseMeas.read_function = lambda n=6: self.Demod_Read_Data_Y_read_function(n)
		self.Demod_6_phaseMeas.trigger_function = lambda n=6: self.Demod_Read_Data_trigger_function(n)

		self.Demod_6_timeStamp.read_function = lambda n=6: self.Demod_Read_Data_timeStamp_read_function(n)
		self.Demod_6_phaseMeas.trigger_function = lambda n=6: self.Demod_Read_Data_trigger_function(n)

		self.Demod_6_frequency.read_function = lambda n=6: self.Demod_Read_Data_frequency_read_function(n)
		self.Demod_6_frequency.trigger_function = lambda n=6: self.Demod_Read_Data_trigger_function(n)

		self.Demod_6_dioBits.read_function = lambda n=6: self.Demod_Read_Data_dioBits_read_function(n)
		self.Demod_6_dioBits.trigger_function = lambda n=6: self.Demod_Read_Data_trigger_function(n)

		self.Demod_6_trigger.read_function = lambda n=6: self.Demod_Read_Data_trigger_read_function(n)
		self.Demod_6_trigger.trigger_function = lambda n=6: self.Demod_Read_Data_trigger_function(n)

		self.Demod_6_AuxIn0.read_function = lambda n=6: self.Demod_Read_Data_AuxIn0_read_function(n)
		self.Demod_6_AuxIn0.trigger_function = lambda n=6: self.Demod_Read_Data_trigger_function(n)

		self.Demod_6_AuxIn1.read_function = lambda n=6: self.Demod_Read_Data_AuxIn1_read_function(n)
		self.Demod_6_AuxIn1.trigger_function = lambda n=6: self.Demod_Read_Data_trigger_function(n)



		self.Demod_7_X.read_function = lambda n=7: self.Demod_Read_Data_X_read_function(n)
		self.Demod_7_X.trigger_function = lambda n=7: self.Demod_Read_Data_trigger_function(n)

		self.Demod_7_Y.read_function = lambda n=7: self.Demod_Read_Data_Y_read_function(n)		
		self.Demod_7_Y.trigger_function = lambda n=7: self.Demod_Read_Data_trigger_function(n)

		self.Demod_7_phaseMeas.read_function = lambda n=7: self.Demod_Read_Data_Y_read_function(n)
		self.Demod_7_phaseMeas.trigger_function = lambda n=7: self.Demod_Read_Data_trigger_function(n)

		self.Demod_7_timeStamp.read_function = lambda n=7: self.Demod_Read_Data_timeStamp_read_function(n)
		self.Demod_7_phaseMeas.trigger_function = lambda n=7: self.Demod_Read_Data_trigger_function(n)

		self.Demod_7_frequency.read_function = lambda n=7: self.Demod_Read_Data_frequency_read_function(n)
		self.Demod_7_frequency.trigger_function = lambda n=7: self.Demod_Read_Data_trigger_function(n)

		self.Demod_7_dioBits.read_function = lambda n=7: self.Demod_Read_Data_dioBits_read_function(n)
		self.Demod_7_dioBits.trigger_function = lambda n=7: self.Demod_Read_Data_trigger_function(n)

		self.Demod_7_trigger.read_function = lambda n=7: self.Demod_Read_Data_trigger_read_function(n)
		self.Demod_7_trigger.trigger_function = lambda n=7: self.Demod_Read_Data_trigger_function(n)

		self.Demod_7_AuxIn0.read_function = lambda n=7: self.Demod_Read_Data_AuxIn0_read_function(n)
		self.Demod_7_AuxIn0.trigger_function = lambda n=7: self.Demod_Read_Data_trigger_function(n)

		self.Demod_7_AuxIn1.read_function = lambda n=7: self.Demod_Read_Data_AuxIn1_read_function(n)
		self.Demod_7_AuxIn1.trigger_function = lambda n=7: self.Demod_Read_Data_trigger_function(n)



		self.Demod_8_X.read_function = lambda n=8: self.Demod_Read_Data_X_read_function(n)
		self.Demod_8_X.trigger_function = lambda n=8: self.Demod_Read_Data_trigger_function(n)

		self.Demod_8_Y.read_function = lambda n=8: self.Demod_Read_Data_Y_read_function(n)		
		self.Demod_8_Y.trigger_function = lambda n=8: self.Demod_Read_Data_trigger_function(n)

		self.Demod_8_phaseMeas.read_function = lambda n=8: self.Demod_Read_Data_Y_read_function(n)
		self.Demod_8_phaseMeas.trigger_function = lambda n=8: self.Demod_Read_Data_trigger_function(n)

		self.Demod_8_timeStamp.read_function = lambda n=8: self.Demod_Read_Data_timeStamp_read_function(n)
		self.Demod_8_phaseMeas.trigger_function = lambda n=8: self.Demod_Read_Data_trigger_function(n)

		self.Demod_8_frequency.read_function = lambda n=8: self.Demod_Read_Data_frequency_read_function(n)
		self.Demod_8_frequency.trigger_function = lambda n=8: self.Demod_Read_Data_trigger_function(n)

		self.Demod_8_dioBits.read_function = lambda n=8: self.Demod_Read_Data_dioBits_read_function(n)
		self.Demod_8_dioBits.trigger_function = lambda n=8: self.Demod_Read_Data_trigger_function(n)

		self.Demod_8_trigger.read_function = lambda n=8: self.Demod_Read_Data_trigger_read_function(n)
		self.Demod_8_trigger.trigger_function = lambda n=8: self.Demod_Read_Data_trigger_function(n)

		self.Demod_8_AuxIn0.read_function = lambda n=8: self.Demod_Read_Data_AuxIn0_read_function(n)
		self.Demod_8_AuxIn0.trigger_function = lambda n=8: self.Demod_Read_Data_trigger_function(n)

		self.Demod_8_AuxIn1.read_function = lambda n=8: self.Demod_Read_Data_AuxIn1_read_function(n)
		self.Demod_8_AuxIn1.trigger_function = lambda n=8: self.Demod_Read_Data_trigger_function(n)

		self._last_measurement = [0] * 8
		self._was_triggered = [0] * 8

		if name != "test":
			self.daq = ziDAQServer("localhost", port_number, 6)
			self.daq.connectDevice(serial_number, connection_type)

	def Out_put_function(self, value, channel):
		if value:
			val = 1
		else:
			val = 0
		self.daq.setInt(f'/dev2901/sigouts/{channel-1}/on', val)

	def Out_50_Ohm_put_function(self, value, channel):
		if value:
			val = 1
		else:
			val = 0
		self.daq.setInt(f'/dev2901/sigouts/{channel-1}/imp50', val)

	def Out_Range_put_function(self, value, channel):
		if value == '750 mV':
			val = 0.75
		elif value == '75 mV':
			val = 0.075
		elif value == '1.5 V':
			val = 1.5
		elif value == '150 mV':
			val = 0.150
		self.daq.setDouble(f'/dev2901/sigouts/{channel-1}/range', val)


	def Out_Offset_put_function(self, value, channel):
		if isinstance(value, (float, int)):
			maximum = self.daq.getDouble(f'/dev2901/sigouts/{channel-1}/range', value)
			if abs(value) > maximum:
				self.daq.setDouble(f'/dev2901/sigouts/{channel-1}/offset', maximum*np.sign(value))
			else:
				self.daq.setDouble(f'/dev2901/sigouts/{channel-1}/offset', value)
		else:
			self.daq.setDouble(f'/dev2901/sigouts/{channel-1}/offset', value)


	"""def Out_1_Amp_Type_put_function(self, value):
		if value == 'Vrms':
			factor = 1 / np.sqrt(2)
			rooting = False
		elif value == 'Vpk':
			factor = 1
			rooting = False
		elif value == 'VdBm' and self.daq.getInt('/dev2901/sigouts/0/imp50') == 1:
			factor = 50
			rooting = True
		return factor, rooting
	"""

	def Out_Amp_Value_put_function(self, value, channel):
		if isinstance(value, (float, int)):
			maximum = self.daq.getDouble(f'/dev2901/sigouts/{channel-1}/range', value)
			if abs(value) > maximum:
				self.daq.setDouble(f'/dev2901/sigouts/{channel-1}/amplitudes/{channel-1 + channel*3 }', maximum * np.sign(value))
			else:
				self.daq.setDouble(f'/dev2901/sigouts/{channel-1}/amplitudes/{channel-1 + channel*3 }', value)
		else:
			self.daq.setDouble(f'/dev2901/sigouts/{channel-1}/amplitudes/{channel-1 + channel*3 }', value)
		

	def Out_Amp_put_function(self, value, channel):
		if value:
			val = 1
		else:
			val = 0
		self.daq.setInt(f'/dev2901/sigouts/{channel-1}/enables/{channel-1 + channel*3 }', val)

	def In_Range_put_function(self, value, channel):
		if isinstance(value, (float, int)):
			if value <= 1.5 and value >= 0.01:
				self.daq.setDouble(f'/dev2901/sigins/{channel-1}/range', value)
			elif value < 0.01:
				self.daq.setDouble(f'/dev2901/sigins/{channel-1}/range', 0.01)
			elif value > 1.5:
				self.daq.setDouble(f'/dev2901/sigins/{channel-1}/range', 1.5)
		else:
			self.daq.setDouble(f'/dev2901/sigins/{channel-1}/range', value)


	def In_Scaling_Value_put_function(self, value, channel):
		if isinstance(value, (float, int)):
			if value < 1e-12:
				self.daq.setDouble(f'/dev2901/sigins/{channel-1}/scaling', 1e-12)
			elif value >1e9:
				self.daq.setDouble(f'/dev2901/sigins/{channel-1}/scaling', 1e9)
			else:
				self.daq.setDouble(f'/dev2901/sigins/{channel-1}/scaling', value)
		else:
			self.daq.setDouble(f'/dev2901/sigins/{channel-1}/scaling', value)


	def In_AC_put_function(self, value, channel):
		if value:
			val = 1
		else:
			val = 0
		self.daq.setInt(f'/dev2901/sigins/{channel-1}/ac', val)

	def In_50_Ohm_put_function(self, value, channel):
		if value:
			val = 1
		else:
			val = 0
		self.daq.setInt(f'/dev2901/sigins/{channel-1}/imp50', val)

	def In_Diff_put_function(self, value, channel):
		if value == "Off":
			self.daq.setInt(f'/dev2901/sigins/{channel-1}/diff', 0)
		elif value == "Inverted":
			self.daq.setInt(f'/dev2901/sigins/{channel-1}/diff', 1)
		elif value == "In1 - In2" and channel == 1:
			self.daq.setInt('/dev2901/sigins/0/diff', 2)
		elif value == "In1 - In2" and channel == 2:
			self.daq.setInt('/dev2901/sigins/1/diff', 3)
		elif value == "In2 - In1" and channel == 1:
			self.daq.setInt('/dev2901/sigins/0/diff', 3)
		elif value == "In2 - In1" and channel == 2:
			self.daq.setInt('/dev2901/sigins/1/diff', 2)

	def Osc_Frequency_put_function(self, value, channel):
		if isinstance(value, (float, int)):
			if abs(value) > 900e6:
				self.daq.setDouble(f'/dev2901/oscs/{channel-1}/freq', 900e6*np.sign(value))
			else: 
				self.daq.setDouble(f'/dev2901/oscs/{channel-1}/freq', value)
		else: # schmeißt dann Fehler wegen setDouble
				self.daq.setDouble(f'/dev2901/oscs/{float(channel)-1}/freq', value)


	def Demod_Mode_put_function(self, value, channel):
		if value == 'Manual':
			self.daq.setInt(f'/dev2901/extrefs/{channel-1}/enable', 0)
		elif value == 'ExtRef':
			self.daq.setInt(f'/dev2901/extrefs/{channel-1}/enable', 1)
			self.daq.setInt(f'/dev2901/extrefs/{channel-1}/automode', 4)
		elif value == 'ExtRef Low BW':
			self.daq.setInt(f'/dev2901/extrefs/{channel-1}/enable', 1)
			self.daq.setInt(f'/dev2901/extrefs/{channel-1}/automode', 2)
		elif value == 'ExtRef High BW':
			self.daq.setInt(f'/dev2901/extrefs/{channel-1}/enable', 1)
			self.daq.setInt(f'/dev2901/extrefs/{channel-1}/automode', 3)

	def Demod_Harmonics_put_function(self, value, channel):
		if isinstance(value, (int)):
			if value < 0 or value > 1023:
				self.daq.setInt(f'/dev2901/demods/{channel-1}/harmonic', 1023)
			else:
				self.daq.setInt(f'/dev2901/demods/{channel-1}/harmonic', value)
		else:
			self.daq.setInt(f'/dev2901/demods/{channel-1}/harmonic', value)

	def Demod_Phase_put_function(self, value, channel):
		if isinstance(value, (int, float)):
			remainder_val = abs(value)%360
			sign = np.sign(value)
			if remainder_val <= 180:
				self.daq.setDouble(f'/dev2901/demods/{channel-1}/phaseshift', remainder_val*sign)
			elif remainder_val > 180:
				if sign == 1:
					self.daq.setDouble(f'/dev2901/demods/{channel-1}/phaseshift', remainder_val-360)
				elif sign == 0:
					self.daq.setDouble(f'/dev2901/demods/{channel-1}/phaseshift', -remainder_val+360)
				


	def Demod_Input_put_function(self, value, channel):
		if value == 'Sig In 1':
			val = 0
		elif value == 'Sig In 2':
			val = 1
		elif value == 'Trigger 1':
			val = 2
		elif value == 'Trigger 2':
			val = 3
		elif value == 'Aux Out 1':
			val = 4
		elif value == 'Aux Out 2':
			val = 5
		elif value == 'Aux Out 3':
			val = 6
		elif value == 'Aux Out 4':
			val = 7
		elif value == 'Aux In 1':
			val = 8
		elif value == 'Aux In 2':
			val = 9
		self.daq.setInt(f'/dev2901/demods/{channel-1}/adcselect', val)

	def Demod_LP_Order_put_function(self, value, channel):
		self.daq.setInt(f'/dev2901/demods/{channel-1}/order', value)

	'''def Demod_1_LP_BW_TC_put_function(self, value):
		pass'''

	'''def Demod_1_LP_BW_Value_put_function(self, value):
		pass'''

	def Demod_LP_TC_Value_put_function(self, value, channel):
		if isinstance(value, (int, float)):
			if value < 102.6e-9:
				self.daq.setDouble(f'/dev2901/demods/{channel-1}/timeconstant', 102.6e-9)
			elif value > 76.35:
				self.daq.setDouble(f'/dev2901/demods/{channel-1}/timeconstant', 76.35)
			else:
				self.daq.setDouble(f'/dev2901/demods/{channel-1}/timeconstant', value)
		else:
				self.daq.setDouble(f'/dev2901/demods/{channel-1}/timeconstant', value)


	def Demod_Sinc_put_function(self, value, channel):
		if value:
			val = 1
		else:
			val = 0
		self.daq.setInt(f'/dev2901/demods/{channel-1}/sinc', 1)


	def Demod_Data_Trans_put_function(self, value, channel):
		if value:
			val = 1
		else:
			val = 0
		self.daq.setInt(f'/dev2901/demods/{channel-1}/enable', 1)

	def Demod_Read_Data_trigger_function(self, channel):
		if not self._was_triggered[channel - 1]:
			self._last_measurement[channel - 1] = self.daq.getSample(f'/dev2901/demods/{channel-1}/sample')
			self._was_triggered[channel - 1] = True


	def Demod_Read_Data_X_read_function(self, channel):
		measurement = self._last_measurement[channel - 1]
		self._was_triggered[channel - 1] = False
		return measurement['x']
		
	def Demod_Read_Data_Y_read_function(self, channel):
		measurement = self._last_measurement[channel - 1]
		self._was_triggered[channel - 1] = False
		return measurement['y']
	
	def Demod_Read_Data_frequency_read_function(self, channel):
		measurement = self._last_measurement[channel - 1]
		self._was_triggered[channel - 1] = False
		return measurement['frequency']
		
	def Demod_Read_Data_phase_read_function(self, channel):
		measurement = self._last_measurement[channel - 1]
		self._was_triggered[channel - 1] = False
		return measurement['phase']

		
	def Demod_Read_Data_timeStamp_read_function(self, channel):
		measurement = self._last_measurement[channel - 1]
		self._was_triggered[channel - 1] = False
		return measurement['timestamp']
	
	def Demod_Read_Data_dioBits_read_function(self, channel):
		measurement = self._last_measurement[channel - 1]
		self._was_triggered[channel - 1] = False
		return measurement['dioBits']

	def Demod_Read_Data_trigger_read_function(self, channel):
		measurement = self._last_measurement[channel - 1]
		self._was_triggered[channel - 1] = False
		return measurement['trigger']

	def Demod_Read_Data_AuxIn0_read_function(self, channel):
		measurement = self._last_measurement[channel - 1]
		self._was_triggered[channel - 1] = False
		return measurement['auxIn0']

	def Demod_Read_Data_AuxIn1_read_function(self, channel):
		measurement = self._last_measurement[channel - 1]
		self._was_triggered[channel - 1] = False
		return measurement['auxIn1']

	
	def Demod_Data_Trans_Value_put_function(self, value, channel):
		if isinstance(value, (int, float)):
			if value < 1.676:
				self.daq.setDouble(f'/dev2901/demods/{channel-1}/rate', 1.676)
			elif value > 14.06e6:
				self.daq.setDouble(f'/dev2901/demods/{channel-1}/rate', 14.06e6)
			else:
				self.daq.setDouble(f'/dev2901/demods/{channel-1}/rate', value)
		else:
				self.daq.setDouble(f'/dev2901/demods/{channel-1}/rate', value)

	def Demod_Data_Trans_Trigger_put_function(self, value, channel):
		val = trigger_dict[value]
		self.daq.setInt(f'/dev2901/demods/{channel-1}/trigger', val)

