from ophyd import Component as Cpt
from ophyd import Device

from nomad_camels.bluesky_handling.custom_function_signal import Custom_Function_Signal, Custom_Function_SignalRO

from pytrinamic.connections import ConnectionManager
from pytrinamic.modules import TMCM1140
import time


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
        try:
            self.interface = ConnectionManager(f'--port {connection_port}').connect()
        except:
            arg_string = f"--interface serial_tmcl --port {connection_port} --data-rate 115200"
            self.interface = ConnectionManager(arg_string).connect()
        self.module = TMCM1140(self.interface)
        self.motor_number = motor_number
        self.motor = self.module.motors[motor_number]

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
        elif name in ['right_lim_switch_disable', 'left_lim_switch_disable',
                      'soft_stop_flag']:
            value = int(value)
        self.motor.set_axis_parameter(self.ap_names[name], value)

    def configure(self, d):
        super().configure(d)
        if self.search_reference_on_start:
            self.find_reference()

    def find_reference(self):
        self.interface.reference_search(0, self.motor_number, self.module.module_id)
        while self.interface.reference_search(2, self.motor_number,
                                              self.module.module_id):
            time.sleep(0.1)
        self.motor.actual_position = 0

    def move_position(self, value):
        self.motor.move_to(value)
        while not self.motor.get_position_reached():
            time.sleep(0.1)



if __name__ == '__main__':

    # for serial interface
    #with ConnectionManager("--interface serial_tmcl --port COM6 --data-rate 115200").connect() as my_interface:
    # for usb interface
    stage = TMCM_1110(name='stage')
    with ConnectionManager('--port COM11').connect() as my_interface:
        print(my_interface)
        module = TMCM1140(my_interface)
        motor = module.motors[0]


        # The configuration is based on our PD42-1-1140-TMCL
        # If you use a different motor be sure you have the right configuration setup otherwise the script may not working.

        print("Preparing parameters...")

        motor.set_axis_parameter(motor.AP.ReferenceSearchMode, reference_search_modes['left switch'])
        motor.set_axis_parameter(motor.AP.RightLimitSwitchDisable, 1)
        motor.set_axis_parameter(motor.AP.LeftLimitSwitchDisable, 1)
        motor.set_axis_parameter(motor.AP.ReferenceSearchSpeed, 100)
        motor.set_axis_parameter(motor.AP.ReferenceSwitchSpeed, 10)
        motor.set_axis_parameter(motor.AP.MaxAcceleration, 100)
        motor.set_axis_parameter(motor.AP.MaxVelocity, 100)
        motor.set_axis_parameter(motor.AP.PowerDownDelay, 2000)
        motor.set_axis_parameter(motor.AP.StandbyCurrent, 0)
        motor.set_axis_parameter(motor.AP.MaxCurrent, 200)
        motor.set_axis_parameter(motor.AP.FreewheelingDelay, 2000)
        motor.set_axis_parameter(motor.AP.PulseDivisor, 4)
        motor.set_axis_parameter(motor.AP.RampDivisor, 7)
        motor.set_axis_parameter(motor.AP.SoftStopFlag, 1)
        motor.set_axis_parameter(motor.AP.MicrostepResolution, step_mode['8 micro'])

        # preparing drive settings
        # motor.drive_settings.max_current = 200
        # motor.drive_settings.standby_current = 0
        # # motor.drive_settings.boost_current = 0
        # motor.drive_settings.microstep_resolution = motor.ENUM.MicrostepResolution256Microsteps
        # motor.set_axis_parameter()
        # # print(motor.drive_settings)

        # preparing linear ramp settings
        # motor.linear_ramp.max_acceleration = 1000
        # motor.linear_ramp.max_velocity = 1000
        # print(motor.linear_ramp)

        time.sleep(1.0)

        motor.move_to(5000)
        while not motor.get_position_reached():
            print("target position: " + str(motor.target_position) + " actual position: " + str(motor.actual_position))
            time.sleep(0.2)
        my_interface.reference_search(0, 0, module.module_id)
        print(my_interface.reference_search(2, 0, module.module_id))
        while my_interface.reference_search(2, 0, module.module_id):
            print("target position: " + str(motor.target_position) + " actual position: " + str(motor.actual_position))
            print(my_interface.reference_search(2, 0, module.module_id))
            time.sleep(0.2)
        # time.sleep(5)
        print(my_interface.reference_search(2, 0, module.module_id))
        raise Exception('break')
        # clear position counter
        motor.actual_position = 0
        # start rotating motor for 5 sek
        # print("Rotating...")
        # motor.rotate(1000)
        # time.sleep(5)

        # # stop rotating motor
        # print("Stopping...")
        # motor.stop()

        # # read actual position
        # print("ActualPosition = {}".format(motor.actual_position))
        # time.sleep(2)

        # print("Doubling moved distance.")
        # motor.move_by(motor.actual_position)

        # # wait till position_reached
        # while not motor.get_position_reached():
        #     print("target position: " + str(motor.target_position) + " actual position: " + str(motor.actual_position))
        #     time.sleep(0.2)

        # print("Furthest point reached.")
        # print("ActualPosition = {}".format(motor.actual_position))

        # # short delay and move back to start
        # time.sleep(3)
        print("Moving back to 0...")
        motor.move_to(3473)
        # wait until position 0 is reached
        while not motor.get_position_reached():
            print("target position: " + str(motor.target_position) + " actual position: " + str(motor.actual_position))
            time.sleep(0.2)
        print("Reached position 0.")
        time.sleep(5)

        motor.move_to(2432)
        # wait until position 0 is reached
        while not motor.get_position_reached():
            print("target position: " + str(motor.target_position) + " actual position: " + str(motor.actual_position))
            time.sleep(0.2)
        print("Reached position 1.")
        time.sleep(5)

        motor.move_to(1400)
        # wait until position 0 is reached
        while not motor.get_position_reached():
            print("target position: " + str(motor.target_position) + " actual position: " + str(motor.actual_position))
            time.sleep(0.2)
        print("Reached position 2.")
        time.sleep(5)

        motor.move_to(418)
        # wait until position 0 is reached
        while not motor.get_position_reached():
            print("target position: " + str(motor.target_position) + " actual position: " + str(motor.actual_position))
            time.sleep(0.2)
        print("Reached position 3.")
        time.sleep(5)

        motor.move_to(-600)
        # wait until position 0 is reached
        while not motor.get_position_reached():
            print("target position: " + str(motor.target_position) + " actual position: " + str(motor.actual_position))
            time.sleep(0.2)
        print("Reached position 4.")
        time.sleep(5)

        motor.move_to(-1600)
        # wait until position 0 is reached
        while not motor.get_position_reached():
            print("target position: " + str(motor.target_position) + " actual position: " + str(motor.actual_position))
            time.sleep(0.2)
        print("Reached position block.")
        time.sleep(5)

    print("\nReady.")