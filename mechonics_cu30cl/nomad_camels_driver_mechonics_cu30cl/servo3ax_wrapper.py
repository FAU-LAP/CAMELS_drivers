"""This module provides communication with the mechonics CU30CL controller, via
the C-wrapper .dll. The functions in the Servo3AxUSB2Wrapper class mostly follow
the corresponding labview library."""

import os
from ctypes import create_string_buffer, c_char_p, c_double, c_ulong, WinDLL, POINTER, byref
import time

f_path = os.path.dirname(__file__)
dll = WinDLL(f'{f_path}/Servo3AxWrap.dll')

devRec = [c_ulong,  # USBInstance
          c_ulong,  # USBVersion
          c_ulong,  # device-type (7 or 14)
          c_ulong]  # EEID, device to be adressed
devRecRef = [POINTER(c_ulong), POINTER(c_ulong),  # same es devRec,
             POINTER(c_ulong), POINTER(c_ulong)]  # just with pointers

# The function opens a connection to the hardware through the selected USB port.
dllOpen = dll.Servo3WAxUSB2Open
dllOpen.argtypes = devRecRef
dllOpen.restype = c_char_p


# The function closes a connection to the hardware through the selected USB port,
# opened with previous call of Servo3WAXUSB2Open() function.
dllClose = dll.Servo3WAxUSB2Close
dllClose.argtypes = devRec
dllClose.restype = None


# The function instantly terminates any movement of the selected hardware.
dllPiezoStop = dll.Servo3WAxUSB2PiezoStop
dllPiezoStop.argtypes = devRec
dllPiezoStop.restype = None


# The function switches DCDC-converter on for the selected hardware.
dllDCDCon = dll.Servo3WAxUSB2DCDCon
dllDCDCon.argtypes = devRec
dllDCDCon.restype = None


# The function switches DCDC-converter off for the selected hardware.
dllDCDCoff = dll.Servo3WAxUSB2DCDCoff
dllDCDCoff.argtypes = devRec
dllDCDCoff.restype = None


# The function performs the setting of the characteristics of a positioner.
# The last two parameters contain the data, needed for proper filling of the
# PositionerRec structure
dllSetProperties = dll.Servo3WAxUSB2SetPositionerProperties
dllSetProperties.argtypes = devRec + [POINTER(c_double), # 3-array of resolution along axes
                                      POINTER(c_ulong)] # 3-array of orientation of axes
dllSetProperties.restype = None


# The function returns the characteristics of a positioner. The last two
# parameters contain the data from the PositionerRec structure.
dllGetProperties = dll.Servo3WAxUSB2GetPositionerProperties
dllGetProperties.argtypes = devRec + [POINTER(c_double), # 3-array of resolution along axes
                                      POINTER(c_ulong)] # 3-array of orientation of axes
dllGetProperties.restype = None


# The function performs the setting of the characteristics of a controller.
# Only enabled, hard limit, forceThreshold, timeThreshold and autoShutOff are
# actually sent to the controller
dllSetControllerProp = dll.Servo3WAxUSB2SetControlerProperties
dllSetControllerProp.argtypes = devRec + [POINTER(c_double), # position
                                          POINTER(c_double), # speed
                                          POINTER(c_ulong), # ref-count
                                          POINTER(c_ulong), # ref valid
                                          POINTER(c_ulong), # indexStatus
                                          POINTER(c_double), # position error
                                          POINTER(c_ulong), # enabled (0 disabled, 255 enabled)
                                          POINTER(c_ulong), # hard limit (counter)
                                          POINTER(c_ulong), # forceThreshold (for auto shut off)
                                          POINTER(c_ulong), # timeThreshold (time constant for auto shut off)
                                          POINTER(c_ulong), # autoShutOff (0 off, 1 on)
                                          c_ulong, # loopCounter
                                          c_ulong, # dcdcStatus
                                          c_ulong] # extVoltageStatus
dllSetControllerProp.restype = None


# The function gets the characteristics of the attached controller.
dllReadAndPickEncoder = dll.Servo3WAxUSB2ReadandPickupEncoderResult
dllReadAndPickEncoder.argtypes = devRec + [POINTER(c_double), # position
                                           POINTER(c_double), # speed
                                           POINTER(c_ulong), # reference count
                                           POINTER(c_ulong), # reference valid
                                           POINTER(c_ulong), # index status
                                           POINTER(c_double), # position error
                                           POINTER(c_ulong), # enabled
                                           POINTER(c_ulong), # hard limit
                                           POINTER(c_ulong), # force threshold
                                           POINTER(c_ulong), # time threshold
                                           POINTER(c_ulong), # auto shut off
                                           POINTER(c_ulong), # loop counter
                                           POINTER(c_ulong), # dcdc status
                                           POINTER(c_ulong)] # ext voltage status
dllReadAndPickEncoder.restype = None


# The function performs movement in manual (Open-Loop ) or servo mode
# (Closed-Loop). The servo mode only works if the controller has found the
# reference from the measurement system (the linear encoder).
dllManualServoMove = dll.Servo3WAxUSB2ManuelServoMove
dllManualServoMove.argtypes = devRec + [c_ulong, c_ulong, c_ulong, c_double,
                                        c_ulong, c_ulong, c_ulong, c_double,
                                        c_ulong, c_ulong, c_ulong, c_double]
# each line: vi, di, mi, dpi of axis i with:
# vi: velocity
# di: direction in open-loop (0 pos, 1 neg)
# mi: mode (0 open-loop, 1 closed-loop)
# dpi: absolute pos in closed-loop
dllManualServoMove.restype = None


# For all three axes: if 1, every time ref is passed, measurement is reset to 0
dllSetIndex = dll.Servo3WAxUSB2SetIndex
dllSetIndex.argtypes = devRec + [c_ulong, c_ulong, c_ulong]
dllSetIndex.restype = None


# The function performs movement along one of the axes up to the hard limit with
# following stop.
dllGotoLimit = dll.Servo3WAxUSB2GotoLimit
dllGotoLimit.argtypes = devRec + [c_ulong, # axis (1, 2, 3)
                                  c_ulong, # direction (0 pos, 1 neg)
                                  c_ulong] # velocity (2...255)
dllGotoLimit.restype = None


# The function performs movement along one of the axes up to a reference with
# following stop.
dllGotoReference = dll.Servo3WAxUSB2GotoReference
dllGotoReference.argtypes = devRec + [c_ulong, # axis (1, 2, 3)
                                      c_ulong, # direction of move (0 pos, 1 neg)
                                      c_ulong] # velocity (2...255)
dllGotoReference.restype = None


# The function enables a selected axis.
dllAsyncEnableAx = dll.Servo3WAxUSB2AsyncEnableAxis
dllAsyncEnableAx.argtypes = devRec + [c_ulong]
dllAsyncEnableAx.restype = None


# The function disables a selected axis.
dllAsyncDisableAx = dll.Servo3WAxUSB2AsyncDisableAxis
dllAsyncDisableAx.argtypes = devRec + [c_ulong]
dllAsyncDisableAx.restype = None


# The function returns a set of collected information from EEPROM.
dllGetEEPROMinfo = dll.Servo3WAxUSB2GetEEPROMInfo
dllGetEEPROMinfo.argtypes = devRec + [POINTER(c_ulong), # USB vendor ID
                                      POINTER(c_ulong), # USB product ID
                                      POINTER(c_ulong), # USB device ID
                                      POINTER(c_ulong), # device ID
                                      POINTER(c_ulong), # EEProm ID
                                      POINTER(c_ulong), # version
                                      POINTER(c_ulong), # serial number
                                      POINTER(c_ulong), # customer ID
                                      c_char_p, # company
                                      c_char_p, # date
                                      c_char_p, # product str
                                      c_char_p, # customer
                                      c_char_p] # customer str
dllGetEEPROMinfo.restype = None


# The function switches power internally on for the selected hardware.
dllPowerOn = dll.Servo3WAxUSB2InternalPowerOn
dllPowerOn.argtypes = devRec
dllPowerOn.restype = None


# The function switches power internally off for the selected hardware.
dllPowerOff = dll.Servo3WAxUSB2InternalPowerOff
dllPowerOff.argtypes = devRec
dllPowerOff.restype = None


# The function sets or gets additional characteristics of the attached controller.
dllServoProperties = dll.Servo3WAxUSB2ServoProperties
dllServoProperties.argtypes = devRec + [c_char_p, # null-terminated string, max 31 characters, representing command
                                        POINTER(c_double)] # additional value, timeconstant (0...255)
dllServoProperties.restype = None




class Servo3AxUSB2Wrapper:

    def __init__(self, usbInstance=0, usbVersion=2, devID=14, eeid=0,
                 indices=None, enableds=None, hardLimits=None,
                 forceThresholds=None, timeThresholds=None, autoShutOffs=None):
        self.devRec = [c_ulong(usbInstance), c_ulong(usbVersion),
                       c_ulong(devID), c_ulong(eeid)]
        self._open()
        self._power_on()
        self._dcdc_on()

        self.positionerProperties = self._get_positioner_properties()

        self.EEPROM_data = self._get_EEPROM_info()

        indices = indices or [1, 1, 1]
        self._set_index(*indices)

        self.enabled_axes = enableds
        self._set_controller_properties(enableds, hardLimits, forceThresholds,
                                        timeThresholds, autoShutOffs)
        self._piezo_stop()


    def _set_properties(self, command, value=200):
        if isinstance(command, str):
            command = command.encode()
        value = c_double(value)
        dllServoProperties(*self.devRec, command, value)
        return value
    
    def _async_disable(self, axis):
        dllAsyncDisableAx(*self.devRec, c_ulong(axis))
    
    def _async_enable(self, axis):
        dllAsyncEnableAx(*self.devRec, c_ulong(axis))
    
    def _close(self):
        dllClose(*self.devRec)
    
    def _dcdc_off(self):
        dllDCDCoff(*self.devRec)
    
    def _dcdc_on(self):
        dllDCDCon(*self.devRec)
    
    def _get_EEPROM_info(self):        
        usbVendorID = c_ulong(0)
        usbProductID = c_ulong(0)
        usbDeviceID = c_ulong(0)
        deviceID = c_ulong(0)
        eepromID = c_ulong(0)
        version = c_ulong(0)
        serialNumber = c_ulong(0)
        customerID = c_ulong(0)
        company = create_string_buffer(32)
        date = create_string_buffer(32)
        productStr = create_string_buffer(32)
        customer = create_string_buffer(32)
        customerStr = create_string_buffer(32)        
        dllGetEEPROMinfo(*self.devRec, byref(usbVendorID), byref(usbProductID),
                         byref(usbDeviceID),
                         byref(deviceID), byref(eepromID), byref(version),
                         byref(serialNumber), byref(customerID),
                         company, date, productStr, customer, customerStr)
        self.EEPROM_data = {'usbVendorID': usbVendorID.value,
                            'usbProductID': usbProductID.value,
                            'usbDeviceID': usbDeviceID.value,
                            'deviceID': deviceID.value,
                            'eepromID': eepromID.value,
                            'version': version.value,
                            'serialNumber': serialNumber.value,
                            'customerID': customerID.value,
                            'company': company.value,
                            'date': date.value,
                            'productStr': productStr.value,
                            'customer': customer.value,
                            'customerStr': customerStr.value}
        return self.EEPROM_data

    def _get_positioner_properties(self):
        encoderResolution_um = (c_double * 3)()
        driveOrientation = (c_ulong * 3)()
        dllGetProperties(*self.devRec, encoderResolution_um, driveOrientation)
        self.positionerProperties = {'encoderResolution_um': [r for r in encoderResolution_um],
                                     'driveOrientation': [do for do in driveOrientation]}
        return self.positionerProperties

    def _goto_limit(self, axis, direction=0, speed=255):
        dllGotoLimit(*self.devRec, c_ulong(axis), c_ulong(direction), c_ulong(speed))

    def _goto_reference(self, axis, direction=0, speed=255):
        dllGotoReference(*self.devRec, c_ulong(axis), c_ulong(direction), c_ulong(speed))
    
    def _power_off(self):
        dllPowerOff(*self.devRec)
    
    def _power_on(self):
        dllPowerOn(*self.devRec)
    
    def _manual_servo_move(self, speeds=None, directions=None, modes=None,
                           positions=None):
        sp = (c_ulong*3)()
        if speeds is None:
            speeds = [0, 0, 0]
        for i, val in enumerate(speeds):
            sp[i] = int(val)
        ds = (c_ulong*3)()
        if directions is None:
            directions = [0, 0, 0]
        for i, val in enumerate(directions):
            ds[i] = int(val)
        ms = (c_ulong*3)()
        if modes is None:
            modes = [0, 0, 0]
        for i, val in enumerate(modes):
            ms[i] = int(val)
        ps = (c_double*3)()
        if positions is None:
            positions = [0, 0, 0]
        for i, val in enumerate(positions):
            ps[i] = val
        dllManualServoMove(*self.devRec,
                           sp[0], ds[0], ms[0], ps[0],
                           sp[1], ds[1], ms[1], ps[1],
                           sp[2], ds[2], ms[2], ps[2])

    def _open(self):
        dllOpen(*self.devRec)
    
    def _read_pick_encoder(self):
        position = (c_double*3)()
        speed = (c_double*3)()
        refCount = (c_ulong*3)()
        refValid = (c_ulong*3)()
        indexStatus = (c_ulong*3)()
        posError = (c_double*3)()
        enabled = (c_ulong*3)()
        hardLimit = (c_ulong*3)()
        forceThreshold = (c_ulong*3)()
        timeThreshold = (c_ulong*3)()
        autoShutOff = (c_ulong*3)()
        loopCounter = c_ulong()
        dcdcStatus = c_ulong()
        extVoltageStatus = c_ulong()
        dllReadAndPickEncoder(*self.devRec, position, speed, refCount, refValid,
                              indexStatus, posError, enabled, hardLimit,
                              forceThreshold, timeThreshold, autoShutOff,
                              loopCounter, dcdcStatus, extVoltageStatus)
        self.encoder_result = {'position': [p for p in position],
                               'speed': [p for p in speed],
                               'refCount': [p for p in refCount],
                               'refValid': [p for p in refValid],
                               'indexStatus': [p for p in indexStatus],
                               'posError': [p for p in posError],
                               'enabled': [p for p in enabled],
                               'hardLimit': [p for p in hardLimit],
                               'forceThreshold': [p for p in forceThreshold],
                               'timeThreshold': [p for p in timeThreshold],
                               'autoShutOff': [p for p in autoShutOff],
                               'loopCounter': loopCounter.value,
                               'dcdcStatus': dcdcStatus.value,
                               'extVoltageStatus': extVoltageStatus.value}
        return self.encoder_result
    
    def _piezo_stop(self):
        dllPiezoStop(*self.devRec)

    def _set_controller_properties(self, enableds=None, hardLimits=None,
                                   forceThresholds=None, timeThresholds=None,
                                   autoShutOffs=None):
        pos = (c_double*3)()
        speed = (c_double*3)()
        refCount = (c_ulong*3)()
        refValid = (c_ulong*3)()
        indexStatus = (c_ulong*3)()
        posErr = (c_double*3)()
        enabled = (c_ulong*3)(255)
        if enableds:
            for i, val in enumerate(enableds):
                enabled[i] = val
        hardLimit = (c_ulong*3)(0)
        if hardLimits:
            for i, val in enumerate(hardLimits):
                hardLimit[i] = val
        forceThreshold = (c_ulong*3)(3)
        if forceThresholds:
            for i, val in enumerate(forceThresholds):
                forceThreshold[i] = val
        timeThreshold = (c_ulong*3)(5)
        if timeThresholds:
            for i, val in enumerate(timeThresholds):
                timeThreshold[i] = val
        autoShutOff = (c_ulong*3)(1)
        if autoShutOffs:
            for i, val in enumerate(autoShutOffs):
                autoShutOff[i] = val
        loopCounter = c_ulong()
        dcdc = c_ulong()
        extVolt = c_ulong()
        dllSetControllerProp(*self.devRec, pos, speed, refCount, refValid,
                             indexStatus, posErr, enabled, hardLimit,
                             forceThreshold, timeThreshold, autoShutOff,
                             loopCounter, dcdc, extVolt)

    def _set_index(self, x=1, y=1, z=1):
        dllSetIndex(*self.devRec, c_ulong(x), c_ulong(y), c_ulong(z))
    
    def _set_positioner_properties(self, encoderResolution_um=None,
                                   driveOrientation=None):
        if encoderResolution_um is None:
            encoderResolution_um = self.positionerProperties['encoderResolution_um']
        if driveOrientation is None:
            driveOrientation = self.positionerProperties['driveOrientation']
        self.positionerProperties = {'encoderResolution_um': [r for r in encoderResolution_um],
                                     'driveOrientation': [do for do in driveOrientation]}
        res = (c_double * 3)()
        for i, r in enumerate(encoderResolution_um):
            res[i] = r
        drO = (c_ulong * 3)()
        for i, do in enumerate(driveOrientation):
            drO[i] = do
        dllSetProperties(*self.devRec, res, drO)


    def close(self):
        self._piezo_stop()
        self._dcdc_off()
        self._power_off()
        self._close()

    def _move_to_position(self, speeds, directions, modes, positions, wait=False, timeout=10, tolerance=0.1):
        self._piezo_stop()
        if wait:
            hard_limit = self._read_pick_encoder()['hardLimit']
        self._manual_servo_move(speeds, directions, modes, positions)
        if wait:
            for i in range(int(10*timeout)):
                time.sleep(0.1)
                data = self._read_pick_encoder()
                breaking = False
                for j, val in enumerate(data['hardLimit']):
                    if val > hard_limit[j]:
                        breaking = True
                        break
                print(i, breaking, hard_limit, data['hardLimit'])
                if breaking:
                    break
                arrived = True
                for j, val in enumerate(data['posError']):
                    if abs(val) > tolerance and speeds[j] != 0:
                        arrived = False
                print(i, arrived)
                if arrived:
                    break
        
    def move_to_position_async(self, positions, speeds, modes=None,
                               directions=None):
        modes = modes or [1, 1, 1]
        directions = directions or [0, 0, 0]
        self._move_to_position(speeds, directions, modes, positions)
    
    def move_to_position_and_wait(self, positions, speeds, modes=None,
                                  directions=None, timeout=10, tolerance=0.1):
        modes = modes or [1, 1, 1]
        directions = directions or [0, 0, 0]
        self._move_to_position(speeds, directions, modes, positions, True,
                               timeout, tolerance)


    def _setTimeConstant(self, value):
        command = 'set:timeconstant'
        self._set_properties(command, value)

    def _getTimeConstant(self):
        command = 'get:timeconstant'
        return self._set_properties(command).value
    
    def enable_disable_axes(self, enabled):
        self.enabled_axes = enabled
        for i, val in enumerate(enabled):
            if val:
                dllAsyncEnableAx(*self.devRec, c_ulong(i+1))
            else:
                dllAsyncDisableAx(*self.devRec, c_ulong(i+1))

    def get_position(self):
        vals = self._read_pick_encoder()['position']
        return vals


    def get_speeds(self):
        return self._read_pick_encoder()['speed']
    
    def get_ref_valid(self):
        return self._read_pick_encoder()['refValid']


    def findReference(self, force=False, axes=None, velocity=255):
        dllPiezoStop(*self.devRec)
        if not force:
            ref_valid = self.get_ref_valid()
        else:
            ref_valid = [False, False, False]
        if axes is None:
            axes = range(1,4)
        elif isinstance(axes, int):
            axes = [axes]
        for ax in axes:
            if force or not ref_valid[ax-1]:
                self.enabled_axes[ax-1] = True
                self.enable_disable_axes(self.enabled_axes)
                dllGotoLimit(*self.devRec, c_ulong(ax), c_ulong(1),
                            c_ulong(velocity))
                self.enable_disable_axes(self.enabled_axes)
                dllGotoReference(*self.devRec, c_ulong(ax), c_ulong(0),
                                c_ulong(velocity))
        dllPiezoStop(*self.devRec)
        ref_valid = self.get_ref_valid()
        for ax in axes:
            if not ref_valid[ax-1]:
                raise Exception(f'Reference of axis {ax} not found!')
            
            







