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

from nomad_camels_driver_thorlabs_ddr_25.thorlabs_ddr_25_ophyd import \
    Thorlabs_DDR_25
from nomad_camels.main_classes import device_class

class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(name='thorlabs_ddr_25', virtual=False,
                         tags=['Rotation Stage'],
                         ophyd_device=Thorlabs_DDR_25,
                         ophyd_class_name='Thorlabs_DDR_25', **kwargs)
        self.config['set_speed'] = 360 # deg / s

class subclass_config(device_class.Simple_Config):
    def __init__(self, parent=None, data='', settings_dict=None,
                 config_dict=None, additional_info=None):
        super().__init__(parent, 'Thorlabs DDR 25', data, settings_dict,
                         config_dict, additional_info)
        self.load_settings()
