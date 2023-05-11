from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.visa_signal import (VISA_Signal_Write,
                                                       VISA_Signal_Read,
                                                       VISA_Device)



class instrument_name(VISA_Device):

    # This is an example for a standard identification query
    get_ID = Cpt(VISA_Signal_Read, name='V_DC', query_text='*IDN?', metadata={'ID': 'string'})

    def __init__(self, prefix='', *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None, resource_name='',
                 baud_rate=9600, write_termination='\r\n',
                 read_termination='\r\n', **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs,
                         configuration_attrs=configuration_attrs, parent=parent,
                         resource_name=resource_name, baud_rate=baud_rate,
                         write_termination=write_termination,
                         read_termination=read_termination, **kwargs)


if __name__ == '__main__':
    testk = instrument_name(name='test_instrument_name')