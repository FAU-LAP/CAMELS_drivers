from ophyd import Component as Cpt
from ophyd import Device
from nomad_camels.bluesky_handling.custom_function_signal import \
    Custom_Function_Signal, Custom_Function_SignalRO
try:
    from .TLPM import TLPM
except ModuleNotFoundError as e:
    import os
    import warnings
    warnings.warn(f'It seems you have not installed the Thorlabs support for TLPM!\nMake sure it is installed, if it is not working, copy the files "TLPM.py" and "TLPM_64.dll" to {os.path.dirname(__file__)}\n\n{e}"')
from ctypes import c_uint32, byref, create_string_buffer, c_bool, c_char_p, c_int, c_double

class Thorlabs_TLPM(Device):
    power = Cpt(Custom_Function_SignalRO, name='power')
    wavelength = Cpt(Custom_Function_Signal, name='wavelength', kind='config')
    calibration_msg = Cpt(Custom_Function_SignalRO, name='calibration_msg', kind='config')


    def __init__(self, prefix='', *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None, resource='', **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind,
                         read_attrs=read_attrs,
                         configuration_attrs=configuration_attrs, parent=parent,
                         **kwargs)
        if name == 'test':
            return
        self.pm = TLPM()
        self.pm.open(resource.encode(), c_bool(True), c_bool(True))
        self.power.read_function = self.getPower
        self.wavelength.put_function = self.setWavelength
        self.wavelength.read_function = self.getWavelength
        self.calibration_msg.read_function = self.get_calibration
    
    def get_calibration(self):
        message = create_string_buffer(1024)
        self.pm.getCalibrationMsg(message)
        return c_char_p(message.raw).value.decode()    

    def getPower(self):
        power = c_double()
        self.pm.measPower(byref(power))
        return power.value

    def setWavelength(self, value):
        val = c_double(value)
        self.pm.setWavelength(val)
        return value

    def getWavelength(self):
        wl = c_double()
        self.pm.getWavelength(0, byref(wl))
        return wl.value

    
    def finalize_steps(self):
        self.pm.close()

def init():
    global tlPM
    tlPM = TLPM()
    deviceCount = c_uint32()
    tlPM.findRsrc(byref(deviceCount))

    print("devices found: " + str(deviceCount.value))

    resourceName = create_string_buffer(1024)

    for i in range(0, deviceCount.value):
        tlPM.getRsrcName(c_int(i), resourceName)
        print(c_char_p(resourceName.raw).value)

    tlPM.close()
    tlPM = TLPM()
    #resourceName = create_string_buffer(b"COM1::115200")
    # print(c_char_p(resourceName.raw).value)
    tlPM.open(resourceName, c_bool(True), c_bool(True))
    message = create_string_buffer(1024)
    tlPM.getCalibrationMsg(message)
    print(c_char_p(message.raw).value)
    tlPM.close()



if __name__ == '__main__':
    init()

