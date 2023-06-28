from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.visa_signal import VISA_Signal, VISA_Signal_RO, \
    VISA_Device



class Agilent_34401(VISA_Device):
    mesDCV = Cpt(VISA_Signal_RO, name='mesDCV', query="MEAS:VOLT:DC?", metadata={'units': 'V'})
    mesDCI = Cpt(VISA_Signal_RO, name='mesDCI', query="MEAS:CURR:DC?", metadata={'units': 'A'})
    mesACV = Cpt(VISA_Signal_RO, name='mesACV', query="MEAS:VOLT:AC?", metadata={'units': 'V'})
    mesACI = Cpt(VISA_Signal_RO, name='mesACI', query="MEAS:CURR:AC?", metadata={'units': 'A'})
    mesR = Cpt(VISA_Signal_RO, name='mesR', query="MEAS:RES?", metadata={'units': 'Ohm'})
    mesR4w = Cpt(VISA_Signal_RO, name='mesR4w', query="MEAS:FRES?", metadata={'units': 'Ohm'})
    idn = Cpt(VISA_Signal_RO, name='idn', kind='config', query='*IDN?')
    nPLC = Cpt(VISA_Signal, name='nPLC', kind='config')

    def __init__(self, prefix='', *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None, resource_name='',
                 read_termination='\r\n', write_termination='\r\n',
                 baud_rate=9600, **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs,
                         configuration_attrs=configuration_attrs, parent=parent,
                         resource_name=resource_name, baud_rate=baud_rate,
                         write_termination=write_termination,
                         read_termination=read_termination, **kwargs)
