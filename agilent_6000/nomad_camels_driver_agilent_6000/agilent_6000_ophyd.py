import pyvisa
import re
from ophyd import Component as Cpt
import numpy as np
from PIL import Image
import io

from nomad_camels.bluesky_handling.visa_signal import VISA_Device, VISA_Signal_RO
from nomad_camels.bluesky_handling.custom_function_signal import (
    Custom_Function_SignalRO,
    Custom_Function_Signal,
)

meas_sources = {
    "channel 1": "CHAN1",
    "channel 2": "CHAN2",
    "channel 3": "CHAN3",
    "channel 4": "CHAN4",
    "math": "MATH",
    "digital 0": "DIG0",
    "digital 1": "DIG1",
    "digital 2": "DIG2",
    "digital 3": "DIG3",
    "digital 4": "DIG4",
    "digital 5": "DIG5",
    "digital 6": "DIG6",
    "digital 7": "DIG7",
    "digital 8": "DIG8",
    "digital 9": "DIG9",
    "digital 10": "DIG10",
    "digital 11": "DIG11",
    "digital 12": "DIG12",
    "digital 13": "DIG13",
    "digital 14": "DIG14",
    "digital 15": "DIG15",
}

waveform_functions = {
    "amplitude": "VAMP",
    "voltage average": "VAV",
    "voltage base": "VBAS",
    "counter": "COUN",
    "delay": "DEL",
    "duty cycle": "DUTY",
    "fall time": "FALL",
    "frequency": "FREQ",
    "voltage max": "VMAX",
    "voltage min": "VMIN",
    "overshoot": "OVER",
    "voltage peak to peak": "VPP",
    "period": "PER",
    "phase": "PHAS",
    "pre-shoot": "PRES",
    "rise time": "RIS",
    "voltage rms": "VRMS",
    "top": "VTOP",
    "width positive": "PWID",
    "width negative": "NWID",
    "x at maximum y": "XMAX",
    "x at minimum y": "XMIN",
}


def filter_resources(search_str: str):
    rm = pyvisa.ResourceManager()
    resources = rm.list_resources()
    search_regex = search_str.replace("?", ".").replace("*", ".*")
    pattern = re.compile(search_regex)
    return [r for r in resources if pattern.match(r)]


