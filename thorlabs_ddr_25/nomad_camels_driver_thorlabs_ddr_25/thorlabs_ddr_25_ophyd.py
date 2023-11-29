# Copyright 2023 Simon Sochiera
#
# This file is part of NOMAD-CAMELS driver for Thorlabs rotation stage DDR 25.
# 
# NOMAD-CAMELS driver for Thorlabs rotation stage DDR 25 is free software: you
# can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version
# 2.1 of the License, or any later version.

# NOMAD-CAMELS driver for Thorlabs rotation stage DDR 25 is distributed in the
# hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with NOMAD-CAMELS driver for Thorlabs rotation stage DDR 25. If not, see
# <https://www.gnu.org/licenses/>.

from ophyd import Component as Cpt
from ophyd import Device
from nomad_camels.bluesky_handling.custom_function_signal import \
    Custom_Function_Signal, Custom_Function_SignalRO
from pylablib.devices import Thorlabs


class Thorlabs_DDR_25(Device):
    get_position = Cpt(Custom_Function_SignalRO, name='get_position',
            metadata={'units':'deg'})
    set_relative_position = Cpt(Custom_Function_Signal,
            name='set_relative_position', metadata={'units':'deg'})
    set_absolute_position = Cpt(Custom_Function_Signal,
            name='set_absolute_position', metadata={'units':'deg'})
    set_speed = Cpt(Custom_Function_Signal,
            name='set_speed', kind='config', metadata={'units':'deg / s'})
    wait_move = Cpt(Custom_Function_SignalRO, name='wait_move')
    is_connected = Cpt(Custom_Function_SignalRO, name='is_connected')
    is_enabled = Cpt(Custom_Function_SignalRO, name='is_enabled')

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
            self.connect_function()

        self.get_position.read_function = self.get_position_function
        self.set_relative_position.put_function = self.move_by_function
        self.set_absolute_position.put_function = self.move_to_function
        self.set_speed.put_function = self.set_speed_function
        self.is_connected.read_function = self.is_connected_function
        self.is_enabled.read_function = self.is_enabled_function
        self.wait_move.read_function = self.wait_move_function

    def connect_function(self, retry=1):
        rs_con = Thorlabs.list_kinesis_devices()
        if len(rs_con) > 0:
            self.rotation_stage = Thorlabs.KinesisMotor(rs_con[0][0],
                scale="DDR25")
            if self.rotation_stage.get_status() == []:
                print("rotation stage disabled; manually enable it")
        else:
            print("cannot find rotation stage DDR 25; check connection")

    def set_speed_function(self, speed):
        if not self.is_connected_function():
            print("rotation stage DDR 25 not connected; cannot set speed")
        elif not speed == 0:
            self.rotation_stage.setup_velocity(max_velocity=speed)
        elif speed == 0:
            print("setting speed of rotation stage DDR25 to zero makes no sense")

    def move_by_function(self, ang):
        if not self.is_connected_function():
            print("rotation stage DDR 25 not connected; cannot set speed")
        elif not self.is_enabled_function():
            print("rotation stage disabled; manually enable it")
        else:
            self.rotation_stage.move_by(ang)

    def move_to_function(self, ang):
        if not self.is_connected_function():
            print("rotation stage DDR 25 not connected; cannot set speed")
        elif not self.is_enabled_function():
            print("rotation stage disabled; manually enable it")
        else:
            self.rotation_stage.move_to(ang)

    def get_position_function(self):
        if not self.is_connected_function():
            print("rotation stage DDR 25 not connected; cannot get position")
            return 0
        else:
            return self.rotation_stage.get_position()

    def wait_move_function(self):
        if self.is_connected_function():
            self.rotation_stage.wait_move()
        else:
            print("rotation stage DDR 25 not connected; cannot wait move")
        return 0

    def is_connected_function(self):
        return hasattr(self, 'rotation_stage')

    def is_enabled_function(self):
        return False if not self.is_connected_function() else not \
            self.rotation_stage.get_status() == []

    def finalize_steps(self):
        # disconnect rotation stage after use so it can be connected without
        # an error next time
        if self.is_connected_function():
            self.rotation_stage.close()
