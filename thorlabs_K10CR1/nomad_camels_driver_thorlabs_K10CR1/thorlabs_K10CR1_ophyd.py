from ophyd import Component as Cpt
from ophyd import Device
from nomad_camels.bluesky_handling.custom_function_signal import \
    Custom_Function_Signal, Custom_Function_SignalRO
from pylablib.devices.Thorlabs import KinesisMotor


class Thorlabs_K10CR1(Device):
    get_position = Cpt(Custom_Function_SignalRO, name='get_position')
    set_position = Cpt(Custom_Function_Signal, name='set_relative_position')


    acceleration = Cpt(Custom_Function_Signal, name='acceleration',
                       kind='config')
    max_velocity = Cpt(Custom_Function_Signal, name='max_velocity',
                       kind='config')

    def __init__(self, prefix='', *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None, serial_number='',
                 home_on_start=True, **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind,
                         read_attrs=read_attrs,
                         configuration_attrs=configuration_attrs, parent=parent,
                         **kwargs)
        if name == 'test':
            return
        self.stage = KinesisMotor(serial_number, 'K10CR1')
        self.stage.open()
        if home_on_start:
            self.stage.home()
        self.set_position.put_function = self.set_pos
        self.get_position.read_function = self.read_pos
        self.acceleration.put_function = lambda x: self.stage.setup_velocity(acceleration=x)
        self.max_velocity.put_function = lambda x: self.stage.setup_velocity(max_velocity=x)

    def read_pos(self):
        return self.stage.get_position()

    def set_pos(self, value):
        self.stage.move_to(value)
        # self.stage.wait_move()

    def finalize_steps(self):
        self.stage.close()

