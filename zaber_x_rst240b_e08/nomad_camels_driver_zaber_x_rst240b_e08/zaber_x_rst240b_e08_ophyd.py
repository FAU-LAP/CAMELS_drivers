# Copyright 2024 Rouven Craemer, Simon Sochiera
#
# This file is part of NOMAD-CAMELS driver for the Zaber rotation stage
# RST240B E08
# 
# NOMAD-CAMELS driver for the Zaber rotation stage RST240B E08 is
# free software: you can redistribute it and/or modify it under the terms of the
# GNU Lesser General Public License as published by the Free Software
# Foundation, version 2.1 of the License, or any later version.

# NOMAD-CAMELS driver for the Zaber rotation stage RST240B E08 is distributed in
# the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with NOMAD-CAMELS driver for the Zaber rotation stage RST240B E08. If not, see
# <https://www.gnu.org/licenses/>.
from ophyd import Component as Cpt
from ophyd import Device
from nomad_camels.bluesky_handling.custom_function_signal import Custom_Function_Signal, Custom_Function_SignalRO
from zaber_motion import Units
from zaber_motion.ascii import Connection


class Zaber_X_RST240B_E08(Device):
    set_speed = Cpt(Custom_Function_Signal, name='set_speed', kind='config',
                    metadata={'units': 'deg/s'})
    get_position = Cpt(Custom_Function_SignalRO, name='get_position',
                metadata={'units': 'deg'})    
    rotation_by = Cpt(Custom_Function_Signal, name='rotation_by',
                metadata={'units': 'deg'})    
    rotate_to = Cpt(Custom_Function_Signal, name='rotate_to',
                metadata={'units': 'deg'})
    
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
        self.set_speed.put_function = self.set_speed_function
        self.get_position.read_function = self.get_postion_function
        self.rotation_by.put_function = self.rotation_by_funtion
        self.rotate_to.put_function = self.rotate_to_function
        
        if not self.name=='test':
            self.connect()
        
    def connect(self):
        self.conn = Connection.open_serial_port("COM5")
        self.device_list = self.conn.detect_devices()
        self.dev = self.device_list[0]
        self.axis = self.dev.get_axis(1)
        self.speed_val = 5

    def set_speed_function(self, speed):
        self.speed_val = speed

    def get_postion_function(self):
        return self.axis.get_position(unit=Units.ANGLE_DEGREES)

    def rotation_by_funtion(self, angle):
        self.axis.move_relative(angle,
                Units.ANGLE_DEGREES,
                velocity=self.speed_val,
                velocity_unit=Units.ANGULAR_VELOCITY_DEGREES_PER_SECOND)

    def rotate_to_function(self, angle):
        self.axis.move_absolute(angle,
                Units.ANGLE_DEGREES,
                velocity=self.speed_val,
                velocity_unit=Units.ANGULAR_VELOCITY_DEGREES_PER_SECOND)
                
    def finalize_steps(self):
        self.conn.close()
