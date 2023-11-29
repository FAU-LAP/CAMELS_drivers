# Copyright 2023 Simon Sochiera
#
# This file is part of NOMAD-CAMELS driver for Keithley current source 6221.
# 
# NOMAD-CAMELS driver for Keithley current source 6221 is free software: you
# can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, version 2.1 of
# the License, or any later version.

# NOMAD-CAMELS driver for Keithley current source 6221 is distributed in the
# hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with NOMAD-CAMELS driver for Keithley current source 6221. If not, see
# <https://www.gnu.org/licenses/>.

from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.visa_signal import VISA_Signal, \
    VISA_Signal_RO, VISA_Device
from nomad_camels.bluesky_handling.custom_function_signal import \
    Custom_Function_Signal

# ------------------------------------------------------------------------------
# Allowed Values
# ------------------------------------------------------------------------------
ALLOWED_CURRENT_MARGINS = [-105e-3, 105e-3]
ALLOWED_WAVE_TYPE = ['SIN', 'SQU', 'RAMP', 'ARB0', 'ARB1', 'ARB2', 'ARB3',
    'ARB4']
ALLOWED_PMAR_LINES = list(range(1, 7))
ALLOWED_WAVE_AMPLITUDE_MARGINS = [2e-12, 105e-3]
ALLOWED_WAVE_FREQUENCY_MARGINS = [1e-3, 1e5]
ALLOWED_WAVE_DUTY_CYCLE_MARGINS = [0, 100]
ALLOWED_WAVE_OFFSET = ALLOWED_CURRENT_MARGINS

is_in_allowed_margins = lambda value, margins: margins[0] <= value <= margins[1]
is_allowed_current = lambda current: is_in_allowed_margins(current,
        ALLOWED_CURRENT_MARGINS)
is_allowed_wave_amplitude = lambda amplitude: is_in_allowed_margins(amplitude,
        ALLOWED_WAVE_AMPLITUDE_MARGINS)
is_allowed_wave_frequency = lambda frequency: is_in_allowed_margins(frequency,
        ALLOWED_WAVE_FREQUENCY_MARGINS)
is_allowed_wave_duty_cycle = lambda duty_cycle: is_in_allowed_margins(duty_cycle,
        ALLOWED_WAVE_DUTY_CYCLE_MARGINS)
is_allowed_wave_offset = lambda offset: is_in_allowed_margins(offset,
        ALLOWED_WAVE_OFFSET)
# ------------------------------------------------------------------------------

def convert_to_bool(state):
    if type(state) == type("") and state in ['True', 'False']:
        exec(f"state = {state}")
    return bool(state)

