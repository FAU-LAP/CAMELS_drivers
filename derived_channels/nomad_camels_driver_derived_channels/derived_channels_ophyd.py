from ophyd import Component as Cpt
from ophyd import Device
from .multi_derived_signal import MultiDerivedSignal, MultiDerivedSignalRO


def make_ophyd_instance_derived_channels(
    prefix="",
    *args,
    name,
    kind=None,
    read_attrs=None,
    configuration_attrs=None,
    parent=None,
    signal_info=None,
    # These are the arguments you want to pass to the ophyd class
    # These are the settings you defined in the .py file
    # We will pass the number of channels we selected in the drop down and are defined in the .py file
    **kwargs,
):
    ophyd_class = make_ophyd_class(signal_info or {})
    return ophyd_class(
        prefix,
        *args,
        name=name,
        kind=kind,
        read_attrs=read_attrs,
        configuration_attrs=configuration_attrs,
        parent=parent,
        **kwargs,
    )


def make_ophyd_class(signal_info):
    signal_dict = {}
    for key, value in signal_info.items():
        write_access = value.get("write_access", False)
        if write_access:
            signal_dict[key] = Cpt(
                MultiDerivedSignal,
                name=key,
                derived_from=value.get("derived_from", []),
                write_access=value.get("write_access", False),
                read_formula=value.get("read_formula"),
                write_formula=value.get("write_formula"),
                metadata={
                    "description": value.get("description", ""),
                    "unit": value.get("unit", ""),
                },
            )
        else:
            signal_dict[key] = Cpt(
                MultiDerivedSignalRO,
                name=key,
                derived_from=value.get("derived_from", []),
                read_formula=value.get("read_formula"),
                metadata={
                    "description": value.get("description", ""),
                    "unit": value.get("unit", ""),
                },
            )
    return type("Derived_Channels_Ophyd", (derived_channels,), {**signal_dict})


class derived_channels(Device):
    """
    This class is used to control the LabVIEW Cryo system.
    It reads the file coming from the LabVIEW code.
    """

    def __init__(
        self,
        prefix="",
        *,
        name,
        kind=None,
        read_attrs=None,
        configuration_attrs=None,
        parent=None,
        signal_info=None,  # this is needed, otherwise there will be an unknown kwarg
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
