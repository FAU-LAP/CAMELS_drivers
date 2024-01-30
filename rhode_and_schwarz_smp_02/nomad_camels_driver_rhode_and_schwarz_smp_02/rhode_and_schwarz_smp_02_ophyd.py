# Copyright 2024 Rouven Craemer, Simon Sochiera
#
# This file is part of NOMAD-CAMELS driver for the Rhode and Schwarz microwave
# amplifier SMP 02
# 
# NOMAD-CAMELS driver for the Rhode and Schwarz microwave amplifier SMP 02 is
# free software: you can redistribute it and/or modify it under the terms of the
# GNU Lesser General Public License as published by the Free Software
# Foundation, version 2.1 of the License, or any later version.

# NOMAD-CAMELS driver for the Rhode and Schwarz microwave amplifier SMP 02 is
# distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with NOMAD-CAMELS driver for the Rhode and Schwarz microwave amplifier SMP 02.
# If not, see <https://www.gnu.org/licenses/>.
from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.visa_signal import (VISA_Signal,
    VISA_Signal_RO, VISA_Device)
from nomad_camels.bluesky_handling.custom_function_signal import\
    Custom_Function_Signal


class Rhode_and_Schwarz_SMP_02(VISA_Device):
    set_Frequency = Cpt(VISA_Signal, name='set_Frequency',
                    metadata={'units': 'GHz'})
    set_Powerlevel = Cpt(VISA_Signal, name='set_Powerlevel',
                    metadata={'units': 'dBm'})
    
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

        self.set_Frequency.write = self.set_Frequency_function
        self.set_Powerlevel.write = self.set_Powerlevel_function

    def set_Frequency_function(self, freq):
        self.visa_instrument.write(f"SOUR:FREQ {freq}GHz")
        return ""
        
    def set_Powerlevel_function(self, power_level):
        self.visa_instrument.write(f"SOUR:POW {power_level}dBm")
        return ""

    def output_on(self):
        self.visa_instrument.write("OUTP:STAT ON")

    def output_off(self):
        self.visa_instrument.write("OUTP:STAT OFF")
    
    def ac_coupling(self):
        self.visa_instrument.write("SOUR:AM:EXT:COUP AC")
        
    def dc_coupling(self):
        self.visa_instrument.write("SOUR:AM:EXT:COUP DC")
        
    def impedance_100kOhm(self):
        self.visa_instrument.write("SOUR:AM:EXT:IMP 100kOhm")