class Agilent_6000(VISA_Device):
    """Agilent 6000 series oscilloscope"""

    idn = Cpt(VISA_Signal_RO, name="idn", query="*IDN?", kind="config")
    invert_colors = Cpt(
        Custom_Function_Signal,
        value=False,
        name="invert_colors",
        kind="config",
        metadata={"description": "invert colors of screenshots"},
    )
    grayscale = Cpt(
        Custom_Function_Signal,
        value=False,
        name="grayscale",
        kind="config",
        metadata={"description": "grayscale for screenshots"},
    )
    image_type = Cpt(
        Custom_Function_Signal,
        value="png",
        name="image_type",
        kind="config",
        metadata={"description": "image type for screenshots"},
    )
    acquisition_type = Cpt(
        Custom_Function_Signal, value="normal", name="acquisition_type", kind="config"
    )
    n_averages = Cpt(
        Custom_Function_Signal,
        value=8,
        name="n_averages",
        kind="config",
        metadata={"description": 'number of averages if acquisition_type is "average"'},
    )

    timebase_get = Cpt(
        Custom_Function_SignalRO,
        value=20e-9,
        name="timebase_get",
        metadata={"units": "s", "description": "timebase for oscilloscope"},
    )
    timebase_set = Cpt(
        Custom_Function_Signal,
        value=20e-9,
        name="timebase_set",
        metadata={"units": "s", "description": "timebase for oscilloscope"},
    )
    timebase_offset = Cpt(
        Custom_Function_Signal,
        value=0,
        name="timebase_offset",
        kind="config",
        metadata={"units": "s", "description": "timebase offset for oscilloscope"},
    )
    min_record_length = Cpt(
        Custom_Function_Signal, name="min_record_length", kind="config"
    )
    trigger_mode = Cpt(
        Custom_Function_Signal,
        name="trigger_mode",
        kind="config",
        metadata={"description": "trigger mode (normal or auto)"},
    )  # auto or normal

    get_channel_range_1 = Cpt(
        Custom_Function_SignalRO,
        value=1,
        name="get_channel_range_1",
        metadata={"units": "V", "description": "vertical range of channel 1"},
    )
    get_channel_range_2 = Cpt(
        Custom_Function_SignalRO,
        value=1,
        name="get_channel_range_2",
        metadata={"units": "V", "description": "vertical range of channel 2"},
    )
    get_channel_range_3 = Cpt(
        Custom_Function_SignalRO,
        value=1,
        name="get_channel_range_3",
        metadata={"units": "V", "description": "vertical range of channel 3"},
    )
    get_channel_range_4 = Cpt(
        Custom_Function_SignalRO,
        value=1,
        name="get_channel_range_4",
        metadata={"units": "V", "description": "vertical range of channel 4"},
    )
    set_channel_range_1 = Cpt(
        Custom_Function_Signal,
        value=1,
        name="set_channel_range_1",
        metadata={"units": "V", "description": "vertical range of channel 1"},
    )
    set_channel_range_2 = Cpt(
        Custom_Function_Signal,
        value=1,
        name="set_channel_range_2",
        metadata={"units": "V", "description": "vertical range of channel 2"},
    )
    set_channel_range_3 = Cpt(
        Custom_Function_Signal,
        value=1,
        name="set_channel_range_3",
        metadata={"units": "V", "description": "vertical range of channel 3"},
    )
    set_channel_range_4 = Cpt(
        Custom_Function_Signal,
        value=1,
        name="set_channel_range_4",
        metadata={"units": "V", "description": "vertical range of channel 4"},
    )
    get_vertical_offset_1 = Cpt(
        Custom_Function_SignalRO,
        value=0,
        name="get_vertical_offset_1",
        metadata={"units": "V", "description": "vertical offset of channel 1"},
    )
    get_vertical_offset_2 = Cpt(
        Custom_Function_SignalRO,
        value=0,
        name="get_vertical_offset_2",
        metadata={"units": "V", "description": "vertical offset of channel 2"},
    )
    get_vertical_offset_3 = Cpt(
        Custom_Function_SignalRO,
        value=0,
        name="get_vertical_offset_3",
        metadata={"units": "V", "description": "vertical offset of channel 3"},
    )
    get_vertical_offset_4 = Cpt(
        Custom_Function_SignalRO,
        value=0,
        name="get_vertical_offset_4",
        metadata={"units": "V", "description": "vertical offset of channel 4"},
    )
    set_vertical_offset_1 = Cpt(
        Custom_Function_Signal,
        value=0,
        name="set_vertical_offset_1",
        metadata={"units": "V", "description": "vertical offset of channel 1"},
    )
    set_vertical_offset_2 = Cpt(
        Custom_Function_Signal,
        value=0,
        name="set_vertical_offset_2",
        metadata={"units": "V", "description": "vertical offset of channel 2"},
    )
    set_vertical_offset_3 = Cpt(
        Custom_Function_Signal,
        value=0,
        name="set_vertical_offset_3",
        metadata={"units": "V", "description": "vertical offset of channel 3"},
    )
    set_vertical_offset_4 = Cpt(
        Custom_Function_Signal,
        value=0,
        name="set_vertical_offset_4",
        metadata={"units": "V", "description": "vertical offset of channel 4"},
    )

    ac_coupling_1 = Cpt(
        Custom_Function_Signal,
        value=False,
        name="ac_coupling_1",
        kind="config",
        metadata={"description": "set AC coupling for channel 1"},
    )
    ac_coupling_2 = Cpt(
        Custom_Function_Signal,
        value=False,
        name="ac_coupling_2",
        kind="config",
        metadata={"description": "set AC coupling for channel 2"},
    )
    ac_coupling_3 = Cpt(
        Custom_Function_Signal,
        value=False,
        name="ac_coupling_3",
        kind="config",
        metadata={"description": "set AC coupling for channel 3"},
    )
    ac_coupling_4 = Cpt(
        Custom_Function_Signal,
        value=False,
        name="ac_coupling_4",
        kind="config",
        metadata={"description": "set AC coupling for channel 4"},
    )
    probe_attenuation_1 = Cpt(
        Custom_Function_Signal, value=10, name="probe_attenuation_1", kind="config"
    )
    probe_attenuation_2 = Cpt(
        Custom_Function_Signal, value=10, name="probe_attenuation_2", kind="config"
    )
    probe_attenuation_3 = Cpt(
        Custom_Function_Signal, value=10, name="probe_attenuation_3", kind="config"
    )
    probe_attenuation_4 = Cpt(
        Custom_Function_Signal, value=10, name="probe_attenuation_4", kind="config"
    )

    waveform_meas_source = Cpt(
        Custom_Function_Signal,
        name="waveform_meas_source",
        kind="config",
        metadata={"description": "source for waveform_meas"},
    )
    waveform_meas_source_2 = Cpt(
        Custom_Function_Signal,
        name="waveform_meas_source_2",
        kind="config",
        metadata={
            "description": "second source for waveform_meas, used in measurements like frequency ratio"
        },
    )
    waveform_meas_function = Cpt(
        Custom_Function_Signal,
        name="waveform_meas_function",
        kind="config",
        metadata={
            "description": "function for waveform_meas, e.g. frequency, voltage peak to peak, ..."
        },
    )

    waveform_meas = Cpt(
        Custom_Function_SignalRO,
        name="waveform_meas",
        metadata={
            "description": "measure the waveform with the given source and function"
        },
    )

    error = Cpt(
        VISA_Signal_RO,
        name="error",
        query=":SYST:ERR?",
        kind="normal",
        metadata={"description": "query the instrument for errors"},
    )

    image = Cpt(
        Custom_Function_SignalRO,
        name="image",
        metadata={"description": "take a screenshot of the oscilloscope"},
    )
    channel1 = Cpt(
        Custom_Function_SignalRO,
        name="channel1",
        metadata={"description": "get data from channel 1", "units": "V"},
    )
    channel2 = Cpt(
        Custom_Function_SignalRO,
        name="channel2",
        metadata={"description": "get data from channel 2", "units": "V"},
    )
    channel3 = Cpt(
        Custom_Function_SignalRO,
        name="channel3",
        metadata={"description": "get data from channel 3", "units": "V"},
    )
    channel4 = Cpt(
        Custom_Function_SignalRO,
        name="channel4",
        metadata={"description": "get data from channel 4", "units": "V"},
    )
    math_data = Cpt(
        Custom_Function_SignalRO,
        name="math_data",
        metadata={"description": "get data from math mode"},
    )
    digital1 = Cpt(
        Custom_Function_SignalRO,
        name="digital1",
        metadata={"description": "get data from digital 1 as bool array"},
    )
    digital2 = Cpt(
        Custom_Function_SignalRO,
        name="digital2",
        metadata={"description": "get data from digital 2 as bool array"},
    )

    time_1 = Cpt(
        Custom_Function_SignalRO,
        name="time_1",
        metadata={"units": "s", "description": "time axis for channel 1"},
    )
    time_2 = Cpt(
        Custom_Function_SignalRO,
        name="time_2",
        metadata={"units": "s", "description": "time axis for channel 2"},
    )
    time_3 = Cpt(
        Custom_Function_SignalRO,
        name="time_3",
        metadata={"units": "s", "description": "time axis for channel 3"},
    )
    time_4 = Cpt(
        Custom_Function_SignalRO,
        name="time_4",
        metadata={"units": "s", "description": "time axis for channel 4"},
    )
    time_math = Cpt(
        Custom_Function_SignalRO,
        name="time_math",
        metadata={"description": "x-axis for math mode"},
    )
    time_digital_1 = Cpt(
        Custom_Function_SignalRO,
        name="time_digital_1",
        metadata={"units": "s", "description": "time axis for digital 1"},
    )
    time_digital_2 = Cpt(
        Custom_Function_SignalRO,
        name="time_digital_2",
        metadata={"units": "s", "description": "time axis for digital 2"},
    )

    acquisition_success = Cpt(
        Custom_Function_SignalRO,
        name="acquisition_success",
        metadata={
            "description": "trigger an acquisition and check whether it was successful"
        },
    )

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
            baud_rate=baud_rate,
            write_termination=write_termination,
            read_termination=read_termination,
            **kwargs,
        )
        self.image.read_function = self.make_screenshot
        self.image.error_retry_function = self.error_clear_function
        self.channel1.read_function = lambda: self.fetch_analog("CHAN1")
        self.channel1.error_retry_function = self.error_clear_function
        self.channel2.read_function = lambda: self.fetch_analog("CHAN2")
        self.channel2.error_retry_function = self.error_clear_function
        self.channel3.read_function = lambda: self.fetch_analog("CHAN3")
        self.channel3.error_retry_function = self.error_clear_function
        self.channel4.read_function = lambda: self.fetch_analog("CHAN4")
        self.channel4.error_retry_function = self.error_clear_function
        self.math_data.read_function = lambda: self.fetch_analog("MATH")
        self.math_data.error_retry_function = self.error_clear_function
        self.digital1.read_function = lambda: self.fetch_digital("POD1")
        self.digital1.error_retry_function = self.error_clear_function
        self.digital2.read_function = lambda: self.fetch_digital("POD2")
        self.digital2.error_retry_function = self.error_clear_function
        self.time_1.read_function = lambda: self.get_analog_times(0)
        self.time_1.error_retry_function = self.error_clear_function
        self.time_2.read_function = lambda: self.get_analog_times(1)
        self.time_2.error_retry_function = self.error_clear_function
        self.time_3.read_function = lambda: self.get_analog_times(2)
        self.time_3.error_retry_function = self.error_clear_function
        self.time_4.read_function = lambda: self.get_analog_times(3)
        self.time_4.error_retry_function = self.error_clear_function
        self.time_math.read_function = self.get_math_times
        self.time_math.error_retry_function = self.error_clear_function
        self.time_digital_1.read_function = lambda: self.get_digital_times(0)
        self.time_digital_1.error_retry_function = self.error_clear_function
        self.time_digital_2.read_function = lambda: self.get_digital_times(1)
        self.time_digital_2.error_retry_function = self.error_clear_function

        self.times_math = None
        self.times_analog = [None, None, None, None]
        self.times_digital = [None, None]

        self.timebase_set.put_function = self.set_timebase
        self.timebase_set.error_retry_function = self.error_clear_function
        self.timebase_get.read_function = self.get_timebase
        self.timebase_get.error_retry_function = self.error_clear_function
        self.timebase_offset.put_function = self.set_timebase_offset
        self.timebase_offset.error_retry_function = self.error_clear_function

        self.set_channel_range_1.put_function = lambda value: self.set_vertical_range(
            1, value
        )
        self.set_channel_range_1.error_retry_function = self.error_clear_function
        self.set_channel_range_2.put_function = lambda value: self.set_vertical_range(
            2, value
        )
        self.set_channel_range_2.error_retry_function = self.error_clear_function
        self.set_channel_range_3.put_function = lambda value: self.set_vertical_range(
            3, value
        )
        self.set_channel_range_3.error_retry_function = self.error_clear_function
        self.set_channel_range_4.put_function = lambda value: self.set_vertical_range(
            4, value
        )
        self.set_channel_range_4.error_retry_function = self.error_clear_function
        self.get_channel_range_1.read_function = lambda: self.read_channel_range(1)
        self.get_channel_range_1.error_retry_function = self.error_clear_function
        self.get_channel_range_2.read_function = lambda: self.read_channel_range(2)
        self.get_channel_range_2.error_retry_function = self.error_clear_function
        self.get_channel_range_3.read_function = lambda: self.read_channel_range(3)
        self.get_channel_range_3.error_retry_function = self.error_clear_function
        self.get_channel_range_4.read_function = lambda: self.read_channel_range(4)
        self.get_channel_range_4.error_retry_function = self.error_clear_function
        self.ac_coupling_1.put_function = lambda value: self.set_coupling(1, value)
        self.ac_coupling_1.error_retry_function = self.error_clear_function
        self.ac_coupling_2.put_function = lambda value: self.set_coupling(2, value)
        self.ac_coupling_2.error_retry_function = self.error_clear_function
        self.ac_coupling_3.put_function = lambda value: self.set_coupling(3, value)
        self.ac_coupling_3.error_retry_function = self.error_clear_function
        self.ac_coupling_4.put_function = lambda value: self.set_coupling(4, value)
        self.ac_coupling_4.error_retry_function = self.error_clear_function
        self.set_vertical_offset_1.put_function = (
            lambda value: self.set_vertical_offset(1, value)
        )
        self.set_vertical_offset_1.error_retry_function = self.error_clear_function
        self.set_vertical_offset_2.put_function = (
            lambda value: self.set_vertical_offset(2, value)
        )
        self.set_vertical_offset_2.error_retry_function = self.error_clear_function
        self.set_vertical_offset_3.put_function = (
            lambda value: self.set_vertical_offset(3, value)
        )
        self.set_vertical_offset_3.error_retry_function = self.error_clear_function
        self.set_vertical_offset_4.put_function = (
            lambda value: self.set_vertical_offset(4, value)
        )
        self.set_vertical_offset_4.error_retry_function = self.error_clear_function
        self.get_vertical_offset_1.read_function = lambda: self.read_channel_offset(1)
        self.get_vertical_offset_1.error_retry_function = self.error_clear_function
        self.get_vertical_offset_2.read_function = lambda: self.read_channel_offset(2)
        self.get_vertical_offset_2.error_retry_function = self.error_clear_function
        self.get_vertical_offset_3.read_function = lambda: self.read_channel_offset(3)
        self.get_vertical_offset_3.error_retry_function = self.error_clear_function
        self.get_vertical_offset_4.read_function = lambda: self.read_channel_offset(4)
        self.get_vertical_offset_4.error_retry_function = self.error_clear_function

        self.acquisition_success.read_function = self.check_acquisition_success
        self.trigger_mode.put_function = self.set_trigger_mode
        self.trigger_mode.error_retry_function = self.error_clear_function

        self.acquisition_type.put_function = self.put_acquisition_type
        self.acquisition_type.error_retry_function = self.error_clear_function
        self.n_averages.put_function = self.update_average_number
        self.n_averages.error_retry_function = self.error_clear_function

        self.waveform_meas.read_function = self.measure_waveform

    def error_clear_function(self, e: Exception):
        if isinstance(e, pyvisa.errors.VisaIOError):
            self.visa_instrument.clear()

    def update_average_number(self, value):
        self.put_acquisition_type(self.acquisition_type.get(), value)

    def put_acquisition_type(self, value, n_avg=None):
        write_string = ":ACQ:TYPE "
        if value == "normal":
            write_string += "NORM; MODE RTIM;"
        elif value == "average":
            # add number of averages as int
            n_avg = n_avg or self.n_averages.get()
            write_string += f"AVER;COUN {int(n_avg)};MODE ETIM;"
        elif value == "peak_detect":
            write_string += "PEAK; MODE RTIM;"
        elif value == "high_resolution":
            write_string += "HRES; MODE RTIM;"
        self.visa_instrument.write(write_string)

    def check_acquisition_success(self):
        self.visa_instrument.write(":DIG;")
        self.visa_instrument.write(":ACQ:COMP?")
        try:
            state = self.visa_instrument.read_raw()
            if state != b"100\n":
                return False
            return True
        except Exception as e:
            print(e)
            return False

    def set_trigger_mode(self, value):
        self.visa_instrument.write(f":TRIG:SWE {value};")

    def measure_waveform(self, source=None, source2=None, function=None):
        source = source or self.waveform_meas_source.get()
        source2 = source2 or self.waveform_meas_source_2.get()
        function = function or self.waveform_meas_function.get()
        if source in meas_sources:
            source = meas_sources[source]
        if source2 in meas_sources:
            source2 = meas_sources[source2]
        if function in waveform_functions:
            function = waveform_functions[function]
        if source2 is None or source2.upper() == "NONE":
            write_string = f":MEAS:SOUR {source};{function}?;"
        else:
            write_string = f":MEAS:SOUR {source},{source2};{function}?;"
        data = self.visa_instrument.query(write_string)
        return float(data)

    def get_digital_times(self, n):
        times = self.times_digital[n]
        if times is None:
            self.fetch_digital(f"POD{n+1}")
            times = self.times_digital[n]
        self.times_digital[n] = None
        return times

    def get_analog_times(self, n):
        times = self.times_analog[n]
        if times is None:
            self.fetch_analog(f"CHAN{n+1}")
            times = self.times_analog[n]
        self.times_analog[n] = None
        return times

    def get_math_times(self):
        if self.times_math is None:
            self.fetch_analog("MATH")
        times = self.times_math
        self.times_math = None
        return times

    def default_setup(self):
        """Default setup for Agilent 6000 series oscilloscope"""
        self.visa_instrument.write(
            "*SRE 48;*CLS;:WAV:BYT MSBF;:WAV:FORM WORD;:TRIG:SWE NORM;:WAV:UNS 1;"
        )

    def make_screenshot(self):
        self.visa_instrument.write(f":HARD:INKS {int(self.invert_colors.get())};")
        write_string = ":DISP:DATA? "
        image_type = self.image_type.get()
        if image_type == "bmp":
            write_string += "BMP, "
        elif image_type == "png":
            write_string += "PNG, "
        if self.grayscale.get():
            write_string += f"SCR, GRAY;"
        else:
            write_string += f"SCR, COL;"
        self.visa_instrument.write(write_string)
        data = self.visa_instrument.read_raw(size=50000000)
        while True:
            try:
                data += self.visa_instrument.read_raw(size=50000000)
            except:
                break
        if image_type == "png":
            header_end = data.find(b"\x89PNG")
            if header_end != -1:
                data = data[header_end:]
        elif image_type == "bmp":
            header_end = data.find(b"BM")
            if header_end != -1:
                data = data[header_end:]
        img_data = io.BytesIO(data)
        img = Image.open(img_data)
        return np.array(img)

    def fetch_analog(self, source):
        write_string = f":WAV:SOUR {source}; PRE?;"
        data = self.visa_instrument.query(write_string)
        values = re.match(
            r"([+-]\d+),([+-]\d+),([+-]\d+),([+-]\d+),([+-]\d+\.\d+E[+-]\d+),([+-]\d+\.\d+E[+-]\d+),([+-]\d+),([+-]\d+\.\d+E[+-]\d+),([+-]\d+\.\d+E[+-]\d+),([+-]\d+)",
            data.strip(),
        )
        self.visa_instrument.write(":WAV:DATA?")
        y_data = self.visa_instrument.read_raw()
        n_vals = int(values.group(3))
        x_increment = float(values.group(5))
        x_origin = float(values.group(6))
        y_increment = float(values.group(8))
        y_origin = float(values.group(9))
        y_reference = int(values.group(10))
        n_bytes = int(y_data[2:10].decode())
        y_data = y_data[11:]
        ints = []
        multiplier = int(n_bytes / n_vals)
        for i in range(n_vals):
            ints.append(
                int.from_bytes(
                    y_data[multiplier * i : multiplier * i + multiplier],
                    byteorder="little",
                )
            )
        y_data = np.array(ints, dtype=float)
        y_data -= y_reference
        y_data *= y_increment
        y_data += y_origin
        x_data = np.array([x_origin + x_increment * i for i in range(len(y_data))])
        for i in range(0, 4):
            if f"{i + 1}" in source:
                self.times_analog[i] = x_data
                break
        if source == "MATH":
            self.times_math = x_data
        return y_data

    def fetch_digital(self, pod_source):
        write_string = f":WAV:SOUR {pod_source}; PRE?;"
        data = self.visa_instrument.query(write_string)
        values = re.match(
            r"([+-]\d+),([+-]\d+),([+-]\d+),([+-]\d+),([+-]\d+\.\d+E[+-]\d+),([+-]\d+\.\d+E[+-]\d+),([+-]\d+),([+-]\d+\.\d+E[+-]\d+),([+-]\d+\.\d+E[+-]\d+),([+-]\d+)",
            data.strip(),
        )
        self.visa_instrument.write(":WAV:DATA?")
        y_data = self.visa_instrument.read_raw()
        n_vals = int(values.group(3))
        x_increment = float(values.group(5))
        x_origin = float(values.group(6))
        ints = []
        n_bytes = int(y_data[2:10].decode())
        multiplier = int(n_bytes / n_vals)
        for i in range(n_vals):
            ints.append(
                int.from_bytes(
                    y_data[multiplier * i : multiplier * i + multiplier],
                    byteorder="little",
                )
            )
        y_data = [int_to_bools(n) for n in ints]
        y_data = np.array(pad_bool_arrays(y_data))
        x_data = np.array([x_origin + x_increment * i for i in range(len(y_data))])
        for i in range(0, 2):
            if f"{i + 1}" in pod_source:
                self.times_digital[i] = x_data
                break
        return y_data

    def set_coupling(self, channel, value):
        if value:
            self.visa_instrument.write(f":CHAN{channel}:COUP AC;")
        else:
            self.visa_instrument.write(f":CHAN{channel}:COUP DC;")

    def set_vertical_range(self, channel, value):
        self.visa_instrument.write(f":CHAN{channel}:RANG {value:g} V;")

    def set_vertical_offset(self, channel, value):
        self.visa_instrument.write(f":CHAN{channel}:OFFS {value:g} V;")

    def set_probe_attenuation(self, channel, value):
        self.visa_instrument.write(f":CHAN{channel}:PROBE {value:g};")

    def set_timebase(self, value):
        self.update_timebase(timebase=value)

    def get_timebase(self):
        return float(self.visa_instrument.query(":TIM:RANG?"))

    def set_timebase_offset(self, value):
        self.update_timebase(timebase_offset=value)

    def set_min_record_length(self, value):
        self.update_timebase(min_record_length=value)

    def update_timebase(
        self, timebase=None, timebase_offset=None, min_record_length=None
    ):
        timebase = timebase or self.timebase_get.get()
        timebase_offset = timebase_offset or self.timebase_offset.get()
        min_record_length = min_record_length or self.min_record_length.get()
        if min_record_length == "max":
            min_record_length = "MAX"
        else:
            min_record_length = int(min_record_length)
        write_string = f":TIM:RANG {timebase:g};:POS {timebase_offset:g};:WAV:POIN {min_record_length};"
        self.visa_instrument.write(write_string)

    def disable_front_panel(self):
        self.visa_instrument.write(":SYSTem:LOCK 1;")

    def enable_front_panel(self):
        self.visa_instrument.write(":SYSTem:LOCK 0;")

    def initiate_acquisition(self):
        self.visa_instrument.write(":DIG;")

    def run_continuous(self):
        self.visa_instrument.write(":RUN;")

    def stop_acquisition(self):
        self.visa_instrument.write(":STOP;")

    def read_channel_range(self, channel):
        val = self.visa_instrument.query(f"CHAN{channel}:RANGE?")
        return float(val)

    def read_channel_offset(self, channel):
        val = self.visa_instrument.query(f"CHAN{channel}:OFFS?")
        return float(val)

    def start_continuous_acquisition(self):
        self.visa_instrument.write(":RUN;")

    def stop_continuous_acquisition(self):
        self.visa_instrument.write(":STOP;")


def int_to_bools(n, lsb_first=True):
    binary = bin(n)[2:]
    if lsb_first:
        binary = binary[::-1]
    return [bool(int(bit)) for bit in binary]


def pad_bool_arrays(bool_arrays):
    max_length = max(
        len(arr) for arr in bool_arrays
    )  # Find the length of the longest array
    return [
        arr + [False] * (max_length - len(arr)) for arr in bool_arrays
    ]  # Pad shorter arrays


if __name__ == "__main__":
    rs = filter_resources("USB?::0x0957::0x172?*INSTR")[0]
    print(rs)
    osci = Agilent_6000(name="osci", resource_name=rs)
    print(osci.channel_range_1.get())
    # img = osci.image.get()
    # import matplotlib.pyplot as plt
    # plt.imshow(img)
    # plt.show()
    # osci.channel1.get()
    # osci.channel2.get()
    # osci.channel3.get()
    # osci.channel4.get()
    # osci.math_data.get()
    # print(osci.digital1.get())
    # osci.digital2.get()
    # osci.image.get()
