from ophyd import Component as Cpt
from ophyd import Device

from nomad_camels.bluesky_handling.custom_function_signal import Custom_Function_Signal, Custom_Function_SignalRO

from pytrinamic.connections import ConnectionManager
from pytrinamic.modules import TMCM1140
import time
import re


reference_search_modes = {'left switch': 1,
                          'right switch': 65,
                          'right then left switch': 2,
                          'left then right switch': 66,
                          'right then left switch (both sides)': 3,
                          'left then right switch (both sides)': 67,
                          'left switch (both sides)': 4,
                          'right switch (both sides)': 68,
                          'home switch (negative dir)': 5,
                          'home switch (positive dir)': 6,
                          'home switch (positive dir, ignore end switch)': 7,
                          'home switch (negative dir, ignore end switch)': 8}
step_mode = {'full': 0,
             'half': 1,
             '4 micro': 2,
             '8 micro': 3,
             '16 micro': 4,
             '32 micro': 5,
             '64 micro': 6,
             '128 micro': 7,
             '256 micro': 8}




class TMCM_1110(Device):

    set_position = Cpt(Custom_Function_Signal, name='set_position')
    get_position = Cpt(Custom_Function_SignalRO, name='get_position')

    ref_search_mode = Cpt(Custom_Function_Signal, name='ref_search_mode', kind='config')
    right_lim_switch_disable = Cpt(Custom_Function_Signal, name='right_lim_switch_disable', kind='config')
    left_lim_switch_disable = Cpt(Custom_Function_Signal, name='left_lim_switch_disable', kind='config')
    ref_search_speed = Cpt(Custom_Function_Signal, name='ref_search_speed', kind='config')
    ref_switch_speed = Cpt(Custom_Function_Signal, name='ref_switch_speed', kind='config')
    max_acceleration = Cpt(Custom_Function_Signal, name='max_acceleration', kind='config')
    max_velocity = Cpt(Custom_Function_Signal, name='max_velocity', kind='config')
    power_down_delay = Cpt(Custom_Function_Signal, name='power_down_delay', kind='config')
    standby_current = Cpt(Custom_Function_Signal, name='standby_current', kind='config')
    max_current = Cpt(Custom_Function_Signal, name='max_current', kind='config')
    freewheeling_delay = Cpt(Custom_Function_Signal, name='freewheeling_delay', kind='config')
    pulse_divisor = Cpt(Custom_Function_Signal, name='pulse_divisor', kind='config')
    ramp_divisor = Cpt(Custom_Function_Signal, name='ramp_divisor', kind='config')
    soft_stop_flag = Cpt(Custom_Function_Signal, name='soft_stop_flag', kind='config')
    microstep_resolution = Cpt(Custom_Function_Signal, name='microstep_resolution', kind='config')

    def __init__(self, prefix='', *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None, connection_port='',
                 search_reference_on_start=True, motor_number=0, **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs,
                         configuration_attrs=configuration_attrs, parent=parent,
                         **kwargs)
        if name == 'test':
            return
        self.search_reference_on_start = search_reference_on_start
        connection_port_match = re.match(r'ASRL(\d*)::INSTR',connection_port)
        try:
            self.interface = ConnectionManager(f'--port COM{connection_port_match.group(1)}').connect()
        except:
            arg_string = f"--interface serial_tmcl --port COM{connection_port_match.group(1)} --data-rate 115200"
            self.interface = ConnectionManager(arg_string).connect()
        self.module = TMCM1140(self.interface)
        self.motor_number = int(motor_number)
        self.motor = self.module.motors[self.motor_number]

        ap = self.motor.AP
        self.ap_names = {'ref_search_mode': ap.ReferenceSearchMode,
                         'right_lim_switch_disable': ap.RightLimitSwitchDisable,
                         'left_lim_switch_disable': ap.LeftLimitSwitchDisable,
                         'ref_search_speed': ap.ReferenceSearchSpeed,
                         'ref_switch_speed': ap.ReferenceSwitchSpeed,
                         'max_acceleration': ap.MaxAcceleration,
                         'max_velocity': ap.MaxVelocity,
                         'power_down_delay': ap.PowerDownDelay,
                         'standby_current': ap.StandbyCurrent,
                         'max_current': ap.MaxCurrent,
                         'freewheeling_delay': ap.FreewheelingDelay,
                         'pulse_divisor': ap.PulseDivisor,
                         'ramp_divisor': ap.RampDivisor,
                         'soft_stop_flag': ap.SoftStopFlag,
                         'microstep_resolution': ap.MicrostepResolution}

        self.ref_search_mode.put_function = lambda x: self.set_parameter(x, 'ref_search_mode')
        self.right_lim_switch_disable.put_function = lambda x: self.set_parameter(x, 'right_lim_switch_disable')
        self.left_lim_switch_disable.put_function = lambda x: self.set_parameter(x, 'left_lim_switch_disable')
        self.ref_search_speed.put_function = lambda x: self.set_parameter(x, 'ref_search_speed')
        self.ref_switch_speed.put_function = lambda x: self.set_parameter(x, 'ref_switch_speed')
        self.max_acceleration.put_function = lambda x: self.set_parameter(x, 'max_acceleration')
        self.max_velocity.put_function = lambda x: self.set_parameter(x, 'max_velocity')
        self.power_down_delay.put_function = lambda x: self.set_parameter(x, 'power_down_delay')
        self.standby_current.put_function = lambda x: self.set_parameter(x, 'standby_current')
        self.max_current.put_function = lambda x: self.set_parameter(x, 'max_current')
        self.freewheeling_delay.put_function = lambda x: self.set_parameter(x, 'freewheeling_delay')
        self.pulse_divisor.put_function = lambda x: self.set_parameter(x, 'pulse_divisor')
        self.ramp_divisor.put_function = lambda x: self.set_parameter(x, 'ramp_divisor')
        self.soft_stop_flag.put_function = lambda x: self.set_parameter(x, 'soft_stop_flag')
        self.microstep_resolution.put_function = lambda x: self.set_parameter(x, 'microstep_resolution')

        self.set_position.put_function = self.move_position
        self.get_position.read_function = self.motor.get_actual_position

    def set_parameter(self, value, name):
        if name == 'ref_search_mode':
            value = reference_search_modes[value]
        elif name == 'microstep_resolution':
            value = step_mode[value]
        else:
            value = int(value)
        self.motor.set_axis_parameter(self.ap_names[name], value)

    def configure(self, d):
        conf = super().configure(d)
        if self.search_reference_on_start:
            self.find_reference()
        return conf

    def find_reference(self):
        self.interface.reference_search(0, self.motor_number, self.module.module_id)
        while self.interface.reference_search(2, self.motor_number,
                                              self.module.module_id):
            time.sleep(0.1)
        self.motor.actual_position = 0

    def move_position(self, value):
        self.motor.move_to(int(value))
        while not self.motor.get_position_reached():
            time.sleep(0.1)
            print()

    def finalize_steps(self):
        self.interface.close()

