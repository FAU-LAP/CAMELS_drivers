from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.visa_signal import VISA_Signal, VISA_Signal_RO, VISA_Device



class Agilent_E363X(VISA_Device):
    current_limit_1 = Cpt(VISA_Signal, name='current_limit_1', kind='config', write=':INST:NSEL 1;:CURR {value:g}', metadata={'units': 'A', 'description': 'Sets the current limit for channel 1.'})
    current_limit_2 = Cpt(VISA_Signal, name='current_limit_2', kind='config', write=':INST:NSEL 2;:CURR {value:g}', metadata={'units': 'A', 'description': 'Sets the current limit for channel 2.'})
    current_limit_3 = Cpt(VISA_Signal, name='current_limit_3', kind='config', write=':INST:NSEL 3;:CURR {value:g}', metadata={'units': 'A', 'description': 'Sets the current limit for channel 3.'})

    voltage_1 = Cpt(VISA_Signal, name='voltage_1', write=':INST:NSEL 1;:VOLT {value:g}', metadata={'units': 'V', 'description': 'Sets the voltage for channel 1.'})
    voltage_2 = Cpt(VISA_Signal, name='voltage_2', write=':INST:NSEL 2;:VOLT {value:g}', metadata={'units': 'V', 'description': 'Sets the voltage for channel 2.'})
    voltage_3 = Cpt(VISA_Signal, name='voltage_3', write=':INST:NSEL 3;:VOLT {value:g}', metadata={'units': 'V', 'description': 'Sets the voltage for channel 3.'})
    output_1 = Cpt(VISA_Signal, name='output_1', write=':INST:NSEL 1;:OUTP {value:d}', metadata={'description': 'Sets the output for channel 1.'})
    output_2 = Cpt(VISA_Signal, name='output_2', write=':INST:NSEL 2;:OUTP {value:d}', metadata={'description': 'Sets the output for channel 2.'})
    output_3 = Cpt(VISA_Signal, name='output_3', write=':INST:NSEL 3;:OUTP {value:d}', metadata={'description': 'Sets the output for channel 3.'})

    def __init__(self, prefix='', *, name, kind=None, read_attrs=None, configuration_attrs=None, parent=None, resource_name='', read_termination='\r\n', write_termination='\r\n', baud_rate=9600, timeout=2000, retry_on_error=0, **kwargs):
        super().__init__(prefix, name=name, kind=kind, read_attrs=read_attrs, configuration_attrs=configuration_attrs, parent=parent, resource_name=resource_name, read_termination=read_termination, write_termination=write_termination, baud_rate=baud_rate, timeout=timeout, retry_on_error=retry_on_error, **kwargs)