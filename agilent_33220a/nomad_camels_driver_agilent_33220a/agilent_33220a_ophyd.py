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

    arb_wave_frequencies = Cpt(
        Custom_Function_Signal,
        name="arb_wave_frequencies",
        kind="config",
        metadata={
            "description": "Comma seperated list of frequencies for each wave-part in the arbitrary waveform."
        },
    )
    arb_wave_amplitudes = Cpt(
        Custom_Function_Signal,
        name="arb_wave_amplitudes",
        kind="config",
        metadata={
            "description": "Comma seperated list of amplitudes for each wave-part in the arbitrary waveform."
        },
    )
    arb_wave_phases = Cpt(
        Custom_Function_Signal,
        name="arb_wave_phases",
        kind="config",
        metadata={
            "description": "Comma seperated list of phases for each wave-part in the arbitrary waveform."
        },
    )
    arb_wave_shapes = Cpt(
        Custom_Function_Signal,
        name="arb_wave_shapes",
        kind="config",
        metadata={
            "description": 'Comma seperated list of shapes for each wave-part in the arbitrary waveform. Possible are "sine" and "triangle".'
        },
    )
    arb_wave_sampling_rate = Cpt(
        Custom_Function_Signal, name="arb_wave_sampling_rate", kind="config"
    )
    arb_wave_num_samples = Cpt(
        Custom_Function_Signal, name="arb_wave_num_samples", kind="config"
    )
    arb_wave_signal_noise_level = Cpt(
        Custom_Function_Signal, name="arb_wave_signal_noise_level", kind="config"
    )
    user_arb_waveforms = Cpt(
        Custom_Function_SignalRO, name="user_arb_waveforms", kind="config"
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
            self.amplitude_unit.put_function = self.set_amplitude_unit
            self.output_impedance.put_function = self.set_output_impedance
            self.error.read_function = self.error_query
            self.user_arb_waveforms.read_function = self.get_user_arb_waveforms
        self.force_sequential = True
        self.currently_reading = False

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
        elif value in user_vals.values():
            self.visa_instrument.write(f"FUNC:USER {value};:FUNC:SHAP USER;")
        elif value == "triangle":
            self.visa_instrument.write("FUNC:SHAP TRI;")
        elif value.upper() in self.user_arb_waveforms.get():
            self.set_arbitrary_waveform(name=value.upper())
        elif value.upper() == "ARB" or value.upper() == "ARBITRARY":
            self.make_arbitrary_waveform()
        else:
            self.make_arbitrary_waveform(name=value.upper())

    def make_arbitrary_waveform(self, name="ARB1"):
        frequs = self.arb_wave_frequencies.get()
        if isinstance(frequs, str):
            frequs = [float(f) for f in self.arb_wave_frequencies.get().split(",")]
        amps = self.arb_wave_amplitudes.get()
        if isinstance(amps, str):
            amps = [float(a) for a in self.arb_wave_amplitudes.get().split(",")]
        phases = self.arb_wave_phases.get()
        if isinstance(phases, str):
            phases = [float(p) for p in self.arb_wave_phases.get().split(",")]
        shapes = self.arb_wave_shapes.get()
        if isinstance(shapes, str):
            shapes = self.arb_wave_shapes.get().split(",")
        sampling_rate = int(self.arb_wave_sampling_rate.get())
        num_samples = int(self.arb_wave_num_samples.get())
        signal_noise_level = float(self.arb_wave_signal_noise_level.get())
        wv = generate_waveform(
            [
                {"frequency": frequs[i], "amplitude": amps[i], "phase": phases[i]}
                for i in range(len(frequs))
            ],
            shapes=shapes,
            noise_level=signal_noise_level,
            sampling_rate=sampling_rate,
            num_samples=num_samples,
        )
        self.configure_arbitrary_waveform(wv, name=name)
        self.set_arbitrary_waveform(offset=self.offset.get(), name=name)

    def get_user_arb_waveforms(self):
        waves = self.visa_instrument.adapter.connection.query(":DATA:CAT?")
        waves = waves.replace('"', "").split(",")
        waves = [w.upper() for w in waves]
        return waves

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

    def set_arbitrary_waveform(self, name="ARB1"):
        self.visa_instrument.write(f"FUNC:USER {name};:FUNC:SHAP USER;")


def generate_waveform(
    tone_params,
    shapes=None,
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

    if not shapes:
        shapes = ["sine"] * len(tone_params)
    elif len(shapes) < len(tone_params):
        shapes += ["sine"] * (len(tone_params) - len(shapes))

    # Generate the waveform by summing sine tones
    if tone_params:
        parts = []
        for i, params in enumerate(tone_params):
            if shapes[i] == "sine":
                parts.append(
                    params["amplitude"]
                    * np.sin(
                        2 * np.pi * params["frequency"] * t
                        + np.deg2rad(params["phase"])
                    )
                )
            elif shapes[i] == "triangle":
                parts.append(
                    params["amplitude"]
                    * (2 * np.abs(2 * ((t * params["frequency"]) % 1) - 1) - 1)
                )
        waveform = np.sum(parts, axis=0)
        waveform += noise
    else:
        waveform = noise

    # Add DC offset
    waveform += offset

    return waveform


if __name__ == "__main__":
    # from datetime import datetime as dt
    import pyvisa

    rm = pyvisa.ResourceManager()
    res = rm.list_resources()
    fg = Agilent_33220A(name="fg", resource_name=res[0])
    # fg.output.put(False)
    # wv = generate_waveform(
    #     [
    #         {"frequency": 0.05, "amplitude": 1.9, "phase": 0},
    #         {"frequency": 51.2, "amplitude": 0.07, "phase": 0},
    #     ],
    #     sampling_rate=200,
    #     num_samples=4000,
    #     shapes=["triangle", "sine"],
    # )
    # fg.configure_arbitrary_waveform(wv)
    # fg.set_arbitrary_waveform(frequency=0.05, gain=1.9)
    # fg.output.put(True)
    fg.visa_instrument.write(":DATA:CAT?")
    print(fg.visa_instrument.read())
