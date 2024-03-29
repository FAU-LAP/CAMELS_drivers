from nomad_camels_driver_thorlabs_TLPM.thorlabs_TLPM_ophyd import Thorlabs_TLPM
from nomad_camels.main_classes import device_class

try:
    from .TLPM import TLPM
except ModuleNotFoundError as e:
    import os
    import warnings

    warnings.warn(
        f'It seems you have not installed the Thorlabs support for TLPM!\nMake sure it is installed, if it is not working, copy the files "TLPM.py" and "TLPM_64.dll" to {os.path.dirname(__file__)}\n\n{e}"'
    )
from ctypes import c_uint32, byref, create_string_buffer, c_char_p, c_int


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="thorlabs_TLPM",
            virtual=False,
            tags=["Rotation Stage"],
            ophyd_device=Thorlabs_TLPM,
            ophyd_class_name="Thorlabs_TLPM",
            **kwargs,
        )
        self.settings["resource"] = ""
        self.config["wavelength"] = 532


class subclass_config(device_class.Simple_Config):
    def __init__(
        self,
        parent=None,
        data="",
        settings_dict=None,
        config_dict=None,
        additional_info=None,
    ):
        availables = []
        try:
            tlpm = TLPM()
            deviceCount = c_uint32()
            tlpm.findRsrc(byref(deviceCount))
            resourceName = create_string_buffer(1024)
            for i in range(0, deviceCount.value):
                tlpm.getRsrcName(c_int(i), resourceName)
                availables.append(c_char_p(resourceName.raw).value.decode())
            tlpm.close()
        except NameError as e:
            import warnings

            warnings.warn(e)
        comboboxes = {"resource": availables}
        super().__init__(
            parent,
            "Thorlabs TLPM",
            data,
            settings_dict,
            config_dict,
            additional_info,
            comboBoxes=comboboxes,
        )
        self.load_settings()
