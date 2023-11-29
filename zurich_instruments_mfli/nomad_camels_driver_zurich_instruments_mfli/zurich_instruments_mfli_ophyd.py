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
from ophyd import Component as Cpt
from ophyd import Device
from nomad_camels.bluesky_handling.custom_function_signal import \
    Custom_Function_Signal, Custom_Function_SignalRO
# Python library to connect to Zurich Instrument devices
from zhinst.core import ziDiscovery, ziDAQServer
import numpy as np


# Dictionary that links external reference clear text strings to their value
# given by zurich instruments
EXTERNAL_REFERENCES = {
        'external:Sig In 1': '0',
        'external:Cur In 1': '1',
        'external:Trigger 1': '2',
        'external:Trigger 2': '3',
        'external:Aux Out 1': '4',
        'external:Aux Out 2': '5',
        'external:Aux Out 3': '6',
        'external:Aux Out 4': '7',
        'external:Aux In 1': '8',
        'external:Aux In 2': '9',
        'external:Constant': '174',
        }

def construct_correct_path(dev_name, path):
    """
    This function constructs a string that is accepted by the lock-in's
    functions `setInt`, `getInt`, `setDouble`, ... . It's job is mainly to avoid
    errors that might occur due to a manual entry of a path.

    parameters:

    dev_name    name of the lock-in, i.e. 'devWXYZ', where WXYZ is a 4-digit
                number
    path        path to a lock-ins functionality
    """
    dev_name = dev_name.lower()
    skip = int(path[0] == '/')
    if len(path) > len(dev_name)+skip and \
        path[skip:len(dev_name)+skip].lower() == dev_name:
        # The device name is included in the path
        return '/'+path if skip == 0 else path
    # The device name has to be added to the path
    return '/'+dev_name+('/' if skip == 0 else '')+path


