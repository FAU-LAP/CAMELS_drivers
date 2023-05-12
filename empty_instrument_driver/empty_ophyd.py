from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.visa_signal import (VISA_Signal_Write,
                                                       VISA_Signal_Read,
                                                       VISA_Device)
from nomad_camels.bluesky_handling.custom_function_signal import Custom_Function_Signal



class instrument_name(VISA_Device):

    # This is an example for a standard identification query
    get_ID = Cpt(VISA_Signal_Read, name='get_ID', query_text='*IDN?', metadata={'ID': 'string'})

    # Example of complicated set channel
    complicated_set = Cpt(VISA_Signal_Write, name='complicated_set',
                          metadata={'units': 'junk units'})

    # Custom functions do not talk directly to the instrument
    # and can be used to store config settings
    custom_signal_config = Cpt(Custom_Function_Signal, name='custom_signal_config', kind='config')

    def __init__(self, prefix='', *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None, resource_name='',
                 baud_rate=9600, write_termination='\r\n',
                 read_termination='\r\n', **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs,
                         configuration_attrs=configuration_attrs, parent=parent,
                         resource_name=resource_name, baud_rate=baud_rate,
                         write_termination=write_termination,
                         read_termination=read_termination, **kwargs)
        self.complicated_set.put_conv_function = self.complicated_set_function


    def complicated_set_function(self, set_value) -> str:
        # Create a string ehre that is passed to the instrument
        # Function must return a string

        # Here we get the config saved in 'custom_signal_config'
        setting_value = self.custom_signal_config.get()
        created_string = f'set this {set_value} with this setting {setting_value}'
        return created_string


if __name__ == '__main__':
    testk = instrument_name(name='test_instrument_name')
