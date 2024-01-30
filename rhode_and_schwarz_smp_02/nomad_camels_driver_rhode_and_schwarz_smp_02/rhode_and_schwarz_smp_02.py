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
from .rhode_and_schwarz_smp_02_ophyd import Rhode_and_Schwarz_SMP_02
from nomad_camels.main_classes import device_class


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name='Rhode_and_Schwarz_SMP_02',
            virtual=False,
            tags=['microwave_generator'],
            ophyd_device=Rhode_and_Schwarz_SMP_02,
            ophyd_class_name='Rhode_and_Schwarz_SMP_02',
            non_channel_functions = [
                'output_on',
                'output_off',
                'ac_coupling',
                'dc_coupling',
                'impedance_100kOhm'
            ],
            **kwargs)

class subclass_config(device_class.Simple_Config):
    def __init__(self, parent=None, data='', settings_dict=None,
                 config_dict=None, additional_info=None):
        super().__init__(
            parent,
            'Rhode_and_Schwarz_SMP_02',
            data,
            settings_dict,
            config_dict,
            additional_info) 

        self.comboBox_connection_type.addItem('Local VISA')
        self.load_settings()
