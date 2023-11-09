# Copyright 2023 Simon Sochiera
#
# This file is part of NOMAD-CAMELS driver for the Zurich Instruments lock-in
# amplifier MFLI 
# 
# NOMAD-CAMELS driver for the Zurich Instruments lock-in amplifier MFLI is free
# software: you can redistribute it and/or modify it under the terms of the GNU
# Lesser General Public License as published by the Free Software Foundation,
# version 2.1 of the License, or any later version.

# NOMAD-CAMELS driver for the Zurich Instruments lock-in amplifier MFLI is
# distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with NOMAD-CAMELS driver for the Zurich Instruments lock-in amplifier MFLI. If
# not, see <https://www.gnu.org/licenses/>.
from nomad_camels_driver_zurich_instruments_mfli.zurich_instruments_mfli_ophyd \
    import Zurich_Instruments_MFLI, EXTERNAL_REFERENCES
from nomad_camels.main_classes import device_class


"""
For more information see `zurich_instruments_mfli_ophyd.py`.
"""
class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(name='zurich_instruments_mfli', virtual=False,
                         tags=['Lock-In'],
                         ophyd_device=Zurich_Instruments_MFLI,
                         ophyd_class_name='Zurich_Instruments_MFLI', 
                         non_channel_functions=[
                            'adjust_demodulator_phase',
                            'autorange_input',
                         ],
                         **kwargs)
        self.config['connect_to_dev'] = "devXXXX"
        self.config['float_input'] = False
        self.config['imp_50_input'] = False
        self.config['ac_input'] = False
        self.config['diff_input'] = False
        self.config['select_reference'] = 'internal'
        self.config['select_nth_harmonic'] = True
        self.config['set_demodulator_phaseshift'] = False
        self.config['select_1_over_nth_harmonic'] = True
        self.config['filter_order'] = '3'
        self.config['filter_time_constant'] = '0.0008154'
        self.config['sinc'] = False

class subclass_config(device_class.Simple_Config):
    def __init__(self, parent=None, data='', settings_dict=None,
                 config_dict=None, additional_info=None):
        comboBoxes = {
                # 'float_input': ['0', '1'],
                # 'imp_50_input': ['0', '1'],
                # 'ac_input': ['0', '1'],
                # 'diff_input': ['0', '1'],
                'select_reference': ['internal'] + list(EXTERNAL_REFERENCES.keys()),
                'filter_order': [str(i) for i in range(1,9)],
                # 'sinc': ['0', '1'],
                }
        super().__init__(parent, 'Zurich Instruments MFLI', data, settings_dict,
                         config_dict, additional_info, comboBoxes=comboBoxes)
        self.load_settings()
