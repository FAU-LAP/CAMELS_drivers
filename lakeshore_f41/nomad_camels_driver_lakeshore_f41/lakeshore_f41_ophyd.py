# Copyright 2024 Rouven Craemer, Simon Sochiera
#
# This file is part of NOMAD-CAMELS driver for the Lakeshore teslameter F41
# 
# NOMAD-CAMELS driver for the Lakeshore teslameter F41 is free software: you can
# redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, version 2.1 of
# the License, or any later version.

# NOMAD-CAMELS driver for the Lakeshore teslameter F41 is distributed in the
# hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with NOMAD-CAMELS driver for the Lakeshore teslameter F41. If not, see
# <https://www.gnu.org/licenses/>.
from lakeshore import Teslameter
from ophyd import Component as Cpt
from ophyd import Device
from nomad_camels.bluesky_handling.visa_signal import (VISA_Signal,
    VISA_Signal_RO, VISA_Device)
from nomad_camels.bluesky_handling.custom_function_signal import \
    Custom_Function_Signal, Custom_Function_SignalRO


class Lakeshore_F41(Device):
    set_field = Cpt(Custom_Function_Signal, name='set_field',
                    metadata={'units': 'T'})
    get_field = Cpt(Custom_Function_SignalRO, name='get_field',
                    metadata={'units': 'T'})
    set_P = Cpt(Custom_Function_Signal, name='set_P', kind='config')
    set_I = Cpt(Custom_Function_Signal, name='set_I', kind='config')
    set_D = Cpt(Custom_Function_Signal, name='set_D', kind='config',
                    metadata={'units': 'mT/s'})

    def __init__(
        self,
        prefix='',
        *,
        name,
        kind=None,
        read_attrs=None,
        configuration_attrs=None,
        parent=None,
        **kwargs):
        super().__init__(
            prefix=prefix,
            name=name,
            kind=kind,
            read_attrs=read_attrs,
            configuration_attrs=configuration_attrs,
            parent=parent,
            **kwargs)


        if not self.name == 'test':
            self.tm = Teslameter()

            self.tm.configure_field_control_output_mode(mode='CLLOOP',
                output_enabled=True)

        self.set_field.put_function = self.set_function
        self.get_field.read_function = self.get_function
        self.set_P.put_function = self.set_P_function
        self.set_I.put_function = self.set_I_function
        self.set_D.put_function = self.set_D_function

    def set_function(self, B):
        self.tm.set_field_control_setpoint(B)
    
    def get_function(self):
        return self.tm.get_dc_field()
    
    def set_P_function(self, args):
        self.tm.configure_field_control_pid(gain = float(args))
    
    def set_I_function(self, args):
        self.tm.configure_field_control_pid(integral = float(args))
        
    def set_D_function(self, args):
        self.tm.configure_field_control_pid(ramp_rate = float(args))
    
    def finalize_steps(self):
        self.tm.disconnect_usb()