class Keithley_6221(VISA_Device):
    get_ID = Cpt(VISA_Signal_RO, name='get_ID', query='*IDN?', metadata={'ID':
        'string'})
    set_constant_current = Cpt(VISA_Signal, name='set_constant_current',
            metadata={'units': 'A'})
    enable_output = Cpt(VISA_Signal, name='enable_output')
    reset = Cpt(VISA_Signal, write="*RST", name='reset')
    phase_marker_trigger_line = Cpt(VISA_Signal,
            name='phase_marker_trigger_line', kind='config')
    enable_phase_marker = Cpt(VISA_Signal,
            name='enable_phase_marker', kind='config')
    set_phase_marker_phase = Cpt(VISA_Signal, name='set_phase_marker_phase',
            kind='config')
    set_wave_type = Cpt(VISA_Signal, name='set_wave_type')
    set_wave_amplitude = Cpt(VISA_Signal, name='set_wave_amplitude')
    set_wave_frequency = Cpt(VISA_Signal, name='set_wave_frequency')
    set_wave_duty_cycle = Cpt(VISA_Signal, name='set_wave_duty_cycle')
    set_wave_offset = Cpt(VISA_Signal, name='set_wave_offset')
    enable_wave = Cpt(VISA_Signal, name='enable_wave')
    clear = Cpt(VISA_Signal, name='clear', write='SOUR:CLE:IMM')

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

        self.set_constant_current.write = self.set_constant_current_function
        self.enable_output.write = self.enable_output_function
        self.phase_marker_trigger_line.write =\
            self.phase_marker_trigger_line_function
        self.enable_phase_marker.write = self.enable_phase_marker_function
        self.set_phase_marker_phase.write = self.set_phase_marker_phase_function
        self.set_wave_type.write = self.set_wave_type_function
        self.set_wave_amplitude.write = self.set_wave_amplitude_function
        self.set_wave_frequency.write = self.set_wave_frequency_function
        self.set_wave_duty_cycle.write = self.set_wave_duty_cycle_function
        self.set_wave_offset.write = self.set_wave_offset_function
        self.enable_wave.write = self.enable_wave_function

    def set_constant_current_function(self, current):
        if is_allowed_current(current):
            self.visa_instrument.write(f'SOUR:CURR:RANG:AUTO ON')
            self.visa_instrument.write(f'SOUR:CURR:AMPL {current}')
            self.visa_instrument.write(f'OUTP ON')
        else:
            print("Keithley 6221 current source: current {current} A not in "+\
                    f"allowed margins ({ALLOWED_CURRENT_MARGINS[0]} A to "+\
                    f"{ALLOWED_CURRENT_MARGINS[1]}) A", flush=1)
        return ''

    def enable_output_function(self, state):
        state = convert_to_bool(state)
        self.visa_instrument.write(f'OUTP {"ON" if state else "OFF"}')
        return ''

    def phase_marker_trigger_line_function(self, line):
        line = int(line)
        if line in ALLOWED_PMAR_LINES:
            self.visa_instrument.write(f"SOUR:WAVE:PMAR:OLIN {line}")
        else:
            print("Keithley 6221 current source: available lines for phase "+\
                f"marker: {ALLOWED_PMAR_LINES}; not {line}")
        return ''

    def enable_phase_marker_function(self, state):
        state = convert_to_bool(state)
        self.visa_instrument.write('SOUR:WAVE:PMAR:STAT '+\
            f'{"ON" if state else "OFF"}')
        return ''

    def set_phase_marker_phase_function(self, phase):
        phase = phase - 360 * (phase//360)
        self.visa_instrument.write(f'SOUR:WAVE:PMAR:LEV {phase}')
        return ''
        
    def set_wave_type_function(self, wave_type):
        wave_type = wave_type.strip().upper()
        if wave_type in ALLOWED_WAVE_TYPE:
            self.visa_instrument.write(f'SOUR:WAVE:FUNC {wave_type}')
        else:
            print(f"Keithley 6221 current source: wave type \"{wave_type}\""+\
                    f"not allowed; allowed wave types: {ALLOWED_WAVE_TYPE}",
                    flush=1)
        return ''

    def set_wave_amplitude_function(self, amplitude):
        if is_allowed_wave_amplitude(amplitude):
            self.visa_instrument.write(f'SOUR:WAVE:AMPL {amplitude}')
        else:
            print(f"Keithley 6221 current source: amplitude {amplitude} Ap2p"+\
                    f"not allowed; allowed amplitudes: "+\
                    f"{ALLOWED_CURRENT_MARGINS[0]} Ap2p to "+\
                    f"{ALLOWED_WAVE_AMPLITUDE_MARGINS[1]} Ap2p",
                    flush=1)
        return ''

    def set_wave_frequency_function(self, frequency):
        if is_allowed_wave_frequency(frequency):
            self.visa_instrument.write(f'SOUR:WAVE:FREQ {frequency}')
        else:
            print(f"Keithley 6221 current source: frequency {frequency} Hz"+\
                    f"not allowed; allowed frequencies: "+\
                    f"{ALLOWED_WAVE_FREQUENCY_MARGINS[0]} Hz to "+\
                    f"{ALLOWED_WAVE_FREQUENCY_MARGINS[1]} Hz",
                    flush=1)
        return ''

    def set_wave_duty_cycle_function(self, duty_cycle):
        if is_allowed_wave_duty_cycle(duty_cycle):
            self.visa_instrument.write(f'SOUR:WAVE:DCYC {int(duty_cycle)}')
        else:
            print(f"Keithley 6221 current source: duty cycle \"{duty_cycle}\""+\
                    f"not allowed; allowed duty cycles: "+\
                    f"{ALLOWED_WAVE_DUTY_CYCLE_MARGINS[0]} to "+\
                    f"{ALLOWED_WAVE_DUTY_CYCLE_MARGINS[1]}",
                    flush=1)
        return ''

    def set_wave_offset_function(self, offset):
        if is_allowed_wave_offset(offset):
            self.visa_instrument.write(f'SOUR:WAVE:OFFS {offset}')
        else:
            print(f"Keithley 6221 current source: wave offset {offset} A"+\
                    f"not allowed; allowed wave offsets: "+\
                    f"{ALLOWED_WAVE_OFFSET[0]} A to {ALLOWED_WAVE_OFFSET} A",
                    flush=1)
        return ''

    def enable_wave_function(self, state):
        state = convert_to_bool(state)
        if state:
            self.visa_instrument.write('SOUR:WAVE:ARM')
            self.visa_instrument.write('SOUR:WAVE:INIT')
        else:
            self.visa_instrument.write('SOUR:WAVE:ABOR')
        return ''
