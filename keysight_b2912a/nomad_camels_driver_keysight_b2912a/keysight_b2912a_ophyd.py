from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.visa_signal import (
    VISA_Signal_RO,
    VISA_Signal,
    VISA_Device,
)


def source_func(inp, chan, volt_source):
    if inp == "Voltage":
        v = "VOLT"
        volt_source[chan - 1] = True
    else:
        v = "CURR"
        volt_source[chan - 1] = False
    return f":SOUR{chan}:{v} 0.0; :SOUR{chan}:FUNC DC; FUNC:MODE {v}"


def compliance_func(inp, chan, comp_type, volt_source):
    v = "VOLT" if volt_source[chan - 1] else "CURR"
    if comp_type == v:
        return ""
    return f":SENS{chan}:{comp_type}:PROT {inp}"


def source_range_func(inp, chan, volt_source):
    v = "VOLT" if volt_source[chan - 1] else "CURR"
    return f":SOUR{chan}:{v}:RANG {inp[:-2]}"


def source_auto_func(inp, chan, volt_source):
    v = "VOLT" if volt_source[chan - 1] else "CURR"
    m = "ON" if inp else "OFF"
    return f":SOUR{chan}:{v}:RANG:AUTO {m}"


def range_lower_lim_func(inp, chan, volt_source):
    v = "VOLT" if volt_source[chan - 1] else "CURR"
    return f":SOUR{chan}:{v}:RANG:AUTO:LLIM {inp[:-2]}"


def output_protection_func(inp, chan):
    v = "ON" if inp else "OFF"
    return f":OUTP{chan}:PROT {v}"


def range_func(inp, chan, typ):
    return f"SENS{chan}:{typ}:RANG {inp}"


def low_terminal_func(inp, chan):
    v = "GRO" if inp == "Ground" else "FLO"
    return f":OUTP{chan}:LOW {v};"


def four_wire_meas_func(inp, chan):
    v = "ON" if inp else "OFF"
    return f":SENS{chan}:REM {v}"


def auto_range_func(inp, chan, typ):
    v = "ON" if inp else "OFF"
    return f":SENS{chan}:{typ}:RANG:AUTO {v}"


def auto_range_lower_lim_func(inp, chan, typ):
    return f":SENS{chan}:{typ}:RANG:AUTO:LLIM {inp[:-2]}"


def auto_range_upper_lim_func(inp, chan, typ):
    return f":SENS{chan}:{typ}:RANG:AUTO:ULIM {inp[:-4]}"


def res_comp_func(inp, chan):
    v = "ON" if inp else "OFF"
    return f":SENS{chan}:RES:OCOM {v}"


def auto_range_mode_func(inp, chan, typ):
    if inp == "Normal":
        v = "NORM"
    elif inp == "Resolution":
        v = "RES"
    else:
        v = "SPE"
    return f":SENS{chan}:{typ}:RANG:AUTO:MODE {v}"


def NPLC_func(inp, chan):
    return f":SENS{chan}:VOLT:NPLC {inp}; :SENS{chan}:CURR:NPLC {inp}; :SENS{chan}:RES:NPLC {inp};"


def enable_func(inp, chan):
    v = "ON" if inp else "OFF"
    return f":OUTP{chan} {v}"


