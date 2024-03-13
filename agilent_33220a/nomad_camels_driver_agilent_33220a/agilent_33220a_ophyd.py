from pymeasure.instruments.agilent import Agilent33220A
import numpy as np

from ophyd import Component as Cpt
from ophyd import Device
from nomad_camels.bluesky_handling.custom_function_signal import (
    Custom_Function_SignalRO,
    Custom_Function_Signal,
)


class Agilent_33220A(Device):
    frequency = Cpt(Custom_Function_Signal, value=1000, name="frequency")
    amplitude = Cpt(Custom_Function_Signal, value=1, name="amplitude")
    offset = Cpt(Custom_Function_Signal, value=0, name="offset")
    output = Cpt(Custom_Function_Signal, value=False, name="output")
    error = Cpt(Custom_Function_SignalRO)

    amplitude_unit = Cpt(
        Custom_Function_Signal, value="VPP", name="amplitude_unit", kind="config"
    )
    waveform = Cpt(
        Custom_Function_Signal, value="sinusoid", name="waveform", kind="config"
    )
    output_impedance = Cpt(
        Custom_Function_Signal, value="50", name="output_impedance", kind="config"
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
    ):
        super().__init__(
            prefix=prefix,
            name=name,
            kind=kind,
            read_attrs=read_attrs,
            configuration_attrs=configuration_attrs,
            parent=parent,
        )
        if name != "test":
            self.visa_instrument = Agilent33220A(resource_name)
            self.frequency.put_function = self.set_frequency
            self.amplitude.put_function = self.set_amplitude
            self.offset.put_function = self.set_offset
            self.output.put_function = self.set_output
            self.waveform.put_function = self.set_waveform

    def error_query(self):
        self.visa_instrument.write(":SYST:ERR?")
        return self.visa_instrument.read()

    def set_frequency(self, value):
        self.visa_instrument.frequency = value

    def set_amplitude(self, value):
        self.visa_instrument.amplitude = value

    def set_offset(self, value):
        self.visa_instrument.offset = value

    def set_output(self, value):
        self.visa_instrument.output = value

    def set_waveform(self, value):
        values = [
            "SINUSOID",
            "SIN",
            "SQUARE",
            "SQU",
            "RAMP",
            "PULSE",
            "PULS",
            "NOISE",
            "NOIS",
            "DC",
        ]
        user_vals = {
            "sinc": "SINC",
            "negative ramp": "NEG_RAMP",
            "exponential rise": "EXP_RISE",
            "exponential fall": "EXP_FALL",
            "cardiac": "CARDIAC",
        }
        if value.upper() in values:
            self.visa_instrument.shape = value.upper()
        elif value in user_vals:
            self.visa_instrument.write(f"FUNC:USER {user_vals[value]};:FUNC:SHAP USER;")
        elif value == "triangle":
            self.visa_instrument.write("FUNC:SHAP TRI;")

    def set_amplitude_unit(self, value):
        self.visa_instrument.amplitude_unit = value.upper()

    def set_output_impedance(self, value):
        if value == "highZ":
            value = "INF"
        self.visa_instrument.write(f"OUTP:LOAD {value}")

    def configure_arbitrary_waveform(self, data, name="ARB1"):
        # scale data according to instrument
        data = np.array(data)
        maxval = max(data)
        minval = min(data)
        if maxval != minval:
            scale = (maxval - minval) / 2
            offset = minval + scale
            data = (data - offset) / scale
        s = f":FORM:BORD NORM;:DATA VOLATILE, "
        for d in data:
            s += f"{d}, "
        s = s[:-2]
        s += f";:DATA:COPY {name}, VOLATILE;"
        timeout = self.visa_instrument.adapter.connection.timeout
        self.visa_instrument.adapter.connection.timeout = 20e3
        self.visa_instrument.write(s)
        self.visa_instrument.adapter.connection.timeout = timeout

    def set_arbitrary_waveform(
        self, name="ARB1", gain=1.0, offset=0.0, frequency=1000.0
    ):
        self.visa_instrument.write(
            f"FUNC:USER {name};:FUNC:SHAP USER;:VOLT {gain:g};:VOLT:OFFS {offset:g};:FREQ {frequency:g};"
        )


def generate_waveform(
    tone_params,
    noise_level=0.0,
    offset=0.0,
    sampling_rate=1000,
    num_samples=1000,
    seed=-1,
):
    """
    Generate a waveform with multiple sine tones, additive Gaussian noise, and a DC offset.

    Parameters:
    tone_params (list of dict): Each dict contains 'frequency', 'amplitude', and 'phase' for a sine tone.
    noise_level (float): The rms level of the additive Gaussian noise. Default is 0.0.
    offset (float): The DC offset of the signal. Default is 0.0.
    sampling_rate (int): The sampling rate in samples per second. Default is 1000.
    num_samples (int): The number of samples in the waveform. Default is 1000.
    seed (int): The seed for the noise generator. Default is -1.

    Returns:
    numpy.ndarray: The generated waveform.
    """
    # Create a time array
    t = np.arange(num_samples) / sampling_rate

    # Add Gaussian noise
    if seed > 0:
        np.random.seed(seed)
    noise = np.random.normal(scale=noise_level, size=num_samples)

    # Generate the waveform by summing sine tones
    if tone_params:
        waveform = np.sum(
            [
                params["amplitude"]
                * np.sin(
                    2 * np.pi * params["frequency"] * t + np.deg2rad(params["phase"])
                )
                for params in tone_params
            ],
            axis=0,
        )
        waveform += noise
    else:
        waveform = noise

    # Add DC offset
    waveform += offset

    return waveform


if __name__ == "__main__":
    from datetime import datetime as dt
    import pyvisa

    rm = pyvisa.ResourceManager()
    res = rm.list_resources()
    print(res)
    fg = Agilent_33220A(name="fg", resource_name=res[0])
    wv = generate_waveform(
        [
            {"frequency": 100, "amplitude": 1, "phase": 0},
            {"frequency": 50, "amplitude": 1, "phase": 0},
        ],
        sampling_rate=200000,
        num_samples=20000,
    )
    fg.configure_arbitrary_waveform(wv)
    fg.set_arbitrary_waveform(frequency=10, gain=0.1)
    fg.output.put(1)
