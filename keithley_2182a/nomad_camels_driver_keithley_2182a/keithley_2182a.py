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

from nomad_camels_driver_keithley_2182a.keithley_2182a_ophyd import Keithley_2182A
from nomad_camels.main_classes import device_class

class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(name='keithley_2182a',
            virtual=False,
            tags=['nanovoltmeter'],
            directory='keithley_2182a',
            ophyd_device=Keithley_2182A,
            ophyd_class_name='Keithley_2182A',
            non_channel_functions=[
                'init_delta_mode',
                'disable_cacluation'
            ],
            **kwargs)

class subclass_config(device_class.Simple_Config):
    def __init__(self, parent=None, data='', settings_dict=None,
                 config_dict=None, ioc_dict=None, additional_info=None):
        super().__init__(parent, 'Keithley 2182a', data, settings_dict,
                         config_dict, additional_info)
        self.comboBox_connection_type.addItem('Local VISA')
        self.load_settings()
