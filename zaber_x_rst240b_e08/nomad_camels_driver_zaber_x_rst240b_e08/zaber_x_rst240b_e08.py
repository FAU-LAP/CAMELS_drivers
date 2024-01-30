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
from .zaber_x_rst240b_e08_ophyd import Zaber_X_RST240B_E08
from nomad_camels.main_classes import device_class

class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name='Zaber_X_RST240B_E08',
            virtual=False,
            tags=['rotation_stage'],
            ophyd_device=Zaber_X_RST240B_E08,
            ophyd_class_name='Zaber_X_RST240B_E08', 
            **kwargs)

        self.config['set_speed'] = 15

class subclass_config(device_class.Simple_Config):
    def __init__(self, parent=None, data='', settings_dict=None,
                 config_dict=None, additional_info=None):

        super().__init__(
            parent,
            'Zaber_X_RST240B_E08',
            data,
            settings_dict,
            config_dict,
            additional_info)

        self.load_settings()
