from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.visa_signal import (
    VISA_Signal,
    VISA_Signal_RO,
    VISA_Device,
)
from nomad_camels.bluesky_handling.custom_function_signal import Custom_Function_Signal


class Instrument_Name(VISA_Device):

    # This is an example for a standard identification query
    get_ID = Cpt(
        VISA_Signal_RO, name="get_ID", query="*IDN?", metadata={"ID": "string"}
    )

    # Example of complicated set channel
    complicated_set = Cpt(
        VISA_Signal, name="complicated_set", metadata={"units": "junk units"}
    )

    # Custom functions do not talk directly to the instrument
    # and can be used to store config settings
    custom_signal_config = Cpt(
        Custom_Function_Signal, name="custom_signal_config", kind="config"
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
        baud_rate=9600,
        write_termination="\r\n",
        read_termination="\r\n",
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
            baud_rate=baud_rate,
            write_termination=write_termination,
            read_termination=read_termination,
            **kwargs,
        )
        # Hand the complicated_set_function as the function to produce the
        # write string
        self.complicated_set.write = self.complicated_set_function

    def complicated_set_function(self, set_value) -> str:
        # Create a string here that is passed to the instrument
        # Function must return a string

        # Here we get the config saved in 'custom_signal_config'
        setting_value = self.custom_signal_config.get()
        created_string = f"set this {set_value} with this setting {setting_value}"
        return created_string
