from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.custom_function_signal import (
    Custom_Function_Signal,
    Custom_Function_SignalRO,
)
from ophyd import Device
import pysmu
import numpy as np


class Adalm1000(Device):
    read_current_A = Cpt(
        Custom_Function_SignalRO,
        name="read_current",
        metadata={"units": "A", "description": ""},
    )
    read_voltage_A = Cpt(
        Custom_Function_SignalRO,
        name="read_voltage",
        metadata={"units": "V", "description": ""},
    )
    set_voltage_A = Cpt(
        Custom_Function_Signal,
        name="set_voltage",
        metadata={"units": "V", "description": ""},
    )
    set_current_A = Cpt(
        Custom_Function_Signal,
        name="set_current",
        metadata={"units": "", "description": ""},
    )
    read_current_B = Cpt(
        Custom_Function_SignalRO,
        name="read_current",
        metadata={"units": "A", "description": ""},
    )
    read_voltage_B = Cpt(
        Custom_Function_SignalRO,
        name="read_voltage",
        metadata={"units": "V", "description": ""},
    )
    set_voltage_B = Cpt(
        Custom_Function_Signal,
        name="set_voltage",
        metadata={"units": "V", "description": ""},
    )
    set_current_B = Cpt(
        Custom_Function_Signal,
        name="set_current",
        metadata={"units": "", "description": ""},
    )
    n_samples = Cpt(
        Custom_Function_Signal,
        name="n_samples",
        kind="config",
        metadata={"units": "", "description": ""},
    )
    device_number = Cpt(
        Custom_Function_Signal,
        name="device_number",
        kind="config",
        metadata={"units": "", "description": ""},
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
        **kwargs,
    ):
        super().__init__(
            prefix=prefix,
            name=name,
            kind=kind,
            read_attrs=read_attrs,
            configuration_attrs=configuration_attrs,
            parent=parent,
            **kwargs,
        )
        if name == "test":
            return
        # Connect and setup the ADALM1000
        self.session = pysmu.Session()
        self.device = self.session.devices[0]
        self.channel_A = self.device.channels["A"]
        self.channel_B = self.device.channels["B"]
        self.mode_A = None
        self.mode_B = None
        self.device.ignore_dataflow = False

        # Flush the channels
        self.channel_A.flush()
        self.channel_B.flush()

        self.read_current_A.read_function = self.read_current_A_read_function
        self.read_voltage_A.read_function = self.read_voltage_A_read_function
        self.set_voltage_A.put_function = self.set_voltage_A_put_function
        self.set_current_A.put_function = self.set_current_A_put_function

        self.read_current_B.read_function = self.read_current_B_read_function
        self.read_voltage_B.read_function = self.read_voltage_B_read_function
        self.set_voltage_B.put_function = self.set_voltage_B_put_function
        self.set_current_B.put_function = self.set_current_B_put_function

    def read_current_A_read_function(self):
        data = self.channel_A.get_samples(self.n_samples.get())
        # Convert the data to a NumPy array
        data_np = np.array(data)
        current_A = data_np[:, 1].mean()

        return current_A

    def read_voltage_A_read_function(self):
        data = self.channel_A.get_samples(self.n_samples.get())
        # Convert the data to a NumPy array
        data_np = np.array(data)
        voltage_A = data_np[:, 0].mean()

        return voltage_A

    def set_voltage_A_put_function(self, value):
        self.channel_A.flush()
        if self.mode_A != "SVMI":
            self.channel_A.mode = pysmu.Mode.SVMI
            self.mode_A = "SVMI"
        self.channel_A.write([value] * self.n_samples.get())

    # def set_voltage_A_read_function(self):
    #     return 10

    def set_current_A_put_function(self, value):
        self.channel_A.flush()
        if self.mode_A != "SIMV":
            self.channel_A.mode = pysmu.Mode.SIMV
            self.mode_A = "SIMV"
        self.channel_A.write([value] * self.n_samples.get())

    def read_current_B_read_function(self):
        data = self.channel_B.get_samples(self.n_samples.get())
        # Convert the data to a NumPy array
        data_np = np.array(data)
        current_B = data_np[:, 1].mean()

        return current_B

    def read_voltage_B_read_function(self):
        data = self.channel_B.get_samples(self.n_samples.get())
        # Convert the data to a NumPy array
        data_np = np.array(data)
        voltage_B = data_np[:, 0].mean()

        return voltage_B

    def set_voltage_B_put_function(self, value):
        self.channel_B.flush()
        if self.mode_B != "SVMI":
            self.channel_B.mode = pysmu.Mode.SVMI
            self.mode_B = "SVMI"
        self.channel_B.write([value] * self.n_samples.get())

    def set_current_B_put_function(self, value):
        self.channel_B.flush()
        if self.mode_B != "SIMV":
            self.channel_B.mode = pysmu.Mode.SIMV
            self.mode_B = "SIMV"
        self.channel_B.write([value] * self.n_samples.get())

    def finalize_steps(self):
        self.session.end()
        self.session._close()
