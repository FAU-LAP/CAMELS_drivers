from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.custom_function_signal import (
    Custom_Function_Signal,
    Custom_Function_SignalRO,
    Sequential_Device,
)
from ophyd import Device
from pylablib.devices import Attocube


def make_attocube_anc300_instance(
    prefix="",
    *args,
    name,
    kind=None,
    read_attrs=None,
    configuration_attrs=None,
    parent=None,
    available_axis_numbers=None,
    ip_address=None,
    port=None,
    com_port=None,
    connection_type=None,
    **kwargs,
):
    ophyd_class = make_attocube_anc300_class(available_axis_numbers)
    return ophyd_class(
        prefix,
        *args,
        name=name,
        kind=kind,
        read_attrs=read_attrs,
        configuration_attrs=configuration_attrs,
        parent=parent,
        available_axis_numbers=available_axis_numbers,
        ip_address=ip_address,
        port=port,
        com_port=com_port,
        connection_type=connection_type,
        **kwargs,
    )


def make_attocube_anc300_class(available_axis_numbers):
    def set_frequency_generator(axis_number):
        def set_frequency(_self_instance, value):
            return lambda: _self_instance.parent.set_frequency(axis_number, value)

        return set_frequency

    def set_voltage_generator(axis_number):
        def set_voltage(_self_instance, value):
            return lambda: _self_instance.parent.set_voltage(axis_number, value)

        return set_voltage

    def set_mode_generator(axis_number):
        def set_mode(_self_instance, value):
            return lambda: _self_instance.parent.set_mode(axis_number, value)

        return set_mode

    def set_offset_generator(axis_number):
        def set_offset(_self_instance, value):
            return lambda: _self_instance.parent.set_offset(axis_number, value)

        return set_offset

    def wait_move_generator(axis_number):
        def wait_move(_self_instance, value):
            return lambda: _self_instance.parent.wait_move(axis_number, value)

        return wait_move

    def move_by_generator(axis_number):
        def move_by(_self_instance, value):
            return lambda: _self_instance.parent.move_by(axis_number, value)

        return move_by

    def jog_generator(axis_number):
        def jog(_self_instance, value):
            return lambda: _self_instance.parent.jog(axis_number, value)

        return jog

    def stop_generator(axis_number):
        def stop(_self_instance, value):
            return lambda: _self_instance.parent.stop(axis_number, value)

        return stop

    def get_capacitance_generator(axis_number):
        def get_capacitance(_self_instance):
            return lambda: _self_instance.parent.get_capacitance(axis_number)

        return get_capacitance

    def get_frequency_generator(axis_number):
        def get_frequency(_self_instance):
            return lambda: _self_instance.parent.get_frequency(axis_number)

        return get_frequency

    def get_voltage_generator(axis_number):
        def get_voltage(_self_instance):
            return lambda: _self_instance.parent.get_voltage(axis_number)

        return get_voltage

    def get_mode_generator(axis_number):
        def get_mode(_self_instance):
            return lambda: _self_instance.parent.get_mode(axis_number)

        return get_mode

    signal_dictionary = {}
    device_string = f"attocube_anc300_axis"
    for axis in available_axis_numbers:
        axis = int(axis)
        signal_dictionary[f"set_frequency_{axis}"] = Cpt(
            Custom_Function_Signal,
            name=f"set_frequency_{axis}",
            metadata={"units": "Hz", "description": f"Set frequency for axis {axis}"},
            put_function=set_frequency_generator(axis),
        )
        signal_dictionary[f"set_voltage_{axis}"] = Cpt(
            Custom_Function_Signal,
            name=f"set_voltage_{axis}",
            metadata={"units": "V", "description": f"Set voltage for axis {axis}"},
            put_function=set_voltage_generator(axis),
        )
        signal_dictionary[f"set_mode_{axis}"] = Cpt(
            Custom_Function_Signal,
            name=f"set_mode_{axis}",
            metadata={"units": "", "description": f"Set mode for axis {axis}"},
            put_function=set_mode_generator(axis),
        )
        signal_dictionary[f"set_offset_{axis}"] = Cpt(
            Custom_Function_Signal,
            name=f"set_offset_{axis}",
            metadata={"units": "V", "description": f"Set offset for axis {axis}"},
            put_function=set_offset_generator(axis),
        )
        signal_dictionary[f"wait_move_{axis}"] = Cpt(
            Custom_Function_Signal,
            name=f"wait_move_{axis}",
            metadata={
                "units": "",
                "description": f"Wait for axis {axis} to finish moving",
            },
            put_function=wait_move_generator(axis),
        )
        signal_dictionary[f"move_by_{axis}"] = Cpt(
            Custom_Function_Signal,
            name=f"move_by_{axis}",
            metadata={
                "units": "steps",
                "description": f"Move axis {axis} by a certain number of steps",
            },
            put_function=move_by_generator(axis),
        )
        signal_dictionary[f"jog_{axis}"] = Cpt(
            Custom_Function_Signal,
            name=f"jog_{axis}",
            metadata={
                "units": "steps",
                "description": f"Jog axis {axis} by a certain number of steps until a new step command or stop is sent.",
            },
            put_function=jog_generator(axis),
        )
        signal_dictionary[f"stop_{axis}"] = Cpt(
            Custom_Function_Signal,
            name=f"stop_{axis}",
            metadata={
                "units": "",
                "description": f"Stop axis {axis}",
            },
            put_function=stop_generator(axis),
        )
        signal_dictionary[f"get_capacitance_{axis}"] = Cpt(
            Custom_Function_SignalRO,
            name=f"get_capacitance_{axis}",
            metadata={"units": "F", "description": f"Get capacitance for axis {axis}"},
            read_function=get_capacitance_generator(axis),
        )
        signal_dictionary[f"get_frequency_{axis}"] = Cpt(
            Custom_Function_SignalRO,
            name=f"get_frequency_{axis}",
            metadata={"units": "Hz", "description": f"Get frequency for axis {axis}"},
            read_function=get_frequency_generator(axis),
        )
        signal_dictionary[f"get_voltage_{axis}"] = Cpt(
            Custom_Function_SignalRO,
            name=f"get_voltage_{axis}",
            metadata={"units": "V", "description": f"Get voltage for axis {axis}"},
            read_function=get_voltage_generator(axis),
        )
        signal_dictionary[f"get_mode_{axis}"] = Cpt(
            Custom_Function_SignalRO,
            name=f"get_mode_{axis}",
            metadata={"units": "", "description": f"Get mode for axis {axis}"},
            read_function=get_mode_generator(axis),
        )
        device_string += f"_{axis}"

    return type(
        device_string,
        (Attocube_Anc300,),
        {**signal_dictionary},
    )


