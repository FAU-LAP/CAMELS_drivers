from ophyd import Component as Cpt
from ophyd import Device
from nomad_camels.bluesky_handling.custom_function_signal import \
    Custom_Function_Signal, Custom_Function_SignalRO
import time

try:
    from nomad_camels_driver_mechonics_cu30cl.servo3ax_wrapper import Servo3AxUSB2Wrapper
except FileNotFoundError as e:
    import os
    import warnings
    warnings.warn(f'It seems you have not installed the Mechonics support for CU30CL!\nMake sure it is installed, if it is not working, copy the files "Servo3AxWrap.dll" and "Servo3AxUSB2.dll"/"Servo3AxUSB2_x64.dll" to {os.path.dirname(__file__)}\n\n{e}"')

class Mechonics_CU30CL(Device):
    x_set_position = Cpt(Custom_Function_Signal, name='x_set_position')
    y_set_position = Cpt(Custom_Function_Signal, name='y_set_position')
    z_set_position = Cpt(Custom_Function_Signal, name='z_set_position')
    x_get_position = Cpt(Custom_Function_SignalRO, name='x_get_position')
    y_get_position = Cpt(Custom_Function_SignalRO, name='y_get_position')
    z_get_position = Cpt(Custom_Function_SignalRO, name='z_get_position')

    timeconstant = Cpt(Custom_Function_Signal, name='timeconstant', kind='config')
    speed_x = Cpt(Custom_Function_Signal, name='speed_x', kind='config')
    speed_y = Cpt(Custom_Function_Signal, name='speed_y', kind='config')
    speed_z = Cpt(Custom_Function_Signal, name='speed_z', kind='config')

    resolution_x = Cpt(Custom_Function_Signal, name='resolution_x', kind='config')
    resolution_y = Cpt(Custom_Function_Signal, name='resolution_y', kind='config')
    resolution_z = Cpt(Custom_Function_Signal, name='resolution_z', kind='config')
    
    orientation_x = Cpt(Custom_Function_Signal, name='orientation_x', kind='config')
    orientation_y = Cpt(Custom_Function_Signal, name='orientation_y', kind='config')
    orientation_z = Cpt(Custom_Function_Signal, name='orientation_z', kind='config')

    # eeprom_data = Cpt(Custom_Function_SignalRO, name='eeprom_data', kind='config')

    
    def __init__(self, prefix="", *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None,
                 ax_X=True, ax_Y=True, ax_Z=True, threshold_x=3,
                 threshold_y=3, threshold_z=3, time_threshold_x=5,
                 time_threshold_y=5, time_threshold_z=5, **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind,
                         read_attrs=read_attrs,
                         configuration_attrs=configuration_attrs, parent=parent,
                         **kwargs)
        comps = list(self.component_names)
        if not ax_X:
            for comp in self.component_names:
                if 'x' in comp:
                    comps.remove(comp)
        if not ax_Y:
            for comp in self.component_names:
                if 'y' in comp:
                    comps.remove(comp)
        if not ax_Z:
            for comp in self.component_names:
                if 'z' in comp:
                    comps.remove(comp)
        self.axes = []
        if ax_X:
            self.axes.append(1)
        if ax_Y:
            self.axes.append(2)
        if ax_Z:
            self.axes.append(3)
        self.component_names = tuple(comps)
        if name == 'test':
            return
        axes = [ax_X, ax_Y, ax_Z]
        force_thresholds = [threshold_x, threshold_y, threshold_z]
        time_thresholds = [time_threshold_x, time_threshold_y, time_threshold_z]
        self.stage = Servo3AxUSB2Wrapper(enableds=axes,
                                         forceThresholds=force_thresholds,
                                         timeThresholds=time_thresholds)
        self.stage.enable_disable_axes([ax_X, ax_Y, ax_Z])
        
        self.x_set_position.put_function = lambda x, ax=0: self.move_stage(ax, x)
        self.y_set_position.put_function = lambda x, ax=1: self.move_stage(ax, x)
        self.z_set_position.put_function = lambda x, ax=2: self.move_stage(ax, x)
        self.x_get_position.read_function = lambda ax=0: self.read_position(ax)
        self.y_get_position.read_function = lambda ax=1: self.read_position(ax)
        self.z_get_position.read_function = lambda ax=2: self.read_position(ax)

        self.speed_x.put_function = lambda x, ax=0: self.set_speed(ax, x)
        self.speed_y.put_function = lambda x, ax=1: self.set_speed(ax, x)
        self.speed_z.put_function = lambda x, ax=2: self.set_speed(ax, x)

        self.orientations = self.stage.positionerProperties['driveOrientation']
        self.resolutions = self.stage.positionerProperties['encoderResolution_um']
        self.orientation_x.put_function = lambda x, ax=0: self.set_orientation(ax, x)
        self.orientation_y.put_function = lambda x, ax=1: self.set_orientation(ax, x)
        self.orientation_z.put_function = lambda x, ax=2: self.set_orientation(ax, x)
        self.resolution_x.put_function = lambda x, ax=0: self.set_resolution(ax, x)
        self.resolution_y.put_function = lambda x, ax=1: self.set_resolution(ax, x)
        self.resolution_z.put_function = lambda x, ax=2: self.set_resolution(ax, x)

        self.timeconstant.put_function = self.stage._setTimeConstant

        # self.eeprom_data.read_function = self.stage._get_EEPROM_info
        self._set_positions = [0, 0, 0]
        self._speeds = self.stage.get_speeds()
        self.update_set_positions()
        self.currently_setting = False

    def update_set_positions(self):
        positions = self.stage.get_position()
        self.x_set_position._readback = positions[0]
        self.y_set_position._readback = positions[1]
        self.z_set_position._readback = positions[2]
        self._set_positions = positions
    
    def find_reference(self):
        self.stage.findReference(force=True, axes=self.axes)
        time.sleep(0.1)
        self.update_set_positions()

    def stop_movement(self):
        self.stage._piezo_stop()

    def read_position(self, ax):
        vals = self.stage.get_position()
        return vals[ax]

    def move_stage(self, ax, pos):
        self._set_positions[ax] = pos
        print(self._set_positions, self.stage.get_position())
        self.stage.move_to_position_async(self._set_positions, self._speeds)
    
    def set_speed(self, ax, speed):
        self._speeds[ax] = speed
    
    def set_orientation(self, ax, orientation):
        while self.currently_setting:
            time.sleep(0.1)
        self.currently_setting = True
        self.orientations[ax] = orientation
        self.stage._set_positioner_properties(self.resolutions, self.orientations)
        self.currently_setting = False
    
    def set_resolution(self, ax, resolution):
        while self.currently_setting:
            time.sleep(0.1)
        self.currently_setting = True
        self.resolutions[ax] = resolution
        self.stage._set_positioner_properties(self.resolutions, self.orientations)
        self.currently_setting = False
    
    def finalize_steps(self):
        self.stage.close()

    def manual_move_start_x(self, speed=None):
        self._manual_move_start(0, speed)

    def manual_move_start_y(self, speed=None):
        self._manual_move_start(1, speed)

    def manual_move_start_z(self, speed=None):
        self._manual_move_start(2, speed)

    def _manual_move_start(self, ax, speed=None):
        speed = speed or self._speeds[ax]
        speeds = [0, 0, 0]
        directions = [0, 0, 0]
        if speed < 0:
            speed *= -1
            directions[ax] = 1
        speeds[ax] = speed
        self.stage.direction_move(speeds, directions)




