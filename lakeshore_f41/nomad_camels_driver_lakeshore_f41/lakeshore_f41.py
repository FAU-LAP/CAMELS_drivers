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
from .lakeshore_f41_ophyd import Lakeshore_F41
from nomad_camels.main_classes import device_class


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name='lakeshore_F41',
            virtual=False,
            tags=['Teslameter'],
            ophyd_device=Lakeshore_F41,
            ophyd_class_name='Lakeshore_F41',
            **kwargs)

        self.config['set_P'] =  '22'
        self.config['set_I'] =  '0.15'
        self.config['set_D'] =  '0'

class subclass_config(device_class.Simple_Config):
    def __init__(self, parent=None, data='', settings_dict=None,
                 config_dict=None, additional_info=None):
        super().__init__(
            parent,
            'Lakeshore teslameter F41',
            data,
            settings_dict,
            config_dict,
            additional_info)

        self.load_settings()
