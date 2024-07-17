from ophyd import Component as Cpt

import pylablib as pll
from pylablib.devices import Andor

from nomad_camels.bluesky_handling.custom_function_signal import (
    Custom_Function_Signal,
    Custom_Function_SignalRO,
    Sequential_Device,
)


read_modes = {
    "FVB - full vertical binning": "fvb",
    "multi track": "multi_track",
    "random track": "random_track",
}


def get_cameras():
    cam_list = []
    for i in range(Andor.get_cameras_number_SDK2()):
        cam = Andor.AndorSDK2Camera(idx=i)
        info = cam.get_device_info()
        cam_list.append(
            f"{info.controller_model}, {info.head_model}, {info.serial_number}"
        )
        cam.close()
    return cam_list


class Andor_Newton(Sequential_Device):
    """
    Driver for the Andor Newton CCD camera
    """

    read_camera = Cpt(
        Custom_Function_SignalRO, name="read_camera", metadata={"units": "intensity"}
    )

    get_temperature = Cpt(
        Custom_Function_SignalRO, name="get_temperature", kind="config"
    )
    temperature_status = Cpt(
        Custom_Function_SignalRO, name="temperature_status", kind="config"
    )

    # Configuration settings
    set_temperature = Cpt(Custom_Function_Signal, name="set_temperature", kind="config")
    shutter_mode = Cpt(Custom_Function_Signal, name="shutter_mode", kind="config")
    exposure_time = Cpt(Custom_Function_Signal, name="exposure_time", kind="config")
    readout_mode = Cpt(Custom_Function_Signal, name="readout_mode", kind="config")
    preamp_gain = Cpt(Custom_Function_Signal, name="preamp_gain", kind="config")
    horizontal_binning = Cpt(
        Custom_Function_Signal, name="horizontal_binning", kind="config"
    )
    hs_speed = Cpt(Custom_Function_Signal, name="hs_speed", kind="config")
    vs_speed = Cpt(Custom_Function_Signal, name="vs_speed", kind="config")
    multi_tracks = Cpt(Custom_Function_Signal, name="multi_tracks", kind="config")
    # read_settings = Cpt(Custom_Function_SignalRO, name='read_settings', kind='config')
    shutter_ttl_open = Cpt(
        Custom_Function_Signal, name="shutter_ttl_open", kind="config"
    )

    def __init__(
        self,
        prefix="",
        *,
        name,
        kind=None,
        read_attrs=None,
        configuration_attrs=None,
        parent=None,
        dll_path="",
        camera=0,
        **kwargs,
    ):
        super().__init__(
            prefix=prefix,
            name=name,
            kind=kind,
            read_attrs=read_attrs,
            configuration_attrs=configuration_attrs,
            parent=parent,
            force_sequential=True,
            **kwargs,
        )
        if name == "test":
            return
        pll.par["devices/dlls/andor_sdk2"] = dll_path
        from pylablib.devices import Andor

        if isinstance(camera, int):
            self.camera = Andor.AndorSDK2Camera(idx=camera)
        else:
            index = get_cameras().index(camera)
            self.camera = Andor.AndorSDK2Camera(idx=index)

        self.read_camera.read_function = self.read_camera_function
        self.get_temperature.read_function = self.get_temperature_function
        self.temperature_status.read_function = self.temperature_status_function
        self.set_temperature.put_function = self.set_temperature_function
        self.shutter_mode.put_function = self.shutter_mode_function
        self.shutter_ttl_open.put_function = self.shutter_ttl_open_function
        self.exposure_time.put_function = self.exposure_time_function
        self.readout_mode.put_function = self.readout_mode_function
        self.preamp_gain.put_function = self.preamp_gain_function
        self.horizontal_binning.put_function = self.horizontal_binning_function
        self.hs_speed.put_function = self.hs_speed_function
        self.vs_speed.put_function = self.vs_speed_function
        self.multi_tracks.put_function = self.multi_tracks_function
        amp_modes = self.camera.get_all_amp_modes()
        self.all_vs_speeds = self.camera.get_all_vsspeeds()
        self.all_preamps = {}
        self.all_hs_speeds = {}
        for mode in amp_modes:
            self.all_preamps[mode.preamp_gain] = mode.preamp
            self.all_hs_speeds[mode.hsspeed_MHz] = mode.hsspeed
        # self.read_settings.read_function = lambda: self.camera.get_settings(-10)
        self.sets = self.camera.get_settings(-10)
        self.shutter_ttl_setting = 0

    def finalize_steps(self):
        self.camera.close()

    def read_camera_function(self):
        time = self.exposure_time.get()
        self.readout_mode.put(self.readout_mode.get())
        dat = self.camera.snap(timeout=10 * time)
        if self.readout_mode.get() != "image":
            return dat[0]
        else:
            return dat

    def get_temperature_function(self):
        return self.camera.get_temperature()

    def temperature_status_function(self):
        return self.camera.get_temperature_status()

    def set_temperature_function(self, value):
        self.camera.set_temperature(value, enable_cooler=True)
        self.camera.set_fan_mode("full")

    def shutter_mode_function(self, value):
        self.camera.setup_shutter(value, ttl_mode=self.shutter_ttl_setting)

    def shutter_ttl_open_function(self, value):
        self.shutter_ttl_setting = 1 if value == "high" else 0
        self.shutter_mode_function(self.shutter_mode.get())

    def exposure_time_function(self, value):
        self.camera.set_exposure(value)

    def readout_mode_function(self, value):
        if value in read_modes:
            value = read_modes[value]
        if value == "fvb":
            value = "multi_track"
            self.camera.setup_multi_track_mode(1, 255, 0)
        elif value == "multi_track":
            self.multi_tracks_function(self.multi_tracks.get())
        self.camera.set_read_mode(value)

    def preamp_gain_function(self, value):
        closest = min(self.all_preamps, key=lambda x: abs(x - value))
        self.camera.set_amp_mode(preamp=self.all_preamps[closest])

    def horizontal_binning_function(self, value):
        self.camera.set_roi(hbin=value)

    def hs_speed_function(self, value):
        closest = min(self.all_hs_speeds, key=lambda x: abs(x - value))
        self.camera.set_amp_mode(hsspeed=self.all_hs_speeds[closest])

    def vs_speed_function(self, value):
        closest = min(self.all_vs_speeds, key=lambda x: abs(x - value))
        index = self.all_vs_speeds.index(closest)
        self.camera.set_vsspeed(index)

    def multi_tracks_function(self, track_data):
        try:
            width = track_data["End"][0] - track_data["Start"][0]
            offset = track_data["Start"][0] - 128 + int(width / 2)
            n = len(track_data["Start"])
        except Exception as e:
            n = 1
            width = 255
            offset = 0
            print(e)
            print("Failed to setup multi track, using FVB settings")
        self.camera.setup_multi_track_mode(n, width, offset)