if __name__ == '__main__':
    settings = {'ax_X': True, 'ax_Y': True, 'ax_Z': False}
    mechonics_cu30cl = Mechonics_CU30CL("mechonics_cu30cl:", name="mechonics_cu30cl", **settings)
    config = {'timeconstant': 200, 'speed_x': 100, 'speed_y': 100, 'resolution_x': 0.05, 'resolution_y': 0.05, 'orientation_x': 0, 'orientation_y': 0}
    # print(mechonics_cu30cl.configure(config))
    # print(mechonics_cu30cl.read_configuration())
    print(mechonics_cu30cl.eeprom_data.get())
    mechonics_cu30cl.timeconstant.put(200)
    mechonics_cu30cl.resolution_x.put(0.05)
    mechonics_cu30cl.resolution_y.put(0.05)
    mechonics_cu30cl.orientation_x.put(0)
    mechonics_cu30cl.orientation_y.put(0)
    mechonics_cu30cl.speed_x.put(100)
    mechonics_cu30cl.speed_y.put(100)
    mechonics_cu30cl.find_reference()
    print(mechonics_cu30cl.stage._get_positioner_properties())
    print(mechonics_cu30cl.stage._getTimeConstant())
    print(mechonics_cu30cl.stage._read_pick_encoder())
    print(mechonics_cu30cl.stage.get_position())
    print(mechonics_cu30cl.x_get_position.get(), mechonics_cu30cl.y_get_position.get())
    mechonics_cu30cl.x_set_position.put(2000)
    import time
    for i in range(7):
        time.sleep(1)
        print(mechonics_cu30cl.x_get_position.get())
    mechonics_cu30cl.x_set_position.put(0)
    mechonics_cu30cl.y_set_position.put(2000)
    for i in range(7):
        time.sleep(1)
        print(mechonics_cu30cl.x_get_position.get(), mechonics_cu30cl.y_get_position.get())
    mechonics_cu30cl.finalize_steps()