class Keysight_B2912(VISA_Device):
    mesV1 = Cpt(
        VISA_Signal_RO, name="mesV1", query="MEAS:VOLT? (@1)", metadata={"units": "V"}
    )
    mesI1 = Cpt(
        VISA_Signal_RO, name="mesI1", query="MEAS:CURR? (@1)", metadata={"units": "A"}
    )
    mesV2 = Cpt(
        VISA_Signal_RO, name="mesV2", query="MEAS:VOLT? (@2)", metadata={"units": "V"}
    )
    mesI2 = Cpt(
        VISA_Signal_RO, name="mesI2", query="MEAS:CURR? (@2)", metadata={"units": "A"}
    )
    setV1 = Cpt(
        VISA_Signal, name="setV1", write="SOUR1:VOLT {value}", metadata={"units": "V"}
    )
    setI1 = Cpt(
        VISA_Signal, name="setI1", write="SOUR1:CURR {value}", metadata={"units": "A"}
    )
    setV2 = Cpt(
        VISA_Signal, name="setV2", write="SOUR2:VOLT {value}", metadata={"units": "V"}
    )
    setI2 = Cpt(
        VISA_Signal, name="setI2", write="SOUR2:CURR {value}", metadata={"units": "A"}
    )

    enable1 = Cpt(VISA_Signal, name="enable1", write=lambda x: enable_func(x, 1))
    enable2 = Cpt(VISA_Signal, name="enable2", write=lambda x: enable_func(x, 2))

    idn = Cpt(VISA_Signal_RO, name="idn", query="*IDN?", kind="config")

    source1 = Cpt(VISA_Signal, name="source1", kind="config")
    source_range1 = Cpt(VISA_Signal, name="source_range1", kind="config")
    range_lower_lim1 = Cpt(VISA_Signal, name="range_lower_lim1", kind="config")
    source_auto1 = Cpt(VISA_Signal, name="source_auto1", kind="config")
    low_terminal1 = Cpt(
        VISA_Signal,
        name="low_terminal1",
        kind="config",
        write=lambda x: low_terminal_func(x, 1),
    )
    current_auto_mode1 = Cpt(
        VISA_Signal,
        name="current_auto_mode1",
        kind="config",
        write=lambda x: auto_range_mode_func(x, 1, "CURR"),
    )
    current_lower_lim1 = Cpt(
        VISA_Signal,
        name="current_lower_lim1",
        kind="config",
        write=lambda x: auto_range_lower_lim_func(x, 1, "CURR"),
    )
    current_range1 = Cpt(
        VISA_Signal,
        name="current_range1",
        kind="config",
        write=lambda x: range_func(x[:-2], 1, "CURR"),
    )
    voltage_range1 = Cpt(
        VISA_Signal,
        name="voltage_range1",
        kind="config",
        write=lambda x: range_func(x[:-2], 1, "VOLT"),
    )
    voltage_auto_mode1 = Cpt(
        VISA_Signal,
        name="voltage_auto_mode1",
        kind="config",
        write=lambda x: auto_range_mode_func(x, 1, "VOLT"),
    )
    voltage_lower_lim1 = Cpt(
        VISA_Signal,
        name="voltage_lower_lim1",
        kind="config",
        write=lambda x: auto_range_lower_lim_func(x, 1, "VOLT"),
    )
    resistance_range1 = Cpt(
        VISA_Signal,
        name="resistance_range1",
        kind="config",
        write=lambda x: range_func(x[:-4], 1, "RES"),
    )
    resistance_upper_lim1 = Cpt(
        VISA_Signal,
        name="resistance_upper_lim1",
        kind="config",
        write=lambda x: auto_range_upper_lim_func(x, 1, "RES"),
    )
    output_protection1 = Cpt(
        VISA_Signal,
        name="output_protection1",
        kind="config",
        write=lambda x: output_protection_func(x, 1),
    )
    four_wire_meas1 = Cpt(
        VISA_Signal,
        name="four_wire_meas1",
        kind="config",
        write=lambda x: four_wire_meas_func(x, 1),
    )
    current_auto_range1 = Cpt(
        VISA_Signal,
        name="current_auto_range1",
        kind="config",
        write=lambda x: auto_range_func(x, 1, "CURR"),
    )
    voltage_auto_range1 = Cpt(
        VISA_Signal,
        name="voltage_auto_range1",
        kind="config",
        write=lambda x: auto_range_func(x, 1, "VOLT"),
    )
    resistance_auto_range1 = Cpt(
        VISA_Signal,
        name="resistance_auto_range1",
        kind="config",
        write=lambda x: auto_range_func(x, 1, "RES"),
    )
    resistance_compensation1 = Cpt(
        VISA_Signal,
        name="resistance_compensation1",
        kind="config",
        write=lambda x: res_comp_func(x, 1),
    )
    voltage_compliance1 = Cpt(
        VISA_Signal,
        name="voltage_compliance1",
        kind="config",
        write=":SENS1:CURR:PROT {value}",
    )
    current_compliance1 = Cpt(
        VISA_Signal,
        name="current_compliance1",
        kind="config",
        write=":SENS1:VOLT:PROT {value}",
    )
    NPLC1 = Cpt(
        VISA_Signal, name="NPLC1", kind="config", write=lambda x: NPLC_func(x, 1)
    )

    source2 = Cpt(VISA_Signal, name="source2", kind="config")
    source_range2 = Cpt(VISA_Signal, name="source_range2", kind="config")
    range_lower_lim2 = Cpt(VISA_Signal, name="range_lower_lim2", kind="config")
    source_auto2 = Cpt(VISA_Signal, name="source_auto2", kind="config")
    low_terminal2 = Cpt(
        VISA_Signal,
        name="low_terminal2",
        kind="config",
        write=lambda x: low_terminal_func(x, 2),
    )
    current_auto_mode2 = Cpt(
        VISA_Signal,
        name="current_auto_mode2",
        kind="config",
        write=lambda x: auto_range_mode_func(x, 2, "CURR"),
    )
    current_lower_lim2 = Cpt(
        VISA_Signal,
        name="current_lower_lim2",
        kind="config",
        write=lambda x: auto_range_lower_lim_func(x, 2, "CURR"),
    )
    current_range2 = Cpt(
        VISA_Signal,
        name="current_range2",
        kind="config",
        write=lambda x: range_func(x[:-2], 2, "CURR"),
    )
    voltage_range2 = Cpt(
        VISA_Signal,
        name="voltage_range2",
        kind="config",
        write=lambda x: range_func(x[:-2], 2, "VOLT"),
    )
    voltage_auto_mode2 = Cpt(
        VISA_Signal,
        name="voltage_auto_mode2",
        kind="config",
        write=lambda x: auto_range_mode_func(x, 2, "VOLT"),
    )
    voltage_lower_lim2 = Cpt(
        VISA_Signal,
        name="voltage_lower_lim2",
        kind="config",
        write=lambda x: auto_range_lower_lim_func(x, 2, "VOLT"),
    )
    resistance_range2 = Cpt(
        VISA_Signal,
        name="resistance_range2",
        kind="config",
        write=lambda x: range_func(x[:-4], 2, "RES"),
    )
    resistance_upper_lim2 = Cpt(
        VISA_Signal,
        name="resistance_upper_lim2",
        kind="config",
        write=lambda x: auto_range_upper_lim_func(x, 2, "RES"),
    )
    output_protection2 = Cpt(
        VISA_Signal,
        name="output_protection2",
        kind="config",
        write=lambda x: output_protection_func(x, 2),
    )
    four_wire_meas2 = Cpt(
        VISA_Signal,
        name="four_wire_meas2",
        kind="config",
        write=lambda x: four_wire_meas_func(x, 2),
    )
    current_auto_range2 = Cpt(
        VISA_Signal,
        name="current_auto_range2",
        kind="config",
        write=lambda x: auto_range_func(x, 2, "CURR"),
    )
    voltage_auto_range2 = Cpt(
        VISA_Signal,
        name="voltage_auto_range2",
        kind="config",
        write=lambda x: auto_range_func(x, 2, "VOLT"),
    )
    resistance_auto_range2 = Cpt(
        VISA_Signal,
        name="resistance_auto_range2",
        kind="config",
        write=lambda x: auto_range_func(x, 2, "RES"),
    )
    resistance_compensation2 = Cpt(
        VISA_Signal,
        name="resistance_compensation2",
        kind="config",
        write=lambda x: res_comp_func(x, 2),
    )
    voltage_compliance2 = Cpt(
        VISA_Signal,
        name="voltage_compliance2",
        kind="config",
        write=":SENS2:CURR:PROT {value}",
    )
    current_compliance2 = Cpt(
        VISA_Signal,
        name="current_compliance2",
        kind="config",
        write=":SENS2:VOLT:PROT {value}",
    )
    NPLC2 = Cpt(
        VISA_Signal, name="NPLC2", kind="config", write=lambda x: NPLC_func(x, 2)
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

        self.v_source = [True, True]

        self.source1.write = lambda x: source_func(x, 1, self.v_source)
        self.source_range1.write = lambda x: source_range_func(x, 1, self.v_source)
        self.range_lower_lim1.write = lambda x: range_lower_lim_func(
            x, 1, self.v_source
        )
        self.source_auto1.write = lambda x: source_auto_func(x, 1, self.v_source)
        self.voltage_compliance1.write = lambda x: compliance_func(
            x, 1, "VOLT", self.v_source
        )
        self.voltage_compliance2.write = lambda x: compliance_func(
            x, 2, "VOLT", self.v_source
        )
        self.current_compliance1.write = lambda x: compliance_func(
            x, 1, "CURR", self.v_source
        )
        self.current_compliance2.write = lambda x: compliance_func(
            x, 2, "CURR", self.v_source
        )

        self.source2.write = lambda x: source_func(x, 2, self.v_source)
        self.source_range2.write = lambda x: source_range_func(x, 2, self.v_source)
        self.range_lower_lim2.write = lambda x: range_lower_lim_func(
            x, 2, self.v_source
        )
        self.source_auto2.write = lambda x: source_auto_func(x, 2, self.v_source)

    def turn_on_output(self):
        self.enable1.put(1)
        self.enable2.put(1)

    def turn_off_output(self):
        self.finalize_steps()

    def finalize_steps(self):
        self.enable1.put(0)
        self.enable2.put(0)
