from ophyd import Component as Cpt
import pylablib as pll

from nomad_camels.bluesky_handling.custom_function_signal import (
    Custom_Function_Signal,
    Custom_Function_SignalRO,
    Sequential_Device,
)


class Andor_Shamrock_500(Sequential_Device):
    """
    Driver for the Andor Shamrock 500 spectrometer (not the camera!).
    The camera is implemented separately.
    """

    spectrum = Cpt(Custom_Function_SignalRO, name="spectrum")
    wavelength = Cpt(
        Custom_Function_SignalRO, name="wavelength", metadata={"units": "nm"}
    )

    set_grating_number = Cpt(
        Custom_Function_Signal, name="set_grating_number", kind="config"
    )
    center_wavelength = Cpt(
        Custom_Function_Signal, name="center_wavelength", kind="config"
    )
    input_port = Cpt(Custom_Function_Signal, name="input_port", kind="config")
    output_port = Cpt(Custom_Function_Signal, name="output_port", kind="config")
    camera = Cpt(Custom_Function_Signal, name="camera", kind="config")
    input_slit_size = Cpt(Custom_Function_Signal, name="input_slit_size", kind="config")
    output_slit_size = Cpt(
        Custom_Function_Signal, name="output_slit_size", kind="config"
    )
    horizontal_cam_flip = Cpt(
        Custom_Function_Signal, name="horizontal_cam_flip", kind="config"
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
        spectrometer="",
        dll_path="",
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
        pll.par["devices/dlls/andor_shamrock"] = dll_path
        from pylablib.devices import Andor

        specs = Andor.list_shamrock_spectrographs()
        try:
            spec = specs.index(spectrometer)
            self.spectrometer = Andor.ShamrockSpectrograph(idx=spec)
        except:
            self.spectrometer = Andor.ShamrockSpectrograph(idx=0)

        self.set_grating_number.put_function = self.set_grating_number_function
        self.center_wavelength.put_function = self.center_wavelength_function
        self.input_port.put_function = self.input_port_function
        self.output_port.put_function = self.output_port_function
        self.camera.put_function = self.camera_function
        self.input_slit_size.put_function = self.input_slit_size_function
        self.output_slit_size.put_function = self.output_slit_size_function
        self.spectrum.read_function = self.read_spectrum
        self.wavelength.read_function = self.get_wavelengths
        self.horizontal_cam_flip.put_function = self.horizontal_cam_flip_function
        self.flip_horizontal = False

    def finalize_steps(self):
        self.spectrometer.close()

    def set_grating_number_function(self, value):
        self.spectrometer.set_grating(value)

    def center_wavelength_function(self, value):
        self.spectrometer.set_wavelength(value * 1e-9)

    def input_port_function(self, value):
        if not self.spectrometer.is_flipper_present("input"):
            return
        self.spectrometer.set_flipper_port("input", value)
        self.input_slit_size_function(self.input_slit_size.get())

    def output_port_function(self, value):
        if not self.spectrometer.is_flipper_present("output"):
            return
        self.spectrometer.set_flipper_port("output", value)
        self.output_port._readback = value
        self.output_slit_size_function(self.output_slit_size.get())

    def camera_function(self, value):
        if isinstance(value, str):
            from nomad_camels.utility import device_handling

            cam = device_handling.running_devices[value].camera
        else:
            cam = value.camera
        self.spectrometer.setup_pixels_from_camera(cam)

    def input_slit_size_function(self, value):
        if not self.spectrometer.is_flipper_present("input"):
            pos = "direct"
            if not self.spectrometer.is_slit_present(f"input_{pos}"):
                pos = "side"
        else:
            pos = self.input_port.get()
        if not self.spectrometer.is_slit_present(f"input_{pos}"):
            return
        self.spectrometer.set_slit_width(f"input_{pos}", value * 1e-6)

    def output_slit_size_function(self, value):
        if not self.spectrometer.is_flipper_present("output"):
            pos = "direct"
        else:
            pos = self.output_port.get()
        if not self.spectrometer.is_slit_present(f"output_{pos}"):
            return
        self.spectrometer.set_slit_width(f"output_{pos}", value * 1e-6)

    def get_wavelengths(self):
        self.spectrometer.setup_pixels_from_camera(self.get_camera_device().camera)
        cal = self.spectrometer.get_calibration()
        return cal * 1e9

    def read_spectrum(self):
        cam = self.get_camera_device()
        spec = cam.read_camera.get()
        if not self.flip_horizontal:
            return spec
        # if dimension of spec is 2, flip the first dimension, if it is 1, just flip the array
        if spec.ndim == 2:
            return spec[:, ::-1]
        else:
            return spec[::-1]

    def get_camera_device(self):
        cam = self.camera.get()
        if isinstance(cam, str):
            from nomad_camels.utility import device_handling

            cam = device_handling.running_devices[cam]
        return cam

    def horizontal_cam_flip_function(self, value):
        self.flip_horizontal = value
