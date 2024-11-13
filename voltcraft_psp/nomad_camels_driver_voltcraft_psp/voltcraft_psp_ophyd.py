from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.visa_signal import VISA_Device

from nomad_camels.bluesky_handling.custom_function_signal import Custom_Function_Signal, Custom_Function_SignalRO


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
        a = None
        for i in range(5):
            a = self.visa_instrument.read_bytes(1)
            print(a)
        return a

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
        b1 = bytes.fromhex("AA")
        b2 = val.to_bytes(2, "big")
        write_str = str(b1 + b2)
        print(write_str)
        self.visa_instrument.write(write_str)

    def set_voltage_limit(self, val):
        return
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
        b1 = bytes.fromhex("AD")
        b2 = val.to_bytes(2, "big")
        write_str = str(b1 + b2)
        print(write_str)
        self.visa_instrument.write(write_str)

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
        command_bytes = command_id.to_bytes(1, byteorder='big')
        val_bytes = val.to_bytes(2, byteorder='big')
        msg = command_bytes + val_bytes
        self.visa_instrument.write_raw(msg)

    def set_output_state(self, val):
        if val:
            val = 1
        else:
            val = 0
        b = bytes.fromhex("AB")
        b += val.to_bytes(1, "big")
        v2 = 0
        b += v2.to_bytes(1, "big")
        write_str = str(b)
        print(write_str)
        self.visa_instrument.write(write_str)
