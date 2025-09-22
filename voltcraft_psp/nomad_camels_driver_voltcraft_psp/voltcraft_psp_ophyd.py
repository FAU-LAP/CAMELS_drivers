from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.visa_signal import VISA_Device

from nomad_camels.bluesky_handling.custom_function_signal import (
    Custom_Function_Signal,
    Custom_Function_SignalRO,
)


class Voltcraft_PSP(VISA_Device):
    set_V = Cpt(
        Custom_Function_Signal,
        name="set_V",
        metadata={"unit": "V", "description": "sets the output voltage"},
    )
    output_state = Cpt(
        Custom_Function_Signal,
        name="output_state",
        metadata={"description": "turns the output on or off"},
    )

    idn = Cpt(
        Custom_Function_SignalRO,
        name="idn",
    )

    voltage_limit = Cpt(
        Custom_Function_Signal,
        name="voltage_limit",
        metadata={"unit": "V", "description": "sets the voltage limit"},
        kind="config",
    )
    current_limit = Cpt(
        Custom_Function_Signal,
        name="current_limit",
        metadata={"unit": "A", "description": "sets the current limit"},
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
        model="PSP 1803",
        **kwargs,
    ):
        super().__init__(
            prefix=prefix,
            name=name,
            kind=kind,
            read_attrs=read_attrs,
            configuration_attrs=configuration_attrs,
            parent=parent,
            **kwargs,
        )
        self.psp_model = model
        self.set_V.put_function = self.set_voltage
        self.output_state.put_function = self.set_output_state
        self.voltage_limit.put_function = self.set_voltage_limit
        self.current_limit.put_function = self.set_current_limit
        self.idn.read_function = self.read_idn

    def read_idn(self):
        state_info = 0xB2.to_bytes(1, byteorder="big")
        info = None
        while info != state_info:
            info = self.visa_instrument.read_bytes(1)
        model_number = self.visa_instrument.read_bytes(1)
        model_number_int = int.from_bytes(model_number, byteorder="big")
        software_version = self.visa_instrument.read_bytes(1)
        software_version_int = int.from_bytes(software_version, byteorder="big")
        model = None
        if model_number_int == 1:
            model = "PSP 1405"
        elif model_number_int == 2:
            model = "PSP 12010"
        elif model_number_int == 3:
            model = "PSP 1803"
        if model != self.psp_model:
            raise ValueError("Model number does not match")
        return f"{model} software version {software_version_int}"

    def set_voltage(self, val):
        if self.psp_model == "PSP 1405":
            if not 0 <= val <= 40:
                raise ValueError("Voltage out of range")
            val *= 100
        elif self.psp_model == "PSP 12010":
            if not 0 <= val <= 20:
                raise ValueError("Voltage out of range")
            val *= 200
        elif self.psp_model == "PSP 1803":
            if not 0 <= val <= 80:
                raise ValueError("Voltage out of range")
            val *= 50
        val = int(val)
        command_id = 0xAA
        command_bytes = command_id.to_bytes(1, byteorder="big")
        val_bytes = val.to_bytes(2, byteorder="big")
        msg = command_bytes + val_bytes
        self.visa_instrument.write_raw(msg)

    def set_voltage_limit(self, val):
        if self.psp_model == "PSP 1405":
            if not 0 <= val <= 40:
                raise ValueError("Voltage out of range")
            val *= 10
        elif self.psp_model == "PSP 12010":
            if not 0 <= val <= 20:
                raise ValueError("Voltage out of range")
            val *= 20
        elif self.psp_model == "PSP 1803":
            if not 0 <= val <= 80:
                raise ValueError("Voltage out of range")
            val *= 5
        val = int(val)
        command_id = 0xAD
        command_bytes = command_id.to_bytes(1, byteorder="big")
        val_bytes = val.to_bytes(2, byteorder="big")
        msg = command_bytes + val_bytes
        self.visa_instrument.write_raw(msg)

    def set_current_limit(self, val):
        if self.psp_model == "PSP 1405":
            if not 0 <= val <= 5:
                raise ValueError("Current out of range")
            val *= 100
        elif self.psp_model == "PSP 12010":
            if not 0 <= val <= 10:
                raise ValueError("Current out of range")
            val *= 50
        elif self.psp_model == "PSP 1803":
            if not 0 <= val <= 3:
                raise ValueError("Current out of range")
            val *= 200
        val = int(val)
        command_id = 0xAC
        command_bytes = command_id.to_bytes(1, byteorder="big")
        val_bytes = val.to_bytes(2, byteorder="big")
        msg = command_bytes + val_bytes
        self.visa_instrument.write_raw(msg)

    def set_output_state(self, val):
        if val:
            val = 1
        else:
            val = 0
        command_id = 0xAB
        command_bytes = command_id.to_bytes(1, byteorder="big")
        val_bytes = val.to_bytes(1, byteorder="big")
        add_byte = 0
        add_byte = add_byte.to_bytes(1, byteorder="big")
        msg = command_bytes + val_bytes + add_byte
        self.visa_instrument.write_raw(msg)
