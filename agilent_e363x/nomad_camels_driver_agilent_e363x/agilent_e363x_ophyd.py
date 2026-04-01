from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.visa_signal import (
    VISA_Signal,
    VISA_Signal_RO,
    VISA_Device,
)


class Agilent_E363X(VISA_Device):
    current_P6V = Cpt(
        VISA_Signal,
        name="current_P6V",
        write=":INST:NSEL 1;:CURR {value:g}",
        metadata={"units": "A", "description": "Sets the current limit for the +6 V channel."},
        write_delay=0.5,
    )
    current_P25V = Cpt(
        VISA_Signal,
        name="current_P25V",
        write=":INST:NSEL 2;:CURR {value:g}",
        metadata={"units": "A", "description": "Sets the current limit for the +25 V channel."},
        write_delay=0.5,
    )
    current_N25V = Cpt(
        VISA_Signal,
        name="current_N25V",
        write=":INST:NSEL 3;:CURR {value:g}",
        metadata={"units": "A", "description": "Sets the current limit for the -25 V channel."},
        write_delay=0.5,
    )

    idn = Cpt(VISA_Signal_RO, name="idn", kind="config", query="*IDN?", write_delay=0.5)

    voltage_P6V = Cpt(
        VISA_Signal,
        name="voltage_P6V",
        write=":INST:NSEL 1;:VOLT {value:g}",
        metadata={"units": "V", "description": "Sets the voltage for the +6 V channel."},
        write_delay=0.5,
    )
    voltage_P25V = Cpt(
        VISA_Signal,
        name="voltage_P25V",
        write=":INST:NSEL 2;:VOLT {value:g}",
        metadata={"units": "V", "description": "Sets the voltage for the +25 V channel."},
        write_delay=0.5,
    )
    voltage_N25V = Cpt(
        VISA_Signal,
        name="voltage_N25V",
        write=":INST:NSEL 3;:VOLT {value:g}",
        metadata={"units": "V", "description": "Sets the voltage for the -25 V channel."},
        write_delay=0.5,
    )
    output = Cpt(
        VISA_Signal,
        name="output_1",
        metadata={"description": "Enables (1) or disables (0) the output for all three channels."},
        write_delay=0.5,
    )

    error = Cpt(VISA_Signal_RO, query="SYST:ERR?", name="error", write_delay=0.5)

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
        **kwargs,
    ):
        super().__init__(
            prefix,
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
            **kwargs,
        )
        self.output.write = lambda x: self.enable_disable_output(x)

    def enable_disable_output(self, value):
        return f":OUTP {int(value):d}"


if __name__ == "__main__":
    import pyvisa
    import time

    rm = pyvisa.ResourceManager()
    ls = rm.list_resources()
    print(ls)
    ps = Agilent_E363X(name="ps", resource_name="ASRL1::INSTR")
    print(ps.idn.get())
    ps.current_limit_1.put(0.1)
    ps.output_1.put(1.0)
    ps.voltage_1.put(1)
    time.sleep(1)
    ps.voltage_1.put(0.5)
    time.sleep(1)
    ps.output_1.put(0)
