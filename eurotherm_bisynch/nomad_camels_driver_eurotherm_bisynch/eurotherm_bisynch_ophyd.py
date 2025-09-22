from nomad_camels.bluesky_handling import visa_signal
from nomad_camels.bluesky_handling.custom_function_signal import Custom_Function_Signal, Custom_Function_SignalRO
from math import floor
from pyvisa.constants import Parity, StopBits
import pyvisa
from ophyd import Component as Cpt


special_commands = ['SW', 'II', 'VO', 'CI', 'BL', 'EE', 'MN', 'OS', 'XS', 'CL', 'CU', 'V1', 'V0']
end_chars = [bytes(chr(3), encoding='utf-8'), bytes(chr(4), encoding='utf-8')]

class Eurotherm_Bisynch(visa_signal.VISA_Device):

    setpoint = Cpt(Custom_Function_Signal, value=0, name="setpoint")
    proportional_val = Cpt(Custom_Function_Signal, value=0, name="proportional_val", kind='config')
    integral_val = Cpt(Custom_Function_Signal, value=0, name="integral_val", kind='config')
    derivative_val = Cpt(Custom_Function_Signal, value=0, name="derivative_val", kind='config')
    max_output = Cpt(Custom_Function_Signal, value=0, name="max_output", kind='config')

    read_output = Cpt(Custom_Function_SignalRO, value=0, name="read_output")
    read_temp = Cpt(Custom_Function_SignalRO, value=0, name="read_temp")


    def __init__(
        self,
        prefix="",
        *,
        name,
        kind=None,
        read_attrs=None,
        configuration_attrs=None,
        parent=None,
        resource_name="",
        read_termination="\r\n",
        write_termination="\r\n",
        baud_rate=9600,
        timeout=2000,
        retry_on_error=0,
        retry_on_timeout=False,
        eurotherm_group_unit=0,
        **kwargs,
    ):
        super().__init__(
            prefix=prefix,
            name=name,
            kind=kind,
            read_attrs=read_attrs,
            configuration_attrs=configuration_attrs,
            parent=parent,
            resource_name=resource_name,
            read_termination=read_termination,
            write_termination=write_termination,
            baud_rate=baud_rate,
            timeout=timeout,
            retry_on_error=retry_on_error,
            retry_on_timeout=retry_on_timeout,
            **kwargs,
        )
        self.eurotherm_group = str(floor(eurotherm_group_unit / 10))
        self.eurotherm_unit = str(eurotherm_group_unit % 10)
        if not self.visa_instrument:
            return
        self.visa_instrument.data_bits = 7
        self.visa_instrument.stop_bits = StopBits.one
        self.visa_instrument.parity = Parity.even
        self.read_output.read_function = lambda: self.read_bisynch('OP')
        self.read_temp.read_function = lambda: self.read_bisynch('PV')
        self.setpoint.write_function = lambda value: self.write_bisynch('SL', value)
        self.proportional_val.write_function = lambda value: self.write_bisynch('XP', value)
        self.integral_val.write_function = lambda value: self.write_bisynch('TI', value)
        self.derivative_val.write_function = lambda value: self.write_bisynch('TD', value)
        self.max_output.write_function = lambda value: self.write_bisynch('HO', value)


    def read_bisynch(self, command:str):
        # check if command starts with a number
        base_command = command
        if not command[0].isdigit() or len(command) != 3:
            command = command[:2]
        command = f'{chr(4)}{self.eurotherm_group}{self.eurotherm_group}{self.eurotherm_unit}{self.eurotherm_unit}{command}{chr(5)}'
        self.visa_instrument.write(command)
        last = None
        return_val = b''
        while last not in end_chars:
            last = self.visa_instrument.read_bytes(1)
            return_val += last
        if not return_val or not len(return_val) >= 4:
            raise ValueError(f"Error reading from Eurotherm: {return_val}")
        return_val = str(return_val)
        if not base_command in return_val:
            raise ValueError(f"Error reading from Eurotherm: {return_val}")
        return_val = return_val.split(base_command)[1]
        return_val = ''.join([char for char in return_val if char.isdigit() or char in ['.', '-', '+']])
        if base_command in special_commands:
            return_val = return_val[1:]
            return int(return_val)
        return float(return_val)
    
    def write_bisynch(self, command:str, value):
        if not command[0].isdigit() or len(command) != 3:
            command = command[:2]
        # make five digit string of value
        if command not in special_commands:
            if value >= 10000:
                value = str(value)
            elif value >= 1000:
                value = f'{value:5.0f}'
            elif value >= 100 or value <= -10:
                value = f'{value:5.1f}'
            else:
                value = f'{value:5.2f}'
        # calculate longitudinal redundancy block check control (bcc) character
        command = f'{command}{value}{chr(3)}'
        bcc = 0
        for char in command:
            bcc = ~(bcc ^ ord(char))
        bcc = chr(bcc)
        command = f'{chr(4)}{self.eurotherm_group}{self.eurotherm_group}{self.eurotherm_unit}{self.eurotherm_unit}{chr(2)}{command}{bcc}'
        self.visa_instrument.write(command)
        ret = self.visa_instrument.read_bytes(1)
        if ret == b'\x15':
            raise ValueError(f"Error writing to Eurotherm: {ret}")


if __name__ == '__main__':
    rm = pyvisa.ResourceManager()
    print(rm.list_resources())
    print(rm.list_opened_resources())
    euro = Eurotherm_Bisynch(name='euro', resource_name='ASRL2::INSTR')
    print(rm.list_opened_resources())
    euro.write_bisynch('SL', 50)
    print(euro.read_bisynch('PV'))