class Attocube_Anc300(Sequential_Device):
    get_full_info = Cpt(
        Custom_Function_SignalRO,
        name="get_full_info",
        metadata={"units": "", "description": "Get full instrument info"},
        kind="config",
    )

    read_instrument = Cpt(
        Custom_Function_SignalRO,
        name="read_instrument",
        metadata={
            "units": "",
            "description": "Read the instrument. You must have used 'write_instrument' loop step before.\nUses Attocube.ANC300.instr.read_multichar_term",
        },
    )

    write_instrument = Cpt(
        Custom_Function_Signal,
        name="write_instrument",
        metadata={
            "units": "",
            "description": "Write arbitrary string to instrument. Uses Attocube.ANC300.instr.write\nUse single quotation marks: ' around string in value field, like: 'write this'\nUse 'read instrument' in the next loop step to read the resposne to the write.",
        },
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
        available_axis_numbers=None,
        ip_address=None,
        port=None,
        com_port=None,
        connection_type=None,
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
        # Set True to force the attocube ANC300 to execute its commands sequentially
        self.force_sequential = True
        self.get_full_info.read_function = self.get_full_info_function
        self.read_instrument.read_function = self.read_instrument_function
        self.write_instrument.put_function = self.write_instrument_function

        if connection_type == "USB":
            self.atc = Attocube.ANC300(f"COM{com_port}")
        elif connection_type == "Ethernet":
            self.atc = Attocube.ANC300((ip_address, int(port)))

    def get_full_info_function(self):
        self.atc.get_full_info()

    def write_instrument_function(self, value):
        self.atc.instr.flush_read()
        self.atc.instr.write(f"{value}")

    def read_instrument_function(self):
        reply = self.atc.instr.read_multichar_term(["ERROR", "OK"], remove_term=False)
        if reply:
            if isinstance(reply, bytes):
                reply = reply.decode()
                # Split the string at the newline character and take the first part
                parsed_reply = reply.split("\n", 1)[0]
        else:
            raise ValueError("No reply from the ANC300 using instr.read_multichar_term")
        return parsed_reply

    def set_frequency(self, axis_number, value):
        self.atc.set_frequency(axis_number, value)

    def set_voltage(self, axis_number, value):
        self.atc.set_voltage(axis_number, value)

    def set_mode(self, axis_number, value):
        self.atc.set_mode(axis_number, value)

    def set_offset(self, axis_number, value):
        self.atc.set_offset(axis_number, value)

    def wait_move(self, axis_number, value):
        self.atc.wait_move(axis_number)

    def move_by(self, axis_number, value):
        self.atc.move_by(axis_number, value)

    def jog(self, axis_number, value):
        if direction not in ["up", "down", "+", "-"]:
            raise ValueError("Direction must be '+' or 'up'; or '-' or 'down'")
        if value == "up" or "+":
            direction = True
        elif value == "down" or "-":
            direction = False
        self.atc.jog(axis_number, direction)

    def stop(self, axis_number, value):
        self.atc.stop(axis_number)

    def get_frequency(self, axis_number):
        return self.atc.get_frequency(axis_number)

    def get_voltage(self, axis_number):
        return self.atc.get_voltage(axis_number)

    def get_mode(self, axis_number):
        return self.atc.get_mode(axis_number)

    def get_offset(self, axis_number):
        return self.atc.get_offset(axis_number)

    def get_capacitance(self, axis_number):
        return self.atc.get_capacitance(axis_number)
