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

from nomad_camels_driver_keithley_6221.keithley_6221_ophyd import Keithley_6221
from nomad_camels.main_classes import device_class

class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name='keithley_6221',
            virtual=False,
            tags=['current',
            'source'],
            directory='keithley_6221',
            ophyd_device=Keithley_6221,
            ophyd_class_name='Keithley_6221',
            **kwargs)
        self.config['phase_marker_trigger_line'] = '3'
        self.config['enable_phase_marker'] = False
        self.config['set_phase_marker_phase'] = 0

class subclass_config(device_class.Simple_Config):
    def __init__(self,
        parent=None,
        data='',
        settings_dict=None,
        config_dict=None,
        ioc_dict=None,
        additional_info=None):
        comboBoxes = {'phase_marker_trigger_line': ['1', '2', '3', '4', '5', '6']}
        super().__init__(parent,
            'Keithley 6221',
            data,
            settings_dict,
            config_dict,
            additional_info,
            comboBoxes=comboBoxes)
        self.comboBox_connection_type.addItem('Local VISA')
        self.load_settings()
