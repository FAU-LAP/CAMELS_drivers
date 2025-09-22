from ophyd import Component as Cpt
from typing import Dict, Tuple
from ophyd import Device, Signal, SignalRO
from nomad_camels.bluesky_handling.custom_function_signal import (
    Custom_Function_Signal,
    Custom_Function_SignalRO,
    Sequential_Device,
)

from pylablib.devices import Toptica
import time


def make_ophyd_instance_iBeam(
    prefix="",
    *args,
    name,
    kind=None,
    read_attrs=None,
    configuration_attrs=None,
    parent=None,
    resource_name="",
    baudrate=115200,
    channels=None,
    Com_port="",
    **kwargs,
):
    ophyd_class = make_ophyd_class(channels)
    return ophyd_class(
        prefix,
        *args,
        name=name,
        kind=kind,
        read_attrs=read_attrs,
        configuration_attrs=configuration_attrs,
        parent=parent,
        resource_name=resource_name,
        baudrate=baudrate,
        channels=channels,
        Com_port=Com_port,
        **kwargs,
    )


def make_ophyd_class(
    channels,
):
    def read_function_generator(channel_number):
        def read_function(_self_instance):
            """
            This function returns a lambda function that reads the power of the specified channe.
            the read_function is added to the signal as a read_function.
            The _self_instance will later be resolved to the parent of the instance of the Ibeam_smart class that the signal belongs to.

            Parameters:
            _self_instance (object): The parent instance.

            Returns:
            function: A lambda function that reads the power channel.

            """
            return lambda: _self_instance.parent.read_power_channel(channel_number)

        return read_function

    def enable_channel_generator(channel_number):
        def enable_channel(_self_instance, value):
            """
            This function returns a lambda function that enables the specified channel.
            the enable_channel is added to the signal as a put_function.
            The _self_instance will later be resolved to the parent of the instance of the Ibeam_smart class that the signal belongs to.
            """
            return lambda: _self_instance.parent.enable_channel(channel_number)

        return enable_channel

    def set_power_generator(channel_number):
        def set_power(_self_instance, value):
            """
            This function returns a lambda function that sets the power of the specified channel.
            the set_power is added to the signal as a put_function.
            The _self_instance will later be resolved to the parent of the instance of the Ibeam_smart class that the signal belongs to.
            """
            return lambda: _self_instance.parent.set_power_channel(
                channel_number, value
            )

        return set_power

    def disable_channel_generator(channel_number):
        def disable_channel(_self_instance, value):
            """
            This function returns a lambda function that disables the specified channel.
            the disable_channel is added to the signal as a put_function.
            The _self_instance will later be resolved to the parent of the instance of the Ibeam_smart class that the signal belongs to.
            """
            return lambda: _self_instance.parent.disable_channel(channel_number)

        return disable_channel

    signal_dictionary = {}
    for channel_number in channels:
        channel_number = int(channel_number)
        # For each channel add read_power function
        signal_dictionary[f"read_power_channel_{channel_number}"] = Cpt(
            Custom_Function_SignalRO,
            name=f"read_power_channel_{channel_number}",
            metadata={"units": "", "description": ""},
            read_function=read_function_generator(channel_number),
        )
        # For each channel add enable_channel function
        signal_dictionary[f"enable_channel_{channel_number}"] = Cpt(
            Custom_Function_Signal,
            name=f"enable_channel_{channel_number}",
            metadata={"units": "", "description": ""},
            put_function=enable_channel_generator(channel_number),
        )
        # For each channel add set_power function
        signal_dictionary[f"set_power_channel_{channel_number}"] = Cpt(
            Custom_Function_Signal,
            name=f"set_power_channel_{channel_number}",
            metadata={
                "units": "W",
                "description": f"Power of channel {channel_number} in W",
            },
            put_function=set_power_generator(channel_number),
        )
        # For each channel add disable_channel function
        signal_dictionary[f"disable_channel_{channel_number}"] = Cpt(
            Custom_Function_Signal,
            name=f"disable_channel_{channel_number}",
            metadata={"units": "", "description": ""},
            put_function=disable_channel_generator(channel_number),
        )

    return type(
        f"iBeam_Smart_total_channels_{len(channels)}",
        (Ibeam_Smart,),
        {**signal_dictionary},
    )


