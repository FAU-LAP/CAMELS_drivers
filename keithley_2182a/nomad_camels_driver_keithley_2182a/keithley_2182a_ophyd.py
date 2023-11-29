# Copyright 2023 Simon Sochiera
#
# This file is part of NOMAD-CAMELS driver for Keithley nanovoltmeter 2182a.
# 
# NOMAD-CAMELS driver for Keithley nanovoltmeter 2182a is free software: you
# can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version
# 2.1 of the License, or any later version.

# NOMAD-CAMELS driver for Keithley nanovoltmeter 2182a is distributed in the
# hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with NOMAD-CAMELS driver for Keithley nanovoltmeter 2182a. If not, see
# <https://www.gnu.org/licenses/>.

from ophyd import Component as Cpt
from nomad_camels.bluesky_handling.visa_signal import VISA_Signal, \
    VISA_Signal_RO, VISA_Device
from nomad_camels.bluesky_handling.custom_function_signal import \
    Custom_Function_Signal

# ------------------------------------------------------------------------------
# Allowed Values
# ------------------------------------------------------------------------------
ALLOWED_CHANNELS = [1, 2]
ALLOWED_VOLTAGE_INTEGRATION_TIME_MARGINS = [200e-6, 1]
ALLOWED_NPL_CYCLES_MARGINS = [0.01, 60]

# This function checks if a value is in the margins defined by a tuple of values
is_in_allowed_margins = lambda value, margins: margins[0] <= value <= margins[1]
is_allowed_voltage_integration_time = lambda voltage_integration_time:\
    is_in_allowed_margins(voltage_integration_time,
    ALLOWED_VOLTAGE_INTEGRATION_TIME_MARGINS)
is_allowed_npl_cycles = lambda npl_cycles: is_in_allowed_margins(npl_cycles,
        ALLOWED_NPL_CYCLES_MARGINS)
# ------------------------------------------------------------------------------

class Keithley_2182A(VISA_Device):
    get_ID = Cpt(VISA_Signal_RO, name='get_ID', query='*IDN?', metadata={'ID':
        'string'})
    abort = Cpt(VISA_Signal, write=":ABOR", name='abort')
    autorange_channel = Cpt(VISA_Signal, name='autorange')
    select_voltage_measurement = Cpt(VISA_Signal,
        name='select_voltage_measurement')
    select_channel = Cpt(VISA_Signal, name='select_channel')
    measurement = Cpt(VISA_Signal_RO, name='measurement', query=':FETC?')
    set_voltage_integration_time = Cpt(VISA_Signal,
        name='set_voltage_integration_time')
    set_npl_cycles = Cpt(VISA_Signal, name='set_npl_cycles')
    set_to_calculate_resistance = Cpt(VISA_Signal,
        name='set_to_calculate_resistance', metadata={'units': 'A'})

    def __init__(self,
        prefix='',
        *,
        name,
        kind=None,
        read_attrs=None,
        configuration_attrs=None,
        parent=None,
        resource_name='',
        baud_rate=9600,
        write_termination='\r\n',
        read_termination='\r\n',
        **kwargs):
        super().__init__(prefix=prefix,
            name=name,
            kind=kind,
            read_attrs=read_attrs,
            configuration_attrs=configuration_attrs,
            parent=parent,
            resource_name=resource_name,
            baud_rate=baud_rate,
            write_termination=write_termination,
            read_termination=read_termination,
            **kwargs)

        self.autorange_channel.write = self.autorange_channel_function
        self.select_voltage_measurement.write = \
            self.select_voltage_measurement_function
        self.select_channel.write = self.select_channel_function
        self.set_voltage_integration_time.write = \
            self.set_voltage_integration_time_function
        self.set_npl_cycles.write = self.set_npl_cycles_function
        self.set_to_calculate_resistance.write =  \
            self.set_to_calculate_resistance_function

    def set_voltage_integration_time_function(self, integration_time):
        if is_allowed_voltage_integration_time(integration_time):
            self.visa_instrument.write(f':SENS:VOLT:APER {integration_time}')
        else:
            print("Keithley 2182A nanovoltmeter: voltage integration time "+\
                    f"{integration_time} s not allowed; allowed integration "+\
                    f"times: {ALLOWED_VOLTAGE_INTEGRATION_TIME_MARGINS[0]} "+\
                    f"s to {ALLOWED_VOLTAGE_INTEGRATION_TIME_MARGINS[1]} s")
        return ''

    def select_voltage_measurement_function(self, dummy):
        self.visa_instrument.write(':SENS:FUNC \'VOLT\'')
        return ''

    def autorange_channel_function(self, channel):
        if channel in ALLOWED_CHANNELS:
            self.visa_instrument.write(f':SENS:VOLT:CHAN{channel}:RANG:AUTO ON')
        else:
            print("Keithley 2182A nanovoltmeter: autorange channel "+\
                f"{channel} not allowed; allowed channels: "+\
                f"{ALLOWED_NPL_CYCLES_MARGINS[0]} to "+\
                f"{ALLOWED_NPL_CYCLES_MARGINS[1]}")
        return ''

    def select_channel_function(self, channel):
        channel = int(channel)
        if channel in ALLOWED_CHANNELS:
            self.visa_instrument.write(f':SENS:CHAN {channel}')
        else:
            print("Keithley 2182A nanovoltmeter: select channel "+\
                    f"{channel} not allowed; allowed channels: "+\
                    f"{ALLOWED_CHANNELS}")
        return ''

    def set_npl_cycles_function(self, npl_cycles):
        if is_allowed_npl_cycles(npl_cycles):
            self.visa_instrument.write(f':SENS:VOLT:NPLC {npl_cycles}')
        else:
            print("Keithley 2182A nanovoltmeter: NPL cycles"+\
                    f"{npl_cycles} not allowed; allowed values: "+\
                    f"{ALLOWED_NPL_CYCLES_MARGINS[0]} to "+\
                    f"{ALLOWED_NPL_CYCLES_MARGINS[1]}")
        return ''

    def set_to_calculate_resistance_function(self, applied_current):
        self.visa_instrument.write(':CALC:FORM MXB')
        self.visa_instrument.write(':CALC:STAT ON')
        self.visa_instrument.write(f':CALC:KMAT:MMF {1/applied_current}')
        self.visa_instrument.write(':CALC:KMAT:MBF 0')
        self.visa_instrument.write(':CALC:KMAT:MUN \'[[\'')
        return ''

    def disable_calculation(self):
        self.visa_instrument.write(':CALC:STAT OFF')

    def init_delta_mode(self):
        self.visa_instrument.write(':SENS:VOLT:DELT ON')

    def finalize_steps(self):
        pass
