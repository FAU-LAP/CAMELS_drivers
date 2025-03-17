from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.custom_function_signal import (
    Custom_Function_Signal,
    Custom_Function_SignalRO,
)
from ophyd import Device
from epics import PV


def make_ophyd_instance_epics(
    prefix="",
    *args,
    name,
    kind=None,
    read_attrs=None,
    configuration_attrs=None,
    parent=None,
    # These are the arguments you want to pass to the ophyd class
    # These are the settings you defined in the .py file
    # We will pass the number of channels we selected in the drop down and are defined in the .py file
    pvs=None,
    **kwargs,
):
    ophyd_class = make_ophyd_class(pvs)
    return ophyd_class(
        prefix,
        *args,
        name=name,
        kind=kind,
        read_attrs=read_attrs,
        configuration_attrs=configuration_attrs,
        parent=parent,
        # These are the arguments you want to pass to the ophyd class
        # These are the settings you defined in the .py file
        # We will pass the number of channels we selected in the drop down and are defined in the .py file
        pvs=pvs,
        **kwargs,
    )


def make_ophyd_class(pvs):
    def read_function_generator(short_name, full_name):
        def read_function(_self_instance):
            """
            This function returns a lambda function that reads the specified channel.
            the read_function is added to the signal as a read_function.
            The _self_instance will later be resolved to the parent of the instance of the signal.

            Parameters:
            _self_instance (object): The parent instance.

            Returns:
            function: A lambda function that reads the power channel.

            """
            return lambda: _self_instance.parent.read_epics_pv(
                short_name=short_name, full_name=full_name
            )

        return read_function

    def set_function_generator(short_name, full_name):
        def set_function(_self_instance, value):
            """
            This function returns a lambda function that sets the opc ua variable.
            The _self_instance will later be resolved to the parent of the instance of the


            Parameters:
            _self_instance (object): The parent instance.
            value (float): The value to set the channel to.

            Returns:
            function: A lambda function that sets the power channel.

            """
            # It is important to pass the value to the lambda function!
            return lambda: _self_instance.parent.set_epics_pv(
                short_name=short_name, full_name=full_name, value=value
            )

        return set_function

    signal_dictionary = {}
    pvs_dict_list = [dict(zip(pvs.keys(), values)) for values in zip(*pvs.values())]
    for pv_dict in pvs_dict_list:
        # For each channel add read_power function
        if pv_dict["PV-Type"] == "read-only":
            signal_dictionary[pv_dict["PV Short Name"]] = Cpt(
                Custom_Function_SignalRO,
                name=pv_dict["PV Short Name"],
                metadata={"units": "", "description": ""},
                read_function=read_function_generator(
                    short_name=pv_dict["PV Short Name"],
                    full_name=pv_dict["PV Full Name"],
                ),
            )
        elif pv_dict["PV-Type"] == "set":
            signal_dictionary[pv_dict["PV Short Name"]] = Cpt(
                Custom_Function_Signal,
                name=pv_dict["PV Short Name"],
                metadata={"units": "", "description": ""},
                put_function=set_function_generator(
                    short_name=pv_dict["PV Short Name"],
                    full_name=pv_dict["PV Full Name"],
                ),
                read_function=read_function_generator(
                    short_name=pv_dict["PV Short Name"],
                    full_name=pv_dict["PV Full Name"],
                ),
            )

    return type(
        f"EPICS_PV_total_channels_{len(pvs_dict_list)}",
        (Epics_Instrument,),
        {**signal_dictionary},
    )


class Epics_Instrument(Device):
    def __init__(
        self,
        prefix="",
        *,
        name,
        kind=None,
        read_attrs=None,
        configuration_attrs=None,
        parent=None,
        pvs=None,
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
        self.pvs = pvs

    def read_epics_pv(self, short_name, full_name):
        """
        This function reads the specified channel.

        Parameters:
        short_name (str): The short name of the channel.
        full_name (str): The full name of the channel.

        Returns:
        float: The value of the channel.

        """
        pv = PV(full_name)
        return pv.get()

    def set_epics_pv(self, short_name, full_name, value):
        """
        This function sets the specified channel.
        """
        pv = PV(full_name)
        pv.put(value)
        return pv.get()
