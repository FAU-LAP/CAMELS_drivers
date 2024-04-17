from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.custom_function_signal import (
    Custom_Function_Signal,
    Custom_Function_SignalRO,
)
from nomad_camels.bluesky_handling.visa_signal import (
    VISA_Signal,
    VISA_Signal_RO,
    VISA_Device,
)


class Agilent_81101A_Puls_Generator(VISA_Device):
    read_puls_freq = Cpt(
        VISA_Signal_RO,
        name="read_puls_freq",
        query=":FREQ?",
        parse_return_type="float",
        metadata={"units": "Hz", "description": "returns puls frequency in Hz"},
    )
    read_puls_period = Cpt(
        VISA_Signal_RO,
        name="read_puls_period",
        query=":PULS:PER?",
        parse_return_type="float",
        metadata={"units": "s", "description": "returns puls period in s"},
    )
    read_puls_width = Cpt(
        VISA_Signal_RO,
        name="read_puls_width",
        query=":PULS:WIDT?",
        parse_return_type="float",
        metadata={"units": "s", "description": "returns puls width in s"},
    )
    read_puls_amplitude = Cpt(
        VISA_Signal_RO,
        name="read_puls_amplitude",
        query=":VOLT?",
        parse_return_type="float",
        metadata={
            "units": "V",
            "description": "returns voltage amplitude of the puls in V",
        },
    )
    read_puls_offset = Cpt(
        VISA_Signal_RO,
        name="read_puls_offset",
        query=":VOLT:OFFS?",
        parse_return_type="float",
        metadata={
            "units": "V",
            "description": "returns offset voltage of the puls in V",
        },
    )
    read_puls_duty_cycle = Cpt(
        VISA_Signal_RO,
        name="read_puls_duty_cycle",
        query=":PULS:DCYC?",
        parse_return_type="float",
        metadata={"units": "%", "description": "returns the puls duty cycle in %"},
    )
    output_enable = Cpt(
        Custom_Function_Signal,
        name="output_enable",
        metadata={"units": "", "description": "Enables the output signal"},
    )
    set_puls_period = Cpt(
        VISA_Signal,
        name="set_puls_period",
        parse_return_type=None,
        metadata={
            "units": "ns",
            "description": "Sets puls peirod to desired value in ns",
        },
    )
    set_puls_width = Cpt(
        VISA_Signal,
        name="set_puls_width",
        write=":PULS:WIDT {value} ns",
        parse_return_type=None,
        metadata={
            "units": "ns",
            "description": "Sets puls width to desired value in ns",
        },
    )
    reset = Cpt(
        VISA_Signal,
        name="reset",
        write="*RST",
        parse_return_type=None,
        metadata={
            "units": "",
            "description": "Resets the puls generator to factory settings",
        },
    )
    output_disable = Cpt(
        Custom_Function_Signal,
        name="output_disable",
        metadata={"units": "", "description": "Disables the output signal"},
    )
    set_puls_duty_cycle = Cpt(
        VISA_Signal,
        name="set_puls_duty_cycle",
        write=":PULS:DCYC {value} ",
        parse_return_type=None,
        metadata={"units": "%", "description": "Sets the puls duty cycle in %"},
    )
    set_puls_freq = Cpt(
        VISA_Signal,
        name="set_puls_freq",
        write=":FREQ {value} Hz",
        parse_return_type=None,
        metadata={"units": "Hz", "description": "Sets the puls frequency in Hz"},
    )
    set_puls_amplitude = Cpt(
        VISA_Signal,
        name="set_puls_amplitude",
        write=":VOLT {value} V",
        parse_return_type=None,
        kind="config",
        metadata={
            "units": "V",
            "description": "Sets the voltage amplitude of the puls in V",
        },
    )
    set_puls_offset = Cpt(
        VISA_Signal,
        name="set_puls_offset",
        write=":VOLT:OFFS {value} V",
        parse_return_type=None,
        kind="config",
        metadata={
            "units": "V",
            "description": "Sets the offset voltage of the puls in V",
        },
    )
    set_puls_transition = Cpt(
        VISA_Signal,
        name="set_puls_transition",
        write=":PULS:TRAN {value} ns",
        parse_return_type=None,
        kind="config",
        metadata={
            "units": "ns",
            "description": "Sets the transition time, i.e., the leading edge and falling edge of the puls in ns",
        },
    )
    identification = Cpt(
        VISA_Signal_RO,
        name="identification",
        query="*IDN?",
        parse_return_type="str",
        kind="config",
        metadata={"units": "", "description": "Returns puls generator ID"},
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
        write_termination="\r\n",
        read_termination="\r\n",
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
            read_termination=read_termination,
            write_termination=write_termination,
            **kwargs,
        )
        self.output_disable.put_function = (
            lambda x: self.output_disable_write_function()
        )
        self.output_enable.put_function = lambda x: self.output_enable_write_function()
        self.set_puls_period.write = lambda value: self.set_puls_period_write_function(
            value
        )
        self.set_puls_freq.write = lambda value: self.set_puls_freq_write_function(
            value
        )

        if name == "test":
            return
        self.output_is_enabled = int(self.visa_instrument.query(":OUTP?"))

    def output_disable_write_function(self):
        if self.output_is_enabled:
            self.visa_instrument.write(":OUTP 0")
            self.output_is_enabled = 0

    def output_enable_write_function(self):
        if not self.output_is_enabled:
            self.visa_instrument.write(":OUTP 1")
            self.output_is_enabled = 1

    def set_puls_period_write_function(self, value):
        self.pulse_width = float(self.visa_instrument.query(":PULS:WIDT?"))
        if value / 1e9 <= self.pulse_width:
            self.visa_instrument.write(f":PULS:WIDT {value/2} ns")
        return f":PULS:PER {value} ns"

    def set_puls_freq_write_function(self, value):
        self.pulse_width = float(self.visa_instrument.query(":PULS:WIDT?"))
        if 1 / value <= self.pulse_width:
            self.visa_instrument.write(f":PULS:WIDT {(1/value)/2} ns")
        return f":FREQ {value} Hz"
