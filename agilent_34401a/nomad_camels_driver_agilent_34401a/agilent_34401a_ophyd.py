from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.visa_signal import VISA_Signal, VISA_Signal_RO, \
    VISA_Device



class Agilent_34401(VISA_Device):
    measure_voltage_DC = Cpt(VISA_Signal_RO,
                             name='measure_voltage_DC', query="MEAS:VOLT:DC?",
                             metadata={'units': 'V', 'description': 'Measures DC voltage.'})
    measure_current_DC = Cpt(VISA_Signal_RO,
                             name='measure_current_DC', query="MEAS:CURR:DC?",
                             metadata={'units': 'A', 'description': 'Measures DC current.'})
    measure_voltage_AC = Cpt(VISA_Signal_RO,
                             name='measure_voltage_AC', query="MEAS:VOLT:AC?",
                             metadata={'units': 'V', 'description':'Measures AC voltage.'})
    measure_current_AC = Cpt(VISA_Signal_RO,
                             name='measure_current_AC', query="MEAS:CURR:AC?",
                             metadata={'units': 'A', 'description':'Measures AC current.'})
    measure_resistance = Cpt(VISA_Signal_RO,
                             name='measure_resistance', query="MEAS:RES?",
                             metadata={'units': 'Ohm', 'description':'Measures DC resistance.'})
    measure_resistance_4wire = Cpt(VISA_Signal_RO,
                                   name='measure_resistance_4wire', query="MEAS:FRES?",
                                   metadata={'units': 'Ohm', 'description':'Measures four wire DC resistance.'})
    device_ID = Cpt(VISA_Signal_RO,
                    name='device_ID', kind='config', query='*IDN?',
                    metadata={'description':'Device ID.'})
    nPLC = Cpt(VISA_Signal,
               name='nPLC', kind='config',
               write='VOLT:DC:NPLC {value};CURR:DC:NPLC {value};RES:NPLC {value};FRES:NPLC {value}',
               metadata={'description':''})

    def __init__(self, prefix='', *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None, resource_name='',
                 read_termination='\r\n', write_termination='\r\n',
                 baud_rate=9600, **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs,
                         configuration_attrs=configuration_attrs, parent=parent,
                         resource_name=resource_name, baud_rate=baud_rate,
                         write_termination=write_termination,
                         read_termination=read_termination, **kwargs)
