import pyvisa
import re
from ophyd import Component as Cpt
import numpy as np
from PIL import Image
import io

from nomad_camels.bluesky_handling.visa_signal import VISA_Device,  VISA_Signal_RO
from nomad_camels.bluesky_handling.custom_function_signal import Custom_Function_SignalRO, Custom_Function_Signal


def filter_resources(search_str:str):
    rm = pyvisa.ResourceManager()
    resources = rm.list_resources()
    search_regex = search_str.replace("?", ".").replace("*", ".*")
    pattern = re.compile(search_regex)
    return [r for r in resources if pattern.match(r)]


class Agilent_6000(VISA_Device):
    """Agilent 6000 series oscilloscope"""
    idn = Cpt(VISA_Signal_RO, name='idn', query='*IDN?', kind='config')
    invert_colors = Cpt(Custom_Function_Signal, value=False, name='invert_colors', kind='config')
    grayscale = Cpt(Custom_Function_Signal, value=False, name='grayscale', kind='config')
    image_type = Cpt(Custom_Function_Signal, value='png', name='image_type', kind='config')

    error = Cpt(VISA_Signal_RO, name='error', query=':SYST:ERR?', kind='normal')

    image = Cpt(Custom_Function_SignalRO, name='image')
    channel1 = Cpt(Custom_Function_SignalRO, name='channel1')
    channel2 = Cpt(Custom_Function_SignalRO, name='channel2')
    channel3 = Cpt(Custom_Function_SignalRO, name='channel3')
    channel4 = Cpt(Custom_Function_SignalRO, name='channel4')
    math_data = Cpt(Custom_Function_SignalRO, name='math_data')
    digital1 = Cpt(Custom_Function_SignalRO, name='digital1')
    digital2 = Cpt(Custom_Function_SignalRO, name='digital2')

    time_1 = Cpt(Custom_Function_SignalRO, name='time_1')
    time_2 = Cpt(Custom_Function_SignalRO, name='time_2')
    time_3 = Cpt(Custom_Function_SignalRO, name='time_3')
    time_4 = Cpt(Custom_Function_SignalRO, name='time_4')
    time_math = Cpt(Custom_Function_SignalRO, name='time_math')
    time_digital_1 = Cpt(Custom_Function_SignalRO, name='time_digital_1')
    time_digital_2 = Cpt(Custom_Function_SignalRO, name='time_digital_2')

    def __init__(self, prefix='', *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None, resource_name='',
                 read_termination='\r\n', write_termination='\r\n',
                 baud_rate=9600, **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs,
                         configuration_attrs=configuration_attrs, parent=parent,
                         resource_name=resource_name, baud_rate=baud_rate,
                         write_termination=write_termination,
                         read_termination=read_termination, **kwargs)
        if name != 'test':
            self.default_setup()
            # self.visa_instrument.timeout = 10
        self.image.read_function = self.make_screenshot
        self.channel1.read_function = lambda: self.fetch_analog('CHAN1')
        self.channel2.read_function = lambda: self.fetch_analog('CHAN2')
        self.channel3.read_function = lambda: self.fetch_analog('CHAN3')
        self.channel4.read_function = lambda: self.fetch_analog('CHAN4')
        self.math_data.read_function = lambda: self.fetch_analog('MATH')
        self.digital1.read_function = lambda: self.fetch_digital('POD1')
        self.digital2.read_function = lambda: self.fetch_digital('POD2')
        self.time_1.read_function = lambda: self.get_analog_times(0)
        self.time_2.read_function = lambda: self.get_analog_times(1)
        self.time_3.read_function = lambda: self.get_analog_times(2)
        self.time_4.read_function = lambda: self.get_analog_times(3)
        self.time_math.read_function = self.get_math_times
        self.time_digital_1.read_function = lambda: self.get_digital_times(0)
        self.time_digital_2.read_function = lambda: self.get_digital_times(1)
        self.times_math = None
        self.times_analog = [None, None, None, None]
        self.times_digital = [None, None]

    def get_digital_times(self, n):
        times = self.times_digital[n]
        if times is None:
            self.fetch_digital(f'POD{n+1}')
            times = self.times_digital[n]
        self.times_digital[n] = None
        return times

    def get_analog_times(self, n):
        times = self.times_analog[n]
        if times is None:
            self.fetch_analog(f'CHAN{n+1}')
            times = self.times_analog[n]
        self.times_analog[n] = None
        return times
    
    def get_math_times(self):
        if self.times_math is None:
            self.fetch_analog('MATH')
        times = self.times_math
        self.times_math = None
        return times

    def default_setup(self):
        """Default setup for Agilent 6000 series oscilloscope"""
        self.visa_instrument.write('*SRE 48;*CLS;:WAV:BYT MSBF;:WAV:FORM WORD;:TRIG:SWE NORM;:WAV:UNS 1;')
    
    def make_screenshot(self):
        self.visa_instrument.write(f':HARD:INKS {int(self.invert_colors.get())};')
        write_string = ':DISP:DATA? '
        image_type = self.image_type.get()
        if image_type == 'bmp':
            write_string += 'BMP, '
        elif image_type == 'bmp8bit':
            write_string += 'BMP8bit, '
        elif image_type == 'png':
            write_string += 'PNG, '
        if image_type == 'tiff':
            write_string += 'TIFF, GRAT, MON;'
        else:
            if self.grayscale.get():
                write_string += f'SCR, GRAY;'
            else:
                write_string += f'SCR, COL;'
        self.visa_instrument.write(write_string)
        data = self.visa_instrument.read_raw(size=50000000)
        while True:
            try:
                data += self.visa_instrument.read_raw(size=50000000)
            except:
                break
        if image_type == 'png':
            header_end = data.find(b'\x89PNG')
            if header_end != -1:
                data = data[header_end:]
        elif image_type in ['bmp', 'bmp8bit']:
            header_end = data.find(b'BM')
            if header_end != -1:
                data = data[header_end:]
        elif image_type == 'tiff':
            header_end = data.find(b'II*\x00')
            if header_end == -1:
                header_end = data.find(b'MM\x00*')
            if header_end != -1:
                data = data[header_end:]
        img_data = io.BytesIO(data)
        img = Image.open(img_data)
        return np.array(img)


    def fetch_analog(self, source):
        write_string = f':WAV:SOUR {source}; PRE?;'
        data = self.visa_instrument.query(write_string)
        values = re.match(r"([+-]\d+),([+-]\d+),([+-]\d+),([+-]\d+),([+-]\d+\.\d+E[+-]\d+),([+-]\d+\.\d+E[+-]\d+),([+-]\d+),([+-]\d+\.\d+E[+-]\d+),([+-]\d+\.\d+E[+-]\d+),([+-]\d+)", data.strip())
        self.visa_instrument.write(':WAV:DATA?')
        y_data = self.visa_instrument.read_raw()
        try:
            y_data = y_data.decode('ascii')
        except:
            pass
        x_increment = float(values.group(5))
        x_origin = float(values.group(6))
        y_increment = float(values.group(8))
        y_origin = float(values.group(9))
        y_reference = int(values.group(10))
        try:
            y_data = np.array([ord(c) for c in y_data], dtype=float)
        except:
            y_data = np.array(list(y_data), dtype=float)
        y_data -= y_reference
        y_data *= y_increment
        y_data += y_origin
        x_data = np.array([x_origin + x_increment * i for i in range(len(y_data))])
        for i in range(0, 4):
            if f'{i + 1}' in source:
                self.times_analog[i] = x_data
                break
        if source == 'MATH':
            self.times_math = x_data
        return y_data

    def fetch_digital(self, pod_source):
        write_string = f':WAV:SOUR {pod_source}; PRE?;'
        data = self.visa_instrument.query(write_string)
        values = re.match(r"([+-]\d+),([+-]\d+),([+-]\d+),([+-]\d+),([+-]\d+\.\d+E[+-]\d+),([+-]\d+\.\d+E[+-]\d+),([+-]\d+),([+-]\d+\.\d+E[+-]\d+),([+-]\d+\.\d+E[+-]\d+),([+-]\d+)", data.strip())
        self.visa_instrument.write(':WAV:DATA?')
        y_data = self.visa_instrument.read_raw()
        x_increment = float(values.group(5))
        x_origin = float(values.group(6))
        y_data = list(y_data)
        y_data = [int_to_bools(n) for n in y_data]
        y_data = np.array(pad_bool_arrays(y_data))
        x_data = np.array([x_origin + x_increment * i for i in range(len(y_data))])
        for i in range(0, 2):
            if f'{i + 1}' in pod_source:
                self.times_digital[i] = x_data
                break
        return y_data

def int_to_bools(n, lsb_first=True):
    binary = bin(n)[2:]
    if lsb_first:
        binary = binary[::-1]
    return [bool(int(bit)) for bit in binary]

def pad_bool_arrays(bool_arrays):
    max_length = max(len(arr) for arr in bool_arrays)  # Find the length of the longest array
    return [arr + [False] * (max_length - len(arr)) for arr in bool_arrays]  # Pad shorter arrays


if __name__ == '__main__':
    rs = filter_resources('USB?::0x0957::0x172?*INSTR')[0]
    print(rs)
    osci = Agilent_6000(name='osci', resource_name=rs)
    # img = osci.image.get()
    # import matplotlib.pyplot as plt
    # plt.imshow(img)
    # plt.show()
    osci.channel1.get()
    osci.channel2.get()
    osci.channel3.get()
    osci.channel4.get()
    osci.math_data.get()
    osci.digital1.get()
    osci.digital2.get()
    osci.image.get()

