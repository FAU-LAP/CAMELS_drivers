from ophyd import Component as Cpt
from ophyd import Device

from nomad_camels.bluesky_handling.custom_function_signal import (
    Custom_Function_Signal,
    Custom_Function_SignalRO,
)

from pipython import GCSDevice, pitools


def get_available_stages():
    availables = []
    with GCSDevice() as pidevice:
        availables += pidevice.EnumerateUSB(mask="E-709")
        availables += pidevice.EnumerateTCPIPDevices(mask="E-709")
    return availables


class PI_E709(Device):
    position_set = Cpt(Custom_Function_Signal, name="position_set")
    position_get = Cpt(Custom_Function_SignalRO, name="position_get")
    servo_on = Cpt(Custom_Function_Signal, name="servo_on", kind="config")
    max_pos = Cpt(Custom_Function_SignalRO, name="max_pos", kind="config")
    min_pos = Cpt(Custom_Function_SignalRO, name="min_pos", kind="config")

    def __init__(
        self,
        prefix="",
        *,
        name,
        kind=None,
        read_attrs=None,
        configuration_attrs=None,
        parent=None,
        resource="",
        autozero_on_start=True,
        **kwargs
    ):
        super().__init__(
            prefix=prefix,
            name=name,
            kind=kind,
            read_attrs=read_attrs,
            configuration_attrs=configuration_attrs,
            parent=parent,
            **kwargs
        )
        if name == "test":
            return
        self.pidevice = GCSDevice()
        try:
            self.pidevice.ConnectUSB(resource)
        except:
            self.pidevice.ConnectTCPIPByDescription(resource)
        print("connected: {}".format(self.pidevice.qIDN().strip()))
        if autozero_on_start:
            self.find_reference()

        self.position_set.put_function = self.set_pos
        self.position_get.read_function = self.get_pos
        self.servo_on.put_function = self.set_servo
        self.max_pos.read_function = lambda: pitools.getmaxtravelrange(
            self.pidevice, "Z"
        )["Z"]
        self.min_pos.read_function = lambda: pitools.getmintravelrange(
            self.pidevice, "Z"
        )["Z"]

    def find_reference(self):
        self.pidevice.ATZ()
        pitools.waitonautozero(self.pidevice)

    def set_servo(self, value):
        pitools.setservo(self.pidevice, "Z", value)

    def get_pos(self):
        return self.pidevice.gcscommands.qPOS()["Z"]

    def set_pos(self, value):
        minpos = self.min_pos.get()
        maxpos = self.max_pos.get()
        if value < minpos:
            value = minpos
        elif value > maxpos:
            value = maxpos
        pitools.moveandwait(self.pidevice, "Z", float(value))

    def finalize_steps(self):
        self.pidevice.close()


if __name__ == "__main__":
    stage = PI_E709(name="stage")