class Ibeam_Smart(Sequential_Device):
    laser_data = Cpt(
        Custom_Function_SignalRO,
        name="laser_data",
        value=None,
        kind="config",
        metadata={"units": "", "description": ""},
    )
    laser_info = Cpt(
        Custom_Function_SignalRO,
        name="laser_info",
        value=None,
        kind="config",
        metadata={"units": "", "description": ""},
    )
    read_laser_temp = Cpt(
        Custom_Function_SignalRO,
        name="read_laser_temp",
        metadata={"units": "", "description": ""},
    )
    use_FINE = Cpt(
        Custom_Function_Signal,
        name="use_FINE",
        kind="config",
        metadata={"units": "", "description": ""},
    )
    use_SKILL = Cpt(
        Custom_Function_Signal,
        name="use_SKILL",
        kind="config",
        metadata={"units": "", "description": ""},
    )
    use_FINE_type = Cpt(
        Custom_Function_Signal,
        name="use_FINE_type",
        kind="config",
        metadata={"units": "", "description": ""},
    )
    use_SKILL_type = Cpt(
        Custom_Function_Signal,
        name="use_SKILL_type",
        kind="config",
        metadata={"units": "", "description": ""},
    )
    enable_output = Cpt(
        Custom_Function_Signal,
        name="enable_output",
        metadata={"units": "", "description": ""},
    )
    disable_output = Cpt(
        Custom_Function_Signal,
        name="disable_output",
        metadata={"units": "", "description": ""},
    )
    enable_digitial_modulation = Cpt(
        Custom_Function_Signal,
        name="enable_digitial_modulation",
        metadata={"units": "", "description": ""},
    )
    disable_digitial_modulation = Cpt(
        Custom_Function_Signal,
        name="disable_digitial_modulation",
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
        baudrate=115200,
        channels=None,
        Com_port="",
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
        if name == "test":
            return
        # The following line forces the channels to wait for others to finish before setting and reading
        # This is because Custom_Function_SignalRO and Custom_Function_Signal are typically run asynchronously
        self.force_sequential = True
        self.laser = Toptica.TopticaIBeam((f"COM{Com_port}", baudrate))
        self.channels = channels
        self.read_laser_temp.read_function = self.read_laser_temp_read_function
        self.laser_data.read_function = self.read_laser_data_read_function
        self.laser_info.read_function = self.read_laser_info_read_function
        self.use_FINE.put_function = self.set_FINE_function
        self.use_SKILL.put_function = self.set_SKILL_function
        self.enable_output.put_function = self.enable_output_function
        self.disable_output.put_function = self.disable_output_function
        self.enable_digitial_modulation.put_function = (
            self.enable_digitial_modulation_function
        )
        self.disable_digitial_modulation.put_function = (
            self.disable_digitial_modulation_function
        )

    def read_laser_temp_read_function(self):
        return str(self.laser.get_temperatures())

    def read_laser_data_read_function(self):
        return str(self.laser.get_full_data())

    def read_laser_info_read_function(self):
        return str(self.laser.get_full_info())

    def set_FINE_function(self, value):
        if value:
            self.laser.query(f"fine {value}", reply=False)
            self.laser.query("fine on", reply=False)

    def set_SKILL_function(self, value):
        if value:
            self.laser.query(f"skill {value}", reply=False)
            self.laser.query("skill on", reply=False)

    def read_power_channel(self, channel_number):
        try:
            return self.laser.get_channel_power(channel_number)
        except:
            print("failed to read power")

    def set_power_channel(self, channel_number, value):
        try:
            self.laser.set_channel_power(channel_number, value)
        except:
            print("failed to set power")

    def enable_channel(self, channel_number):
        try:
            if not self.laser.is_channel_enabled(channel_number):
                self.laser.enable_channel(channel_number)
        except:
            print("failed to enable channel")

    def disable_channel(self, channel_number):
        try:
            if self.laser.is_channel_enabled(channel_number):
                self.laser.enable_channel(channel_number, enabled=False)
        except:
            print("failed to disable channel")

    def enable_output_function(self, value):
        try:
            if not self.laser.is_enabled():
                self.laser.enable()
        except:
            print("failed to enable output")

    def disable_output_function(self, value):
        try:
            if self.laser.is_enabled():
                self.laser.enable(enabled=False)
        except:
            print("failed to disable output")

    def enable_digitial_modulation_function(self, value):
        try:
            self.laser.query("en ext", reply=False)
        except:
            print("failed to enable digital modulation")

    def disable_digitial_modulation_function(self, value):
        try:
            self.laser.query("di ext", reply=False)
        except:
            print("failed to disable digital modulation")

    def finalize_steps(self):
        self.laser.close()
