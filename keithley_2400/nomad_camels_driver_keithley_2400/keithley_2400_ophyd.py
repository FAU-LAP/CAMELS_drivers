from ophyd import Component as Cpt
import re
from nomad_camels.bluesky_handling.visa_signal import (
    VISA_Signal,
    VISA_Signal_RO,
    VISA_Device,
)
from nomad_camels.bluesky_handling.custom_function_signal import Custom_Function_Signal


class Keithley_2400(VISA_Device):
    measure_voltage = Cpt(
        VISA_Signal_RO,
        name="measure_voltage",
        parse=r"^([+-].*),[+-].*,[+-].*,[+-].*,[+-].*$",
        parse_return_type="float",
        metadata={"units": "V", "description": "Measures voltage using READ?"},
    )
    measure_current = Cpt(
        VISA_Signal_RO,
        name="measure_current",
        parse=r"^[+-].*,([+-].*),[+-].*,[+-].*,[+-].*$",
        parse_return_type="float",
        metadata={"units": "A", "description": "Measures current using READ?"},
    )
    measure_resistance = Cpt(
        VISA_Signal_RO,
        name="measure_resistance",
        parse=r"^[+-].*,[+-].*,([+-].*),[+-].*,[+-].*$",
        parse_return_type="float",
        metadata={"units": "Ohm", "description": "Measures resistance using READ?"},
    )
    set_voltage = Cpt(
        VISA_Signal,
        name="set_voltage",
        parse_return_type=None,
        metadata={"units": "V", "description": "Sets voltage to desired value"},
    )
    set_current = Cpt(
        VISA_Signal,
        name="set_current",
        parse_return_type=None,
        metadata={"units": "A", "description": "Sets current to desired value"},
    )
    current_compliance = Cpt(
        Custom_Function_Signal,
        name="current_compliance",
        kind="config",
        metadata={"units": "A", "description": "Maximum allowed current. 1.05A max"},
    )  # Value is used but the actual channel does not set anything
    voltage_compliance = Cpt(
        Custom_Function_Signal,
        name="voltage_compliance",
        kind="config",
        metadata={"units": "V", "description": "Maximum allowed voltage. 210V max"},
    )  # Value is used but the actual channel does not set anything
    current_range_source = Cpt(
        Custom_Function_Signal,
        name="current_range_source",
        kind="config",
        metadata={
            "units": "A",
            "description": "Sets current sourcing range. 1.05A max",
        },
    )  # Value is used but the actual channel does not set anything
    voltage_range_source = Cpt(
        Custom_Function_Signal,
        name="voltage_range_source",
        kind="config",
        metadata={"units": "V", "description": "Sets voltage sourcing range. 210V max"},
    )  # Value is used but the actual channel does not set anything
    current_range_sense = Cpt(
        Custom_Function_Signal,
        name="current_range_sense",
        kind="config",
        metadata={"units": "A", "description": "Sets current sensing range. 1.05A max"},
    )  # Value is used but the actual channel does not set anything
    voltage_range_sense = Cpt(
        Custom_Function_Signal,
        name="voltage_range_sense",
        kind="config",
        metadata={"units": "V", "description": "Sets voltage sensing range. 210V max"},
    )  # Value is used but the actual channel does not set anything
    device_id = Cpt(
        VISA_Signal_RO,
        name="device_id",
        query="*IDN?",
        parse_return_type="str",
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
        self.measure_voltage.query = self.measure_voltage_query_function
        self.measure_current.query = self.measure_current_query_function
        self.measure_resistance.query = self.measure_resistance_query_function
        self.set_voltage.write = self.set_voltage_write_function
        self.set_current.write = self.set_current_write_function
        # self.current_range_sense.write = self.current_range_sense_write_function
        # self.voltage_range_sense.write = self.voltage_range_sense_write_function
        if name == "test":
            return
        self.source_function = None
        self.measure_function = None
        self.output_on = False
        self.set_voltage_compliance = (
            None  # None if nothing was set and True if it was set
        )
        self.set_current_compliance = (
            None  # None if nothing was set and True if it was set
        )
        self.set_voltage_range_sense = (
            None  # None if nothing was set and True if it was set
        )
        self.set_current_range_sense = (
            None  # None if nothing was set and True if it was set
        )
        self.set_voltage_range_source = (
            None  # None if nothing was set and True if it was set
        )
        self.set_current_range_source = (
            None  # None if nothing was set and True if it was set
        )
        # Set the data format to ASCII
        self.visa_instrument.write(":FORM:DATA ASC")

    def measure_voltage_query_function(self):
        # check if the voltage sensing range was set and if not set it
        if self.source_function != "voltage":
            if self.set_voltage_range_sense:
                pass
            else:
                value_voltage_range_sense = self.voltage_range_sense.get()
                self.visa_instrument.write(f":VOLT:RANG {value_voltage_range_sense}")
                self.set_voltage_range_sense = True

        # check if the measure function type is voltage and if not set it
        if self.measure_function != "voltage":
            self.visa_instrument.write(":CONF:VOLT")
            self.measure_function = "voltage"
        else:
            pass
        return ":READ?"

    def measure_current_query_function(self):
        # check if the current sensing range was set and if not set it
        if self.source_function != "current":
            if self.set_current_range_sense:
                pass
            else:
                value_current_range_sense = self.current_range_sense.get()
                self.visa_instrument.write(f":CURR:RANG {value_current_range_sense}")
                self.set_current_range_sense = True

        # check if the measure function type is current and if not set it
        if self.measure_function != "current":
            self.visa_instrument.write(":CONF:CURR")
            self.measure_function = "current"
        else:
            pass
        return ":READ?"

    def measure_resistance_query_function(self):
        # check if the voltage sensing range was set and if not set it
        if self.source_function != "voltage":
            if self.set_voltage_range_sense:
                pass
            else:
                value_voltage_range_sense = self.voltage_range_sense.get()
                self.visa_instrument.write(f":VOLT:RANG {value_voltage_range_sense}")
                self.set_voltage_range_sense = True

        # check if the current sensing range was set and if not set it
        if self.source_function != "current":
            if self.set_current_range_sense:
                pass
            else:
                value_current_range_sense = self.current_range_sense.get()
                self.visa_instrument.write(f":CURR:RANG {value_current_range_sense}")
                self.set_current_range_sense = True

        if self.measure_function != "resistance":
            self.visa_instrument.write(":CONF:RES")
            self.measure_function = "resistance"
        else:
            pass
        return ":READ?"

    def set_voltage_write_function(self, value):
        # check if current compliance is already set and if not set it
        if self.set_current_compliance:
            pass
        else:
            value_current_compliance = self.current_compliance.get()
            self.visa_instrument.write(f"CURR:PROT {value_current_compliance}")
            self.set_current_compliance = True

        # check if voltage range is set and if not set it
        if self.set_voltage_range_source:
            pass
        else:
            value_voltage_range_source = self.voltage_range_source.get()
            # set sensing range:
            self.visa_instrument.write(f":SOUR:VOLT:RANG {value_voltage_range_source}")
            # set current sourcing range:

            self.set_voltage_range_source = True

        # check if the source function type is voltage and if not set it
        if self.source_function != "voltage":
            # can not set voltage if measuring resistance
            if re.search(r'"RES"', self.visa_instrument.query(":CONF?")):
                self.visa_instrument.write(":CONF:CURR")
                self.measure_function = "current"
            self.visa_instrument.write(":SOUR:FUNC VOLT")
            self.source_function = "voltage"
        else:
            pass

        # check if the output is on and if not turn it on
        if self.output_on:
            pass
        else:
            self.visa_instrument.write(":OUTP 1")
        return f":SOUR:VOLT {value}"

    def set_current_write_function(self, value):
        # check if voltage compliance is already set and if not set it
        if self.set_voltage_compliance:
            pass
        else:
            value_voltage_compliance = self.voltage_compliance.get()
            self.visa_instrument.write(f"SENS:VOLT:PROT {value_voltage_compliance}")
            self.set_voltage_compliance = True

        # check if current range is set and if not set it
        if self.set_current_range_source:
            pass
        else:
            value_current_range_source = self.current_range_source.get()
            self.visa_instrument.write(f"SOUR:CURR:RANG {value_current_range_source}")
            self.set_current_range_source = True

        # check if the source function type is current and if not set it
        if self.source_function != "current":
            # can not set voltage if measuring resistance
            if re.search(r'"RES"', self.visa_instrument.query(":CONF?")):
                self.visa_instrument.write(":CONF:VOLT")
                self.measure_function = "voltage"
            self.visa_instrument.write(":SOUR:FUNC CURR")
            self.source_function = "current"
        else:
            pass

        # check if the output is on and if not turn it on
        if self.output_on:
            pass
        else:
            self.visa_instrument.write(":OUTP 1")
        return f":SOUR:CURR {value}"

    # def current_range_sense_write_function(self, value):
    # 	return f':CURR:RANG {value}'

    # def voltage_range_sense_write_function(self, value):
    # 	return f':VOLT:RANG {value}'

    def finalize_steps(self):
        self.visa_instrument.write("OUTP 0")
