from pymeasure.instruments.agilent import Agilent33220A

from ophyd import Component as Cpt
from ophyd import Device
from nomad_camels.bluesky_handling.custom_function_signal import Custom_Function_SignalRO, Custom_Function_Signal

class Agilent_33220A(Device):
    frequency = Cpt(Custom_Function_Signal, value=1000, name='frequency')
    amplitude = Cpt(Custom_Function_Signal, value=1, name='amplitude')
    offset = Cpt(Custom_Function_Signal, value=0, name='offset')
    output = Cpt(Custom_Function_Signal, value=False, name='output')

    amplitude_unit = Cpt(Custom_Function_Signal, value='VPP', name='amplitude_unit', kind='config')
    waveform = Cpt(Custom_Function_Signal, value='sinusoid', name='waveform', kind='config')
    output_impedance = Cpt(Custom_Function_Signal, value='50', name='output_impedance', kind='config')

    def __init__(self, prefix='', *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None, resource_name=''):
        super().__init__(prefix=prefix, name=name, kind=kind,
                         read_attrs=read_attrs,
                         configuration_attrs=configuration_attrs, parent=parent)
        if name != 'test':
            self.visa_instrument = Agilent33220A(resource_name)
            self.frequency.put_function = self.set_frequency
            self.amplitude.put_function = self.set_amplitude
            self.offset.put_function = self.set_offset
            self.output.put_function = self.set_output
            self.waveform.put_function = self.set_waveform
    

    def set_frequency(self, value):
        self.visa_instrument.frequency = value
    
    def set_amplitude(self, value):
        self.visa_instrument.amplitude = value

    def set_offset(self, value):
        self.visa_instrument.offset = value

    def set_output(self, value):
        self.visa_instrument.output = value

    def set_waveform(self, value):
        self.visa_instrument.shape = value.upper()
    
    def set_amplitude_unit(self, value):
        self.visa_instrument.amplitude_unit = value.upper()
    
    def set_output_impedance(self, value):
        if value == 'highZ':
            value = 'INF'
        self.visa_instrument.write(f'OUTP:LOAD {value}')

    def configure_arbitrary_waveform(self, data, name='ARB1'):
        # scale data according to instrument
        import numpy as np
        n1 = len(bytes(len(data) * 2))
        n2 = len(data) * 2
        data = np.array(data)
        maxval = max(data)
        minval = min(data)
        if maxval != minval:
            scale = (maxval - minval) / 2
            offset = minval + scale
            data = (data - offset) / scale
        # typecast to int16
        data *= 2047
        data = data.astype(int)
        # convert numbers to binary data
        data = data.tobytes()
        # write data to instrument
        self.visa_instrument.write(f'FORM:BORD NORM;:DATA:DAC VOLATILE, #{n1}{n2}{data};:DATA:COPY {name}, VOLATILE;')

    def set_arbitrary_waveform(self, name='ARB1', gain=1.0, offset=0.0, frequency=1000.0):
        self.visa_instrument.write(f'FUNC:USER {name};:FUNC:SHAP USER;:VOLT {gain:g};:VOLT:OFFS {offset:g};:FREQ {frequency:g};')
        
