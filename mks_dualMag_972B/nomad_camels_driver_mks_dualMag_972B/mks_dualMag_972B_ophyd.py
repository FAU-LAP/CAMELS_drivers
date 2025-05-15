from ophyd import Component as Cpt
from ophyd import Device
from nomad_camels.bluesky_handling.custom_function_signal import (
    Custom_Function_Signal,
    Custom_Function_SignalRO,
)
from nomad_camels.bluesky_handling.visa_signal import VISA_Device

import pyvisa
import time
import re

import pyvisa.constants


_NAK_MESSAGES = {
    500008: "Zero adjustment at too high pressure",
    500009: "Atmospheric adjustment at too low",
    500160: "Unrecognized message",
    500169: "Invalid argument",
    500172: "Value out of range",
    500175: "Command/query character invalid",
    500180: "Protected setting (locked)",
    500195: "Control setpoint enabled (ENC)",
}

gas_types = {
    "Nitrogen": "NITROGEN",
    "Air": "AIR",
    "Argon": "ARGON",
    "Helium": "HELIUM",
    "Hydrogen": "HYDROGEN",
    "Water vapor": "H2O",
    "Neon": "NEON",
    "CO2": "CO2",
    "Xenon": "XENON",
}

pressure_units = {
    "Torr": "TORR",
    "mBar": "MBAR",
    "Pa": "PASCAL",
}


class MKS_DualMag_972B(VISA_Device):
    pressure = Cpt(
        Custom_Function_SignalRO,
        name="pressure",
        metadata={
            "units": "pressure_unit_value",
            "description": "Pressure reading from the MKS DualMag 972B",
        },
    )
    pressure_unit = Cpt(
        Custom_Function_Signal,
        name="pressure_unit",
        metadata={
            "description": "Pressure unit of the MKS DualMag 972B",
        },
        kind="config",
    )
    gas_type = Cpt(
        Custom_Function_Signal,
        name="gas_type",
        metadata={
            "description": "Gas type of the MKS DualMag 972B",
        },
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
        timeout=2000,
        retry_on_error=0,
        retry_on_timeout=False,
        software_address=253,
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
            read_termination=";",
            write_termination="\x0c",
            baud_rate=9600,
            timeout=timeout,
            retry_on_error=retry_on_error,
            retry_on_timeout=retry_on_timeout,
            **kwargs,
        )
        self.software_address = software_address

        self.pressure.read_function = self.read_pressure
        self.pressure_unit.put_function = self.set_pressure_unit
        self.gas_type.put_function = self.set_gas_type

        if name != "test":
            self.visa_instrument.parity = pyvisa.constants.Parity.none
            self.visa_instrument.data_bits = 8
            self.visa_instrument.stop_bits = pyvisa.constants.StopBits.one

    def set_gas_type(self, gas_type):
        if gas_type in gas_types:
            gas_type = gas_types[gas_type]
        if gas_type not in gas_types.values():
            raise ValueError(
                f"Invalid gas type: {gas_type}. Valid options are: {', '.join(gas_types)}"
            )
        self.communicate("GT", gas_type)

    def set_pressure_unit(self, unit):
        if unit in pressure_units:
            unit = pressure_units[unit]
        if unit not in pressure_units.values():
            raise ValueError(
                f"Invalid pressure unit: {unit}. Valid options are: {', '.join(pressure_units)}"
            )
        self.communicate("U", unit)

    def read_pressure(self):
        return float(self.communicate("PR4"))

    def communicate(self, command, parameter):
        # 1) Build the outgoing string
        if parameter != "?":
            parameter = "!" + parameter
        full_cmd = f"@{self.software_address}{command}{parameter}"
        # write() will automatically append inst.write_termination == '\x0C'
        self.visa_instrument.write(full_cmd)

        # 2) Read until we see the ';' terminator (pyvisa.read() blocks until read_termination)
        start = time.time()
        # we rely on inst.timeout to break out if the device never replies at all,
        # but we also enforce our own timeout_s for extra safety
        raw = ""
        while True:
            try:
                chunk = self.visa_instrument.read()  # reads up to and including the ';'
            except pyvisa.errors.VisaIOError:
                # Timeout at the VISA layer
                raise TimeoutError("No response from device (VISA timeout)")
            raw += chunk
            if ";" in raw:
                break
            if (time.time() - start) > self.visa_instrument.timeout / 1000:
                raise TimeoutError("No complete response (';' terminator) from device")

        # 3) Parse: expect something like "003 ACK 1.2345;" or "001 NAK 500008;"
        m = re.match(r"\s*(\d{3})\s+(\S+)\s+([^;]+);", raw)
        if not m:
            raise ValueError(f"Unexpected response format: {raw!r}")

        cmd_name = m.group(2)
        value_str = m.group(3).strip()

        # 4) Handle NAKs by mapping the numeric code to your message list
        if cmd_name.upper() == "NAK":
            try:
                code = int(value_str)
            except ValueError:
                raise Exception(
                    f"Device returned NAK with non-numeric code: {value_str!r}"
                )

            msg = _NAK_MESSAGES.get(code, f"Unknown error code {code}")
            raise Exception(f"Device NAK: {msg} (code {code})")

        # 5) Otherwise, return the “value” token
        return value_str
