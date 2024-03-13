from ophyd import Component as Cpt
import numpy as np
import re

from nomad_camels.bluesky_handling.visa_signal import (
    VISA_Signal,
    VISA_Signal_RO,
    VISA_Device,
)
from nomad_camels.bluesky_handling.custom_function_signal import Custom_Function_Signal


def get_current_range_value(current_range_string):
    current_ranges = {
        "Auto": 0,
        "1nA": 1,
        "10nA": 2,
        "100nA": 3,
        "1uA": 4,
        "10uA": 5,
        "100uA": 6,
        "1mA": 7,
        "10mA": 8,
        "100mA": 9,
    }
    return current_ranges[current_range_string]


def get_voltage_range_value(voltage_range_string):
    voltage_ranges = {
        "Auto": 0,
        "1.1V": 1,
        "11V": 2,
        "110V": 3,
        "1100V": 4,
    }
    return voltage_ranges[voltage_range_string]


def get_integration_time_value(integration_time):
    if integration_time:
        integration_times = {
            "0.4ms": 0,
            "4ms": 1,
            "20ms": 3,
        }
        return integration_times[integration_time]


def read_sweep_array(read_string):
    """Converts the long sweep string to numpy arrays.
    :param read_string: The string returned by the instrument. It is a comma separated string
    containing pairs of source and measure values.
    Like: '<source1>,<meas1>,<source2>,<meas2>,<source3>,<meas3>'
    :return: Returns a numpy array with the first column containing the sourced values and the
    second column containing the measured values
    """
    read_data = np.array(read_string.split(","), dtype=float)
    source_data = []
    for x in read_data[::2]:
        try:
            source_data.append(float(x))
        except:
            match_result = re.match(r"^(\+\d\d.\d)(\+.*)$", x)
            source_data.append(float(match_result[2]))
    source_data = np.array(source_data)
    measure_data = [float(x) for x in read_data[1::2]]
    all_data = np.vstack((source_data, measure_data)).transpose()
    return all_data