class Zurich_Instruments_MFLI(Device):
    """
    This class communicates with the lock-in amplifier MFLI from Zurich
    Instruments. In it, some of the functionality accessible over the web
    interface is implemented.

    Other functionality, that concerns setting values can also be accessed via
    the `set_double` and `set_int` functions: call the channel `set_double` or
    `set_int` and pass a string of the path to the functionality of the lock-in
    (without the device name) with a ':' and then the value you want to set. The
    string should conform with this format: 'PATH/TO/FUNCTIONALITY:VALUE'. Do
    not forget the inverted commas in CAMELS, otherwise it will be interpreted
    as python code.

    Many parameters that can be set, but do not need to be set via a variable,
    such as the number of the harmonic you want to measure, are included in the
    configuration to give a better overview.
    """
    # --------------------------------------------------------------------------
    # Connecting
    # --------------------------------------------------------------------------
    # Establish the connection to the lock-in
    connect_to_dev = Cpt(Custom_Function_Signal, name='connect_to_dev',
        kind='config')
    # Get whether a connection to a lock-in has been established
    is_connected = Cpt(Custom_Function_SignalRO, name='is_connected')
    # --------------------------------------------------------------------------
    # General Set Function
    # --------------------------------------------------------------------------
    set_double = Cpt(Custom_Function_Signal, name='set_double')
    set_int = Cpt(Custom_Function_Signal, name='set_int')
    # --------------------------------------------------------------------------
    # Config
    # --------------------------------------------------------------------------
    # === Lock-In Input ===
    float_input = Cpt(Custom_Function_Signal, name='float_input', kind='config')
    imp_50_input = Cpt(Custom_Function_Signal, name='imp_50_input',
        kind='config')
    ac_input = Cpt(Custom_Function_Signal, name='ac_input', kind='config')
    diff_input = Cpt(Custom_Function_Signal, name='diff_input', kind='config')
    # === Filter ===
    filter_order = Cpt(Custom_Function_Signal, name='filter_order',
        kind='config')
    filter_time_constant = Cpt(Custom_Function_Signal,
            name='filter_time_constant', kind='config')
    sinc = Cpt(Custom_Function_Signal, name='sinc', kind='config')
    # === Reference ===
    select_reference = Cpt(Custom_Function_Signal, name='select_reference',
            kind='config')
    select_nth_harmonic = Cpt(Custom_Function_Signal,
            name='select_nth_harmonic', kind='config')
    set_demodulator_phaseshift = Cpt(Custom_Function_Signal,
            name='set_demodulator_phaseshift', kind='config')
    select_1_over_nth_harmonic = Cpt(Custom_Function_Signal,
            name='select_1_over_nth_harmonic', kind='config')
    # --------------------------------------------------------------------------
    # Setting Variables
    # --------------------------------------------------------------------------
    # === Lock-In Input ===
    set_input_range = Cpt(Custom_Function_Signal, name='set_input_range')
    set_input_scaling = Cpt(Custom_Function_Signal, name='set_input_scaling')
    # --------------------------------------------------------------------------
    # Reading Channels
    # --------------------------------------------------------------------------
    # === Lock-In Signal ===
    get_x = Cpt(Custom_Function_SignalRO, name='get_x',
        metadata={'units': 'V'})
    get_y = Cpt(Custom_Function_SignalRO, name='get_y',
        metadata={'units': 'V'})
    get_R = Cpt(Custom_Function_SignalRO, name='get_R',
        metadata={'units': 'V'})
    get_theta = Cpt(Custom_Function_SignalRO, name='get_theta',
        metadata={'units': 'V'})

    def __init__(self, prefix='', *, name, kind=None, read_attrs=None,
                configuration_attrs=None, parent=None, **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind,
        read_attrs=read_attrs, configuration_attrs=configuration_attrs,
        parent=parent, **kwargs)

        self.dev_name = None
        # Store the object returned by the Zurich Instruments library with which
        # one can control the Lock-In
        self.LockIn = None

        # ----------------------------------------------------------------------
        # Connecting
        # ----------------------------------------------------------------------
        self.connect_to_dev.put_function = self.connect_to_dev_function
        self.is_connected.put_function = self.is_connected_function
        # ----------------------------------------------------------------------
        # General Set Function
        # ----------------------------------------------------------------------
        self.set_double.put_function = self.set_double_function
        self.set_int.put_function = self.set_int_function
        # ----------------------------------------------------------------------
        # Config
        # ----------------------------------------------------------------------
        # === Lock-In Input ===
        self.float_input.put_function = self.float_input_function
        self.imp_50_input.put_function = self.imp_50_input_function
        self.ac_input.put_function = self.ac_input_function
        self.diff_input.put_function = self.diff_input_function
        # === Filter ===
        self.filter_order.put_function = self.filter_order_function
        self.filter_time_constant.put_function =\
            self.filter_time_constant_function
        self.sinc.put_function = self.sinc_function
        # === Reference ===
        self.select_reference.put_function = self.select_reference_function
        self.select_nth_harmonic.put_function =\
            self.select_nth_harmonic_function
        self.set_demodulator_phaseshift.put_function =\
            self.select_1_over_nth_harmonic_function
        self.select_1_over_nth_harmonic.put_function = \
                self.select_1_over_nth_harmonic_function
        # ----------------------------------------------------------------------
        # Setting Variables
        # ----------------------------------------------------------------------
        # === Lock-In Input ===
        self.set_input_range.put_function = self.set_input_range_function
        self.set_input_scaling.put_function = self.set_input_scaling_function
        # ----------------------------------------------------------------------
        # Reading Channels
        # ----------------------------------------------------------------------
        # === Lock-In Signal ===
        self.get_x.read_function = self.get_x_function
        self.get_y.read_function = self.get_y_function
        self.get_R.read_function = self.get_R_function
        self.get_theta.read_function = self.get_theta_function

    # --------------------------------------------------------------------------
    # Connecting
    # --------------------------------------------------------------------------
    def connect_to_dev_function(self, dev_name):
        self.dev_name = dev_name
        discovery = ziDiscovery()
        try:
            self.props = discovery.get(discovery.find(self.dev_name))
            try:
                self.LockIn = ziDAQServer(self.props['serveraddress'],
                    self.props['serverport'], self.props['apilevel'])
                self.LockIn.connectDevice(self.dev_name,
                    self.props['interfaces'][0])
            except Exception as e:
                print(f"cannot connect Zurich Instruments MFLI "+\
                    f"({dev_name}): exception occured while trying to "+\
                    f"connect: {e}")
                self.LockIn = None
        except Exception as e:
            print(f"cannot connect Zurich Instruments MFLI ({dev_name}): "+\
                f"discovery threw an exception: {e}")
            self.LockIn = None

    def is_connected_function(self):
        return not self.LockIn is None
    # --------------------------------------------------------------------------
    # General Set Function
    # --------------------------------------------------------------------------
    def set_double_function(self, cmd):
        if not self.LockIn is None:
            if ':' in cmd and len(cmd.split(':')) == 2:
                path = cmd.split(':')[0]
                correct_path = construct_correct_path(self.dev_name, path)
                value = float(cmd.split(':')[1])
                try:
                    self.LockIn.setDouble(correct_path, value)
                except Exception as e:
                    print(f"Zurich Instruments MFLI could not set double "+\
                        f"({cmd}): exception occured {e}")
            else:
                print(f"Zurich Instruments MFLI could not set double "+\
                    f"({cmd}): currently supported syntax: PATH:VALUE")
                
        else:
            print(f"Zurich Instruments MFLI: cannot set double {cmd}: device "+\
                f"not connected.")

    def set_int_function(self, cmd):
        if not self.LockIn is None:
            if ':' in cmd and len(cmd.split(':')) == 2:
                path = cmd.split(':')[0]
                correct_path = construct_correct_path(self.dev_name, path)
                if cmd.split(':')[1].lower() in ['true', 'false']:
                    value = cmd.split(':')[1].lower() == 'true'
                else:
                    value = int(cmd.split(':')[1])
                try:
                    self.LockIn.setInt(correct_path, value)
                except Exception as e:
                    print(f"Zurich Instruments MFLI could not set int "+\
                        f"({cmd}): exception occured {e}")
            else:
                print(f"Zurich Instruments MFLI could not set int "+\
                    "({cmd}): currently supported syntax: PATH:VALUE")
        else:
            print(f"Zurich Instruments MFLI: cannot set int ({cmd}): device "+\
                f"not connected.")

    # --------------------------------------------------------------------------
    # Config
    # --------------------------------------------------------------------------
    # === Lock-In Input ===
    def float_input_function(self, state):
        state = int(state)
        self.set_int_function(f'sigins/0/float:{state}')

    def imp_50_input_function(self, state):
        state = int(state)
        self.set_int_function(f'sigins/0/imp50:{state}')

    def ac_input_function(self, state):
        state = int(state)
        self.set_int_function(f'sigins/0/ac:{state}')

    def diff_input_function(self, state):
        state = int(state)
        self.set_int_function(f'sigins/0/diff:{state}')
    # === Filter ===
    def filter_order_function(self, order):
        self.set_int_function(f'demods/0/order:{order}')

    def filter_time_constant_function(self, tc):
        self.set_double_function(f'demods/0/timeconstant:{tc}')

    def sinc_function(self, state):
        state = int(state)
        self.set_int_function(f'demods/0/sinc:{state}')
    # === Reference ===
    def select_reference_function(self, ref):
        if ref == 'internal':
            self.set_int_function('extrefs/0/enable:0')
        elif ref[:9] == 'external:':
            self.set_int_function('extrefs/0/enable:1')
            self.set_int_function('demods/1/adcselect:'+\
                    EXTERNAL_REFERENCES[ref])
        else:
            print(f"Zurich Instruments MFLI: oscillation reference can "+\
                    f"either be internal or start with 'external:'. '{ref}' "+\
                    f"is not allowed")

    def select_nth_harmonic_function(self, n):
        self.set_int_function(f'demods/0/harmonic:{int(n)}')

    def set_demodulator_phaseshift_function(self, phase):
        self.set_int_function(f'demods/0/phaseshift:{phase}')

    def adjust_demodulator_phase(self):
        self.set_int_function('demods/0/phaseadjust:1')

    def select_1_over_nth_harmonic_function(self, n):
        self.set_int_function(f'demods/1/harmonic:{n}')
    # --------------------------------------------------------------------------
    # Setting Variables
    # --------------------------------------------------------------------------
    # === Lock-In Input ===
    def set_input_range_function(self, rang):
        self.set_double_function(f'sigins/0/range:{rang}')

    def set_input_scaling_function(self, scaling):
        self.set_double_function(f'sigins/0/scaling:{scaling}')
    # --------------------------------------------------------------------------
    # Reading Channels
    # --------------------------------------------------------------------------
    # === Lock-In Signal ===
    def get_x_function(self):
        if not self.LockIn is None:
            try:
                s = self.LockIn.getSample(f"/{self.dev_name}/demods/0/sample")
                return s['x'][0]
            except Exception as e:
                print(f"Zurich Instruments MFLI: cannot get x: exception "+\
                    f"occured: {e}")
            return 0
        else:
            print(f"Zurich Instruments MFLI: cannot get x: device "+\
                f"not connected.")
            return 0

    def get_y_function(self):
        if not self.LockIn is None:
            try:
                s = self.LockIn.getSample(f"/{self.dev_name}/demods/0/sample")
                return s['y'][0]
            except Exception as e:
                print(f"Zurich Instruments MFLI: cannot get y: exception "+\
                    f"occured: {e}")
            return 0
        else:
            print(f"Zurich Instruments MFLI: cannot get y: device "+\
                f"not connected.")
            return 0

    def get_R_function(self):
        if not self.LockIn is None:
            try:
                s = self.LockIn.getSample(f"/{self.dev_name}/demods/0/sample")
                return (s['x'][0]**2+s['y'][0]**2)**.5
            except Exception as e:
                print(f"Zurich Instruments MFLI: cannot get R: exception "+\
                    f"occured: {e}")
            return 0
        else:
            print(f"Zurich Instruments MFLI: cannot get R: device "+\
                "not connected.")
            return 0

    def get_theta_function(self):
        if not self.LockIn is None:
            try:
                s = self.LockIn.getSample(f"/{self.dev_name}/demods/0/sample")
                return np.arctan2(s['y'][0], s['x'][0])
            except Exception as e:
                print(f"Zurich Instruments MFLI: cannot get theta: exception "+\
                    f"occured: {e}")
            return 0
        else:
            print(f"Zurich Instruments MFLI: cannot get theta: device "+\
                f"not connected.")
            return 0
    # --------------------------------------------------------------------------
    # Non-Channel Functions
    # --------------------------------------------------------------------------
    # === Lock-In Input ===
    def autorange_input(self):
        self.set_int_function('sigins/0/autorange:1')
    # --------------------------------------------------------------------------
    # Finalize Steps
    # --------------------------------------------------------------------------
    def finalize_steps(self):
        if not self.LockIn is None:
            self.LockIn.disconnect()