if __name__ == '__main__':
    wrap = Servo3AxUSB2Wrapper(enableds=[True, True, False])
    # wrap.setTimeConstant(200)
    # wrap.setPositionerProperties((0.02, 0.02, 0.02), (1, 1, 1))
    # print(wrap.get_position())
    # print(wrap.get_ref_valid())
    # wrap.findReference(axes=[1,2], force=True)
    # print(wrap.get_position())
    # set_vals = [1000, 1000, 0]
    # wrap.set_position(set_vals, wait=False)
    print(wrap._get_positioner_properties())
    print(wrap._getTimeConstant())
    wrap.findReference(force=False, axes=[1, 2])
    print(wrap.get_position())
    wrap.move_to_position_async([100, 0, 0], [10, 10, 0])
    wrap.move_to_position_async([100, 0, 0], [10, 10, 0])
    wrap.move_to_position_async([100, 0, 0], [10, 10, 0])
    for i in range(3):
        time.sleep(1)
        print(i, wrap.get_position())
        print(i, wrap.get_position())
        print(i, wrap.get_position())
    wrap.move_to_position_async([200, 100, 0], [10, 10, 0])
    wrap.move_to_position_async([200, 100, 0], [10, 10, 0])
    wrap.move_to_position_async([200, 100, 0], [10, 10, 0])
    for i in range(3):
        time.sleep(1)
        print(i, wrap.get_position())
        print(i, wrap.get_position())
        print(i, wrap.get_position())
    wrap.close()