class Keithley_237(VISA_Device):
    """
    Driver for the Keithley 237:
    The K237 needs to be initialized before measurement! (set initialize loop-step to any value)
    Basic functions:
    F: Set source and function
    P: Select filter
    S: Set integration time
    W: Enable/ disable default delay
    L: Program compliance
    B: Program bias operation
    Q: Create/append sweep list
    A: Modify sweep list
    T: Select trigger configuration
    R: Enable/ disable triggers
    N: Select operate/ standby mode
    Y: Select terminator characters
    K: Select EOI and hold-off on X
    G: Select output data format
    V: 1100V range control
    J: Execute self-tests
    U: Request status
    H: Send IEEE immediate trigger, H0X needed to actually trigger device
    X: Execute DDCs
    """

    read_voltage = Cpt(
        VISA_Signal_RO,
        name="read_voltage",
        metadata={"units": "V", "description": "Reads a single voltage value."},
    )
    read_current = Cpt(
        VISA_Signal_RO,
        name="read_current",
        metadata={"units": "A", "description": "Reads a single current value."},
    )
    set_voltage = Cpt(
        VISA_Signal,
        name="set_voltage",
        metadata={"units": "V", "description": "Sets a single voltage value."},
    )
    set_current = Cpt(
        VISA_Signal,
        name="set_current",
        metadata={"units": "A", "description": "Sets a single current value."},
    )
    start_voltage_sweep = Cpt(
        VISA_Signal,
        name="start_voltage_sweep",
        metadata={
            "description": "Set to 1 to start the sweep after all required values "
            "are set with a Set Channels step.",
        },
    )
    start_current_sweep = Cpt(
        VISA_Signal,
        name="start_current_sweep",
        metadata={
            "description": "Set to 1 to start the sweep after all required values "
            "are set with a Set Channels step.",
        },
    )
    read_voltage_sweep = Cpt(
        VISA_Signal_RO,
        name="read_voltage_sweep",
        query="X",
        parse=read_sweep_array,
        metadata={
            "units": "first column: V, second column: A",
            "description": "Reads the string and converts it to a numpy array. "
            "First column is voltage, second cloumn is current.",
        },
    )
    read_current_sweep = Cpt(
        VISA_Signal_RO,
        name="read_current_sweep",
        query="X",
        parse=read_sweep_array,
        metadata={
            "units": "first column: A, second column: V",
            "description": "Reads the string and converts it to a numpy array. "
            "First column is current, second cloumn is voltage.",
        },
    )
    disable = Cpt(
        VISA_Signal,
        name="disable",
        write="N0X",
        metadata={"description": "Disables the instrument."},
    )
    # Settings for Sweeps
    setSweep_Type = Cpt(
        Custom_Function_Signal,
        name="setSweep_Type",
        metadata={
            "description": "0:Fix Level\n"
            "1:Lin. Stair\n"
            "2:Log. Stair\n"
            "3:Fix Level Pulsed\n"
            "4: Lin. Stair Pulsed\n"
            "5:Log. Stair Pulsed"
        },
    )
    setSweep_Level = Cpt(
        Custom_Function_Signal,
        name="setSweep_Level",
        metadata={
            "description": "Specifies the output level of a fixed level "
            "or fixed level pulse sweep (I or V)"
        },
    )
    setSweep_Start = Cpt(
        Custom_Function_Signal,
        name="Sweep_Start",
        metadata={"description": "Starting source values for stair waveforms."},
    )
    setSweep_Stop = Cpt(
        Custom_Function_Signal,
        name="setSweep_Stop",
        metadata={"description": "Stopping source values for stair waveforms."},
    )
    setSweep_Step = Cpt(
        Custom_Function_Signal,
        name="setSweep_Step",
        metadata={
            "description": "Incremental absolute value for stair sweeps. "
            "\nMaximum value is twice the full scale range of the "
            "highest range used in generating the sweep."
        },
    )
    setSweep_Pulses = Cpt(
        Custom_Function_Signal,
        name="setSweep_Pulses",
        metadata={
            "description": "Quantity of pulses in a pulse sweep waveform (0-500)"
        },
    )
    setSweep_Points = Cpt(
        Custom_Function_Signal,
        name="setSweep_Points",
        metadata={
            "description": "Specifies the number of measurements \nin a fixed level sweep (any number possible) or "
            "\npoints per decade in a log stair or log stair pulsed sweep with following options:"
            "\n0=5 Points per decade"
            "\n1=10"
            "\n2=25"
            "\n3=50"
        },
    )
    setSweep_T_on = Cpt(
        Custom_Function_Signal,
        name="setSweep_T_on",
        metadata={
            "units": "ms",
            "description": "Duration of sweep level in milliseconds (0-65000)",
        },
    )
    setSweep_T_off = Cpt(
        Custom_Function_Signal,
        name="setSweep_T_off",
        metadata={
            "units": "ms",
            "description": "Duration of bias level in milliseconds (0-65000)",
        },
    )
    # Configuration settings
    idn = Cpt(
        VISA_Signal_RO,
        name="idn",
        kind="config",
        query="U0X",
        metadata={"description": "Instrument ID"},
    )
    Source_Type = Cpt(Custom_Function_Signal, name="Source_Type", kind="config")
    Four_wire = Cpt(Custom_Function_Signal, name="Four_wire", kind="config")
    Averages = Cpt(
        Custom_Function_Signal,
        name="Averages",
        kind="config",
    )
    Bias_delay = Cpt(
        Custom_Function_Signal,
        name="Bias_delay",
        kind="config",
    )
    Integration_time = Cpt(
        Custom_Function_Signal,
        name="Integration_time",
        kind="config",
    )
    Current_compliance_range = Cpt(
        Custom_Function_Signal,
        name="Current_compliance_range",
        kind="config",
    )
    Current_compliance = Cpt(
        Custom_Function_Signal,
        name="Current_compliance",
        kind="config",
    )
    Voltage_compliance_range = Cpt(
        Custom_Function_Signal,
        name="Voltage_compliance_range",
        kind="config",
    )
    Voltage_compliance = Cpt(
        Custom_Function_Signal,
        name="Voltage_compliance",
        kind="config",
    )
    Sweep_Hysteresis = Cpt(
        Custom_Function_Signal,
        name="Sweep_Hysteresis",
        kind="config",
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
        baud_rate=9600,
        write_termination="\r\n",
        read_termination="\r\n",
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
        self.source_range_value = None
        self.compliance_value = None
        self.Integration_time_value = None
        self.compliance_range_value = None
        self.Sweep_Hysteresis_value = None
        self.averages_value = None
        self.Source_Type_latest = None
        # Setting all the variables with the values of the config settings
        self.Averages.put_function = self.Averages_put_function
        self.Integration_time.put_function = self.Integration_time_put_function
        self.Sweep_Hysteresis.put_function = self.Sweep_Hysteresis_put_function
        # set functions of the settable channels
        self.set_voltage.write = self.set_voltage_function
        self.set_current.write = self.set_current_function
        self.read_current.query = self.read_current_function
        self.read_voltage.query = self.read_voltage_function
        self.start_voltage_sweep.write = self.start_voltage_sweep_function
        self.start_current_sweep.write = self.start_current_sweep_function

    def compliance_put_function(self, value):
        if value == "Voltage":
            self.source_range_value = get_voltage_range_value(
                self.Voltage_compliance_range.get()
            )
            if self.source_range_value == 4:
                self.visa_instrument.write("V1X")
            else:
                self.visa_instrument.write("V0X")
            self.compliance_range_value = get_current_range_value(
                self.Current_compliance_range.get()
            )
            self.compliance_value = self.Current_compliance.get()
            self.visa_instrument.write("F0,0X")
            self.visa_instrument.write("G4,2,0X")
            self.visa_instrument.write(
                f"L{self.compliance_value},{self.compliance_range_value}X"
            )
        elif value == "Current":
            self.source_range_value = get_current_range_value(
                self.Current_compliance_range.get()
            )
            self.compliance_range_value = get_voltage_range_value(
                self.Voltage_compliance_range.get()
            )
            if self.compliance_range_value == 4:
                self.visa_instrument.write("V1X")
            else:
                self.visa_instrument.write("V0X")
            self.compliance_value = self.Voltage_compliance.get()
            self.visa_instrument.write("F1,0X")
            self.visa_instrument.write("G4,2,0X")
            self.visa_instrument.write(
                f"L{self.compliance_value},{self.compliance_range_value}X"
            )
        elif value == "Sweep Voltage":
            self.source_range_value = get_voltage_range_value(
                self.Voltage_compliance_range.get()
            )
            if self.source_range_value == 4:
                self.visa_instrument.write("V1X")
            else:
                self.visa_instrument.write("V0X")
            self.compliance_range_value = get_current_range_value(
                self.Current_compliance_range.get()
            )
            self.compliance_value = self.Current_compliance.get()
            self.visa_instrument.write("F0,1X")
            self.visa_instrument.write("G5,2,2X")
            # self.read_sweep.parse = read_sweep_array
            self.visa_instrument.write(
                f"L{self.compliance_value},{self.compliance_range_value}X"
            )
        elif value == "Sweep Current":
            self.source_range_value = get_current_range_value(
                self.Current_compliance_range.get()
            )
            self.compliance_range_value = get_voltage_range_value(
                self.Voltage_compliance_range.get()
            )
            if self.compliance_range_value == 4:
                self.visa_instrument.write("V1X")
            else:
                self.visa_instrument.write("V0X")
            self.compliance_value = self.Voltage_compliance.get()
            self.visa_instrument.write("F1,1X")
            self.visa_instrument.write("G5,2,2X")
            # self.read_sweep.parse = read_sweep_array
            self.visa_instrument.write(
                f"L{self.compliance_value},{self.compliance_range_value}X"
            )

    def Averages_put_function(self, value):
        self.averages_value = int(np.log2(int(value)))

    def Sweep_Hysteresis_put_function(self, value):
        self.Sweep_Hysteresis_value = value

    def Integration_time_put_function(self, value):
        self.Integration_time_value = get_integration_time_value(value)
        print(f"P{self.averages_value}XS{self.Integration_time_value}X")
        self.visa_instrument.write(
            f"P{self.averages_value}XS{self.Integration_time_value}X"
        )

    def set_voltage_function(self, set_value):
        write_string = ""
        if self.Source_Type.get() != "Voltage":
            raise Exception(
                'You can not set a voltage if the Source Type is not set to "Voltage"!'
            )
        if self.Source_Type_latest != "Voltage":
            self.Source_Type_latest = "Voltage"
            self.compliance_put_function("Voltage")
        write_string += (
            f"B{set_value},{self.source_range_value},{int(self.Bias_delay.get())}XN1X"
        )
        print(write_string)
        print(self.averages_value)
        return write_string

    def set_current_function(self, set_value):
        write_string = ""
        if self.Source_Type.get() != "Current":
            raise Exception(
                'You can not set a current if the Source Type is not set to "Current"!'
            )
        if self.Source_Type_latest != "Current":
            self.Source_Type_latest = "Current"
            self.compliance_put_function("Current")
        write_string += (
            f"B{set_value},{self.source_range_value},{int(self.Bias_delay.get())}XN1X"
        )
        print(write_string)
        print(self.averages_value)
        return write_string

    def read_current_function(
        self,
    ):
        if self.Source_Type.get() == "Voltage":
            self.visa_instrument.write("H0X")
        else:
            raise Exception(
                "Source Type is not Voltage. You can not measure current when not sourcing voltage."
            )
        return ""

    def read_voltage_function(
        self,
    ):
        if self.Source_Type.get() == "Current":
            self.visa_instrument.write("H0X")
        else:
            raise Exception(
                "Source Type is not Current. You can not measure voltage when not sourcing current."
            )
        return ""

    def start_voltage_sweep_function(self, passed_value):
        if not self.Source_Type.get() == "Sweep Voltage":
            raise Exception(
                "Source Type is not Sweep Voltage. You can not perform a voltage sweep with the current settings."
            )
        self.compliance_put_function("Sweep Voltage")
        if passed_value == 1:
            # Fixed level: points = counts
            if self.setSweep_Type.get() == 0:
                write_string = (
                    f"Q0,{self.setSweep_Level.get()},{self.compliance_range_value},"
                    f"{int(self.Bias_delay.get())},{self.setSweep_Points.get()}X"
                )
                if self.Sweep_Hysteresis_value:
                    write_string += (
                        f"Q6,{self.setSweep_Level.get()},{self.compliance_range_value},"
                        f"{int(self.Bias_delay.get())},{self.setSweep_Points.get()}X"
                    )

            # Linear stair
            elif self.setSweep_Type.get() == 1:
                write_string = (
                    f"Q1,{self.setSweep_Start.get()},{self.setSweep_Stop.get()},"
                    f"{self.setSweep_Step.get()},{self.compliance_range_value},{int(self.Bias_delay.get())}X"
                )
                if self.Sweep_Hysteresis_value:
                    write_string += (
                        f"Q7,{self.setSweep_Stop.get()},{self.setSweep_Start.get()},"
                        f"{self.setSweep_Step.get()},{self.compliance_range_value}, {int(self.Bias_delay.get())}X"
                    )
            # Logarithmic stair
            elif self.setSweep_Type.get() == 2:
                write_string = (
                    f"Q2,{self.setSweep_Start.get()},{self.setSweep_Stop.get()},"
                    f"{self.setSweep_Points.get()},{self.compliance_range_value}, {int(self.Bias_delay.get())}X"
                )
                if self.Sweep_Hysteresis_value:
                    write_string += (
                        f"Q8,{self.setSweep_Stop.get()},{self.setSweep_Start.get()},"
                        f"{self.setSweep_Points.get()},{self.compliance_range_value}, {int(self.Bias_delay.get())}X"
                    )
            # Fixed level pulsed
            elif self.setSweep_Type.get() == 3:
                write_string = (
                    f"Q3,{self.setSweep_Level.get()},{self.compliance_range_value},"
                    f"{self.setSweep_Pulses.get()},{self.setSweep_T_on.get()},{self.setSweep_T_off.get()}X"
                )
                if self.Sweep_Hysteresis_value:
                    write_string += (
                        f"Q9,{self.setSweep_Level.get()},{self.compliance_range_value},"
                        f"{self.setSweep_Pulses.get()},{self.setSweep_T_on.get()}, {self.setSweep_T_off.get()}X"
                    )
            # Linear Stair pulsed
            elif self.setSweep_Type.get() == 4:
                write_string = (
                    f"Q4,{self.setSweep_Start.get()},{self.setSweep_Stop.get()},"
                    f"{self.setSweep_Step.get()},{self.compliance_range_value}, "
                    f",{self.setSweep_T_on.get()}, {self.setSweep_T_off.get()}X"
                )
                if self.Sweep_Hysteresis_value:
                    write_string += (
                        f"Q10,{self.setSweep_Stop.get()},{self.setSweep_Start.get()},"
                        f"{self.setSweep_Step.get()},{self.compliance_range_value}, "
                        f",{self.setSweep_T_on.get()}, {self.setSweep_T_off.get()}X"
                    )
            # Logarithmic stair pulsed
            elif self.setSweep_Type.get() == 5:
                write_string = (
                    f"Q5,{self.setSweep_Start.get()},{self.setSweep_Stop.get()},"
                    f"{self.setSweep_Points.get()},{self.compliance_range_value}, "
                    f",{self.setSweep_T_on.get()}, {self.setSweep_T_off.get()}X"
                )
                if self.Sweep_Hysteresis_value:
                    write_string += (
                        f"Q11,{self.setSweep_Stop.get()},{self.setSweep_Start.get()},"
                        f"{self.setSweep_Points.get()},{self.compliance_range_value}, "
                        f",{self.setSweep_T_on.get()}, {self.setSweep_T_off.get()}X"
                    )
            write_string += "N1XH0X"
            print(write_string)
            return write_string

    def start_current_sweep_function(self, passed_value):
        if not self.Source_Type.get() == "Sweep Current":
            raise Exception(
                "Source Type is not Sweep Current. You can not perform a current sweep with the current settings."
            )
        self.compliance_put_function("Sweep Current")
        if passed_value == 1:
            # Fixed level: points = counts
            if self.setSweep_Type.get() == 0:
                write_string = (
                    f"Q0,{self.setSweep_Level.get()},{self.compliance_range_value},"
                    f"{int(self.Bias_delay.get())},{self.setSweep_Points.get()}X"
                )
                if self.Sweep_Hysteresis_value:
                    write_string += (
                        f"Q6,{self.setSweep_Level.get()},{self.compliance_range_value},"
                        f"{int(self.Bias_delay.get())},{self.setSweep_Points.get()}X"
                    )

            # Linear stair
            elif self.setSweep_Type.get() == 1:
                write_string = (
                    f"Q1,{self.setSweep_Start.get()},{self.setSweep_Stop.get()},"
                    f"{self.setSweep_Step.get()},{self.compliance_range_value},{int(self.Bias_delay.get())}X"
                )
                if self.Sweep_Hysteresis_value:
                    write_string += (
                        f"Q7,{self.setSweep_Stop.get()},{self.setSweep_Start.get()},"
                        f"{self.setSweep_Step.get()},{self.compliance_range_value}, {int(self.Bias_delay.get())}X"
                    )
            # Logarithmic stair
            elif self.setSweep_Type.get() == 2:
                write_string = (
                    f"Q2,{self.setSweep_Start.get()},{self.setSweep_Stop.get()},"
                    f"{self.setSweep_Points.get()},{self.compliance_range_value}, {int(self.Bias_delay.get())}X"
                )
                if self.Sweep_Hysteresis_value:
                    write_string += (
                        f"Q8,{self.setSweep_Stop.get()},{self.setSweep_Start.get()},"
                        f"{self.setSweep_Points.get()},{self.compliance_range_value}, {int(self.Bias_delay.get())}X"
                    )
            # Fixed level pulsed
            elif self.setSweep_Type.get() == 3:
                write_string = (
                    f"Q3,{self.setSweep_Level.get()},{self.compliance_range_value},"
                    f"{self.setSweep_Pulses.get()},{self.setSweep_T_on.get()},{self.setSweep_T_off.get()}X"
                )
                if self.Sweep_Hysteresis_value:
                    write_string += (
                        f"Q9,{self.setSweep_Level.get()},{self.compliance_range_value},"
                        f"{self.setSweep_Pulses.get()},{self.setSweep_T_on.get()}, {self.setSweep_T_off.get()}X"
                    )
            # Linear Stair pulsed
            elif self.setSweep_Type.get() == 4:
                write_string = (
                    f"Q4,{self.setSweep_Start.get()},{self.setSweep_Stop.get()},"
                    f"{self.setSweep_Step.get()},{self.compliance_range_value}, "
                    f",{self.setSweep_T_on.get()}, {self.setSweep_T_off.get()}X"
                )
                if self.Sweep_Hysteresis_value:
                    write_string += (
                        f"Q10,{self.setSweep_Stop.get()},{self.setSweep_Start.get()},"
                        f"{self.setSweep_Step.get()},{self.compliance_range_value}, "
                        f",{self.setSweep_T_on.get()}, {self.setSweep_T_off.get()}X"
                    )
            # Logarithmic stair pulsed
            elif self.setSweep_Type.get() == 5:
                write_string = (
                    f"Q5,{self.setSweep_Start.get()},{self.setSweep_Stop.get()},"
                    f"{self.setSweep_Points.get()},{self.compliance_range_value}, "
                    f",{self.setSweep_T_on.get()}, {self.setSweep_T_off.get()}X"
                )
                if self.Sweep_Hysteresis_value:
                    write_string += (
                        f"Q11,{self.setSweep_Stop.get()},{self.setSweep_Start.get()},"
                        f"{self.setSweep_Points.get()},{self.compliance_range_value}, "
                        f",{self.setSweep_T_on.get()}, {self.setSweep_T_off.get()}X"
                    )
            write_string += "N1XH0X"
            print(write_string)
            return write_string


if __name__ == "__main__":
    testk = Keithley_237(name="testk")
