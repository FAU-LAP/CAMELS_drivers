from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.visa_signal import VISA_Device, VISA_Signal_RO

from nomad_camels.bluesky_handling.custom_function_signal import Custom_Function_Signal


class Agilent_34970(VISA_Device):
    idn = Cpt(VISA_Signal_RO, query="*IDN?", name="idn", kind="config")
    scanlist = Cpt(
        Custom_Function_Signal,
        name="scanlist",
        metadata={
            "description": "list of channels to scan, as string of comma separated numbers"
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
