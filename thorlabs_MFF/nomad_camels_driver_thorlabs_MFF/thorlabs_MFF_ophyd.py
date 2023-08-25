from ophyd import Component as Cpt
from ophyd import Device
from nomad_camels.bluesky_handling.custom_function_signal import \
    Custom_Function_Signal, Custom_Function_SignalRO
from pylablib.devices.Thorlabs import MFF


class Thorlabs_MFF(Device):
    get_position = Cpt(Custom_Function_SignalRO, name='get_position')
    set_position = Cpt(Custom_Function_Signal, name='set_relative_position')

    transit_time = Cpt(Custom_Function_Signal, name='transit_time',
                       kind='config', metadata={'unit': 's',
                                                'description': 'between 0.3 and 2.8'})

    def __init__(self, prefix='', *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None, serial_number='',
                 **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind,
                         read_attrs=read_attrs,
                         configuration_attrs=configuration_attrs, parent=parent,
                         **kwargs)
        if name == 'test':
            return
        self.flip = MFF(serial_number)
        self.flip.open()
        self.transit_time.put_function = lambda x: self.flip.setup_flipper(transit_time=x)
        self.set_position.put_function = self.set_pos
        self.get_position.read_function = self.read_pos

    def read_pos(self):
        state = self.flip.get_state()
        if state is None:
            return -1
        return state

    def set_pos(self, value):
        self.flip.move_to_state(int(value))

    def finalize_steps(self):
        self.flip.close()

