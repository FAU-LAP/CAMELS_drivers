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


class Standford_Research_Gs_384(VISA_Device):
    read_frequency = Cpt(
        VISA_Signal_RO,
        name="read_frequency",
        query="FREQ?",
        parse_return_type="float",
        metadata={"units": "", "description": ""},
    )
    read_amplitude_n_type = Cpt(
        VISA_Signal_RO,
        name="read_amplitude_n_type",
        query="AMPR?",
        parse_return_type="float",
        metadata={"units": "", "description": ""},
    )
    set_frequency = Cpt(
        VISA_Signal,
        name="set_frequency",
        write="FREQ {value}",
        parse_return_type=None,
        metadata={"units": "", "description": "set frequency in Hz"},
    )
    set_amplitude_n_type = Cpt(
        VISA_Signal,
        name="set_amplitude_n_type",
        write="AMPR {value}",
        parse_return_type=None,
        metadata={"units": "", "description": "set amplitude in dB"},
    )
    enable_output_n_type = Cpt(
        VISA_Signal,
        name="enable_output_n_type",
        write="ENBR {value}",
        parse_return_type=None,
        metadata={
            "units": "",
            "description": "enable with value =1, or disable with value = 0",
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
        resource_name="",
        write_termination="\r\n",
        read_termination="\r\n",
        baud_rate=9600,
        **kwargs
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
            **kwargs
        )
