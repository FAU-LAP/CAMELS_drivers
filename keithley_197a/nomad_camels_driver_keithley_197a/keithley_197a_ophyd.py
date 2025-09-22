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


class Keithley_197A(VISA_Device):
    read_DC_voltage = Cpt(
        VISA_Signal_RO,
        name="read_DC_voltage",
        query="T1X",
        parse="NDCV([+-]?\d+(?:\.\d+)?[Ee][+-]?\d+)",
        parse_return_type="float",
        metadata={
            "units": "V",
            "description": "reads DC voltage and strips the NDCV string part",
        },
    )
    read_DC_current = Cpt(
        VISA_Signal_RO,
        name="read_DC_current",
        query="T1X",
        parse="NDCA([+-]?\d+(?:\.\d+)?[Ee][+-]?\d+)",
        parse_return_type="float",
        metadata={
            "units": "A",
            "description": "reads DC current and strips the NDCA string part",
        },
    )
    read_AC_voltage = Cpt(
        VISA_Signal_RO,
        name="read_AC_voltage",
        query="T1X",
        parse="NACV([+-]?\d+(?:\.\d+)?[Ee][+-]?\d+)",
        parse_return_type="str",
        metadata={"units": "", "description": ""},
    )
    read_AC_current = Cpt(
        VISA_Signal_RO,
        name="read_AC_current",
        query="T1X",
        parse="NACA([+-]?\d+(?:\.\d+)?[Ee][+-]?\d+)",
        parse_return_type="str",
        metadata={"units": "", "description": ""},
    )
    measure_range = Cpt(
        VISA_Signal,
        name="measure_range",
        parse_return_type=None,
        kind="config",
        metadata={"units": "", "description": ""},
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
        # self.measure_range.write = self.measure_range_write_function
        if name == "test":
            return
        self.visa_instrument.write(
            "G0"
        )  # set data format to have the readings with header, G1 for no header

    def finalize_steps(self):
        """This function is called when the device is not used anymore. It is used for example to close the connection to the device."""
        pass
        # self.visa_instrument.close()

    def measure_range_write_function(self, value):
        # pass
        if value == "Auto":
            self.visa_instrument.write("R0")
        elif value == "200mV":
            self.visa_instrument.write("R1")
        elif value == "2V":
            self.visa_instrument.write("R2")
        elif value == "20V":
            self.visa_instrument.write("R3")
        elif value == "200V":
            self.visa_instrument.write("R4")
        elif value == "2000V":
            self.visa_instrument.write("R5")
        elif value == "10A":
            self.visa_instrument.write("R6")
