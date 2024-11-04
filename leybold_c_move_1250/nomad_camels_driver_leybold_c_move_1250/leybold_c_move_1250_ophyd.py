from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.visa_signal import VISA_Device, VISA_Signal_RO

from nomad_camels.bluesky_handling.custom_function_signal import Custom_Function_Signal


class Leybold_C_Move_1250(VISA_Device):
    version = Cpt(VISA_Signal_RO, query="VER?", name="version", kind="config")

    flow_value = Cpt(
        Custom_Function_Signal,
        name="flow_value",
        metadata={"unit": "l/s", "description": "sets the flow value"},
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
        self.flow_value.put_function = self.set_flow_value

    def set_flow_value(self, val):
        if val > 5e-6:
            val_str = f"{val:.2E}"
        else:
            val_str = f"1.00E-06"
        self.visa_instrument.query(f"FLO={val_str}")
