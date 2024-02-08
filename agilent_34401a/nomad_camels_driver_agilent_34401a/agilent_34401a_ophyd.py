from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.visa_signal import VISA_Signal, VISA_Signal_RO, \
    VISA_Device
from nomad_camels.bluesky_handling.custom_function_signal import Custom_Function_SignalRO, Custom_Function_Signal



class Agilent_34401(VISA_Device):
    measure_voltage_DC = Cpt(Custom_Function_SignalRO,
                             name='measure_voltage_DC',
                             metadata={'units': 'V', 'description': 'Measures DC voltage.'})
    measure_current_DC = Cpt(Custom_Function_SignalRO,
                             name='measure_current_DC',
                             metadata={'units': 'A', 'description': 'Measures DC current.'})
    measure_voltage_AC = Cpt(Custom_Function_SignalRO,
                             name='measure_voltage_AC',
                             metadata={'units': 'V', 'description':'Measures AC voltage.'})
    measure_current_AC = Cpt(Custom_Function_SignalRO,
                             name='measure_current_AC',
                             metadata={'units': 'A', 'description':'Measures AC current.'})
    measure_resistance = Cpt(Custom_Function_SignalRO,
                             name='measure_resistance',
                             metadata={'units': 'Ohm', 'description':'Measures DC resistance.'})
    measure_resistance_4wire = Cpt(Custom_Function_SignalRO,
                                   name='measure_resistance_4wire',
                                   metadata={'units': 'Ohm', 'description':'Measures four wire DC resistance.'})
    error = Cpt(Custom_Function_SignalRO,
                name='error',
                metadata={'description':'Error message.'})

    device_ID = Cpt(VISA_Signal_RO,
                    name='device_ID', kind='config', query='*IDN?',
                    metadata={'description':'Device ID.'})
    nPLC = Cpt(Custom_Function_Signal,
               name='nPLC', kind='config',
               metadata={'description':''})
                        

    def __init__(self, prefix='', *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None, resource_name='',
                 read_termination='\r\n', write_termination='\r\n',
                 baud_rate=9600, **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs,
                         configuration_attrs=configuration_attrs, parent=parent,
                         resource_name=resource_name, baud_rate=baud_rate,
                         write_termination=write_termination,
                         read_termination=read_termination, **kwargs)
        self.measure_current_DC.read_function = lambda: self.do_measurement('CURR:DC')
        self.measure_voltage_DC.read_function = lambda: self.do_measurement('VOLT:DC')
        self.measure_resistance.read_function = lambda: self.do_measurement('RES')
        self.measure_resistance_4wire.read_function = lambda: self.do_measurement('FRES')
        self.measure_current_AC.read_function = lambda: self.do_measurement('CURR:AC')
        self.measure_voltage_AC.read_function = lambda: self.do_measurement('VOLT:AC')
        self.error.read_function = self.read_errors
        
        self.last_meas_type = None
        self.nPLC.put_function = self.set_nPLC
    
    def set_nPLC(self, value):
        if self.last_meas_type in ['VOLT:DC', 'CURR:DC', 'RES', 'FRES']:
            self.last_meas_type = None
    
    def do_measurement(self, measurement_type):
        if self.last_meas_type != measurement_type:
            self.visa_instrument.write(f':CONF:{measurement_type}')
            if measurement_type in ['VOLT:DC', 'CURR:DC', 'RES', 'FRES']:
                self.visa_instrument.write(f':{measurement_type}:NPLC {self.nPLC.get()}')
            self.visa_instrument.write(f':{measurement_type}:NPLC {self.nPLC.get()}')
            self.visa_instrument.write(':TRIG:SOUR IMM;:TRIG:DEL:AUTO ON;')
            self.visa_instrument.write(':TRIG:COUN 1;:SAMP:COUN 1;:SAMP:TIM 0.1;:SAMP:SOUR IMM;')
            self.last_meas_type = measurement_type
        dat = self.visa_instrument.query('READ?')
        return float(dat.rstrip())

    def read_errors(self):
        invalid = self.check_valid()
        errs = self.visa_instrument.query(':SYST:ERR?').rstrip()
        if invalid:
            return f'{invalid}\n{errs}'
        return errs

    def check_valid(self):
        resp = int(self.visa_instrument.query(':STAT:QUES?'))
        # convert to binary and check which bits are set
        resp = int_to_bools(resp, n_bits=16)
        # check if any bits are set
        errors = ''
        if resp[0]:
            errors += 'voltage overload\n'
        if resp[1]:
            errors += 'current overload\n'
        if resp[2]:
            errors += 'sample timing violation\n'
        if resp[4]:
            errors += 'temperature overload\n'
        if resp[5]:
            errors += 'frequency overload/underflow\n'
        if resp[8]:
            errors += 'calibration corrupt\n'
        if resp[9]:
            errors += 'resistance overload\n'
        if resp[10]:
            errors += 'capacitance overload/underflow\n'
        if resp[11]:
            errors += 'lower limit failed\n'
        if resp[12]:
            errors += 'upper limit failed\n'
        if resp[14]:
            errors += 'memory overflow\n'
        return errors

def int_to_bools(n, lsb_first=True, n_bits=16):
    binary = bin(n)[2:]
    if lsb_first:
        binary = binary[::-1]
    arr = [bool(int(bit)) for bit in binary]
    while len(arr) < n_bits:
        arr.append(False)
    return arr


        


if __name__ == '__main__':
    from datetime import datetime as dt
    dmm = Agilent_34401(name='dmm', resource_name='USB0::0x0957::0x0607::MY47007006::INSTR')
    dmm.nPLC.put(1)
    now = dt.now()
    for i in range(10):
        print(dmm.measure_current_DC.get())
        print(dt.now() - now)
        now = dt.now()
    dmm.nPLC.put(10)
    now = dt.now()
    for i in range(10):
        print(dmm.measure_current_DC.get())
        print(dt.now() - now)
        now = dt.now()
    



