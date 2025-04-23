import time

import numpy as np
from scipy.optimize import root
import pandas as pd
import copy

import simple_pid

from ophyd import Device
from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.custom_function_signal import (
    Custom_Function_Signal,
    Custom_Function_SignalRO,
)
from nomad_camels.utility import device_handling

from PySide6.QtCore import QThread, Signal, QTimer


def helper_ptX(x, r, a, b, c):
    return 1 - r + a * x + b * x**2 + c * (x - 100) * x**3


def ptX(rMeas, rX=1000):
    r = rMeas / rX
    a = 3.9083e-3
    b = -5.775e-7
    c = -4.183e-12
    t = 273.15 + (-a + np.sqrt(a**2 - 4 * (1 - r) * b)) / 2 / b
    if t < 273.15:
        zero = root(lambda x: helper_ptX(x, r, a, b, c), -150).x
        return zero[0] + 273.15
    return t


def ptX_inv(T, rX=1000):
    return root(lambda r: ptX(r, rX) - T, 300).x[0]


def pt1000(rMeas):
    return ptX(rMeas)


def pt1000_inv(T):
    return ptX_inv(T)


def pt100(rMeas):
    return ptX(rMeas, rX=100)


def pt100_inv(T):
    return ptX_inv(T, rX=100)


class PID_Controller(Device):
    output_value = Cpt(Custom_Function_SignalRO, value=0.0, name="output_value")
    current_value = Cpt(Custom_Function_SignalRO, value=0.0, name="current_value")
    setpoint = Cpt(Custom_Function_Signal, value=0.0, name="setpoint")
    pid_stable = Cpt(Custom_Function_SignalRO, value=0.0, name="pid_stable")
    pid_on = Cpt(Custom_Function_Signal, value=False, name="pid_on")
    p_value = Cpt(Custom_Function_SignalRO, value=0.0, name="p_value")
    i_value = Cpt(Custom_Function_SignalRO, value=0.0, name="i_value")
    d_value = Cpt(Custom_Function_SignalRO, value=0.0, name="d_value")

    kp = Cpt(Custom_Function_Signal, value=0.0, name="kp", kind="config")
    ki = Cpt(Custom_Function_Signal, value=0.0, name="ki", kind="config")
    kd = Cpt(Custom_Function_Signal, value=0.0, name="kd", kind="config")
    dt = Cpt(Custom_Function_Signal, value=0.0, name="dt", kind="config")
    min_value = Cpt(Custom_Function_Signal, value=0.0, name="min_value", kind="config")
    max_value = Cpt(Custom_Function_Signal, value=0.0, name="max_value", kind="config")

    set_conversion_func = Cpt(
        Custom_Function_Signal, value="", name="set_conversion_func", kind="config"
    )
    read_conversion_func = Cpt(
        Custom_Function_Signal, value="", name="read_conversion_func", kind="config"
    )
    show_plot = Cpt(Custom_Function_Signal, value=True, name="show_plot", kind="config")
    interpolate_auto = Cpt(
        Custom_Function_Signal, value=False, name="interpolate_auto", kind="config"
    )
    pid_val_table = Cpt(
        Custom_Function_Signal, value={}, name="pid_val_table", kind="config"
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
        auto_pid=True,
        bias_signal=None,
        set_signal=None,
        read_signal=None,
        **kwargs
    ):
        pops = [
            "val_choice",
            "val_file",
            "read_signal_name",
            "set_signal_name",
            "bias_signal_name",
        ]
        for p in pops:
            if p in kwargs:
                kwargs.pop(p)
        super().__init__(
            prefix=prefix,
            name=name,
            kind=kind,
            read_attrs=read_attrs,
            configuration_attrs=configuration_attrs,
            parent=parent,
            **kwargs
        )
        if isinstance(read_signal, str):
            read_signal = device_handling.get_channel_from_string(read_signal)
        self.read_signal = read_signal
        if isinstance(set_signal, str):
            set_signal = device_handling.get_channel_from_string(set_signal)
        self.set_signal = set_signal
        if bias_signal == "None":
            bias_signal = None
        if isinstance(bias_signal, str):
            bias_signal = device_handling.get_channel_from_string(bias_signal)

        self.show_plot.put_function = self.change_show_plot

        self.read_conversion_func.put_function = self.update_read_conv_func

        self.set_conversion_func.put_function = self.update_set_conv_func

        self.current_output = 0.0

        if bias_signal:
            self.bias_func = bias_signal.put
        else:
            self.bias_func = None

        self.current_value.read_function = self.current_value_read
        self.output_value.read_function = self.get_output
        self.pid_stable.read_function = self.stable_check
        self.kp.put_function = self.set_Kp
        self.ki.put_function = self.set_Ki
        self.kd.put_function = self.set_Kd
        self.dt.put_function = self.set_dt

        self.p_value.read_function = self.read_p
        self.i_value.read_function = self.read_i
        self.d_value.read_function = self.read_d

        self.min_value.put_function = self.set_minval
        self.max_value.put_function = self.set_maxval
        self.pid_on.put_function = self.set_pid_on
        self.setpoint.put_function = self.update_PID_vals

        self.auto_pid = auto_pid
        self.pid_vals = None
        self.stability_time = np.inf
        self.stability_delta = 0.0
        if name != "test":
            self.pid_thread = PID_Thread(self)
            from nomad_camels.main_classes.plot_pyqtgraph import PlotWidget

            y_axes = {"output": 2, "k": 2, "i": 2, "d": 2}
            self.plot = PlotWidget(
                "time",
                None,
                title="PID plot",
                ylabel="value",
                ylabel2="PID-values",
                y_axes=y_axes,
                first_hidden=list(y_axes.keys()),
                show_plot=False,
                use_bluesky=False,
            )
            # for y in y_axes:
            #     self.plot.plot.current_lines[y].setLinestyle('None')
            self.update_read_conv_func(None)
            self.update_set_conv_func(None)
            self.pid_thread.new_data.connect(self.data_update)
            self.pid_thread.finished.connect(self.plot.close)

    def get_pid_val_table(self):
        pid_val_table = self.pid_val_table.get()
        if pid_val_table is None:
            pid_val_table = {
                "setpoint": [0.0],
                "kp": [0.0],
                "ki": [0.0],
                "kd": [0.0],
                "max_value": [np.inf],
                "min_value": [-np.inf],
                "bias": [0.0],
                "stability-delta": [0.0],
                "stability-time": [0.0],
            }
        elif type(pid_val_table) is str:
            pid_val_table = pd.read_csv(pid_val_table, delimiter="\t")
        elif type(pid_val_table) is pd.DataFrame:
            pid_val_table = pid_val_table.to_dict(orient="list")
        return pid_val_table

    def configure(self, d):
        ret = super().configure(d)
        if not self.pid_thread.isRunning():
            self.pid_thread.start()
        self.update_PID_vals(self.pid_thread.pid.setpoint)
        return ret

    def update_read_conv_func(self, func):
        if not func:
            func = lambda x: x
        elif isinstance(func, str):
            func = globals()[func]

        def read_function():
            x = self.read_signal.get()
            return func(x)

        self.read_function = read_function

    def update_set_conv_func(self, func):
        if not func:
            func = lambda x: x
        elif isinstance(func, str):
            func = globals()[func]

        def set_function(x):
            x = func(x)
            self.set_signal.put(x)
            self.current_output = x

        self.set_function = set_function

    def change_show_plot(self, show):
        self.plot.livePlot.show_plot = show
        QTimer.singleShot(0, lambda: self.plot.setHidden(not show))

    def current_value_read(self):
        return self.pid_thread.current_value

    def data_update(self, timestamp, setpoint, current, output, kid):
        ys = {
            "current value": current,
            "setpoint": setpoint,
            "output": output,
            "k": kid[0],
            "i": kid[1],
            "d": kid[2],
        }
        self.plot.livePlot.add_data(timestamp, ys)

    def stable_check(self):
        return self.pid_thread.stable_time >= self.stability_time

    def get_output(self):
        return self.current_output

    def set_Kp(self, value):
        self.pid_thread.pid.Kp = value

    def set_Ki(self, value):
        self.pid_thread.pid.Ki = value

    def set_Kd(self, value):
        self.pid_thread.pid.Kd = value

    def set_dt(self, value):
        self.pid_thread.pid.sample_time = value
        self.pid_thread.sample_time = value

    def set_minval(self, value):
        maxval = self.max_value.get()
        self.pid_thread.pid.output_limits = (value, maxval)

    def set_maxval(self, value):
        minval = self.min_value.get()
        self.pid_thread.pid.output_limits = (minval, value)

    def read_p(self):
        return float(self.pid_thread.pid.components[0])

    def read_i(self):
        return float(self.pid_thread.pid.components[1])

    def read_d(self):
        return float(self.pid_thread.pid.components[2])

    def set_pid_on(self, value):
        self.pid_thread.pid.set_auto_mode(value)
        self.auto_pid = value
        self.update_PID_vals(self.pid_thread.pid.setpoint, force=True)

    def finalize_steps(self):
        self.pid_thread.still_running = False
        # self.plot.close()

    def update_PID_vals(self, setpoint, force=False):
        if not self.auto_pid:
            if self.bias_func is not None:
                self.bias_func(0)
            self.update_vals_to_thread(setpoint)
            return
        old_vals = copy.deepcopy(self.pid_vals)
        pid_val_table = pd.DataFrame(self.get_pid_val_table())
        setpoints = pid_val_table["setpoint"]
        if setpoint >= max(setpoints):
            self.pid_vals = pid_val_table[setpoints == max(setpoints)].to_dict(
                orient="list"
            )
        elif setpoint <= min(setpoints):
            self.pid_vals = pid_val_table[setpoints == min(setpoints)].to_dict(
                orient="list"
            )
        elif not self.interpolate_auto.get():
            next_lo = max(setpoints[setpoints <= setpoint])
            self.pid_vals = pid_val_table[setpoints == next_lo].to_dict(orient="list")
        else:
            next_lo = max(setpoints[setpoints <= setpoint])
            next_hi = min(setpoints[setpoints > setpoint])
            lo_vals = pid_val_table[setpoints == next_lo].to_dict(orient="list")
            hi_vals = pid_val_table[setpoints == next_hi].to_dict(orient="list")
            self.pid_vals = {}
            for key, lo_val in lo_vals.items():
                self.pid_vals[key] = [
                    lo_val[0]
                    + (hi_vals[key][0] - lo_val[0])
                    * (setpoint - next_lo)
                    / (next_hi - next_lo)
                ]
        if old_vals != self.pid_vals or force:
            for key in self.pid_vals:
                if key in ["setpoint", "stability-time", "stability-delta"] or (
                    key == "bias" and self.bias_func is None
                ):
                    continue
                elif key == "bias":
                    self.bias_func(self.pid_vals[key][0])
                else:
                    att = getattr(self, key)
                    att.put(self.pid_vals[key][0])
        self.stability_time = self.pid_vals["stability-time"][0]
        self.stability_delta = self.pid_vals["stability-delta"][0]
        self.update_vals_to_thread(setpoint)

    def update_vals_to_thread(self, setpoint):
        self.pid_thread.stability_delta = self.pid_vals["stability-delta"][0]
        # self.setpoint = setpoint
        self.pid_thread.pid.setpoint = setpoint
        self.pid_thread.stable_time = 0

    def update_pid_settings(self):
        self.update_PID_vals(self.pid_thread.pid.setpoint)


class PID_Thread(QThread):
    new_data = Signal(float, float, float, float, tuple)

    def __init__(
        self,
        pid_device,
        Kp=1.0,
        Ki=1.0,
        Kd=1.0,
        setpoint=0,
        sample_time=1,
        output_limits=(None, None),
        auto_mode=False,
        proportional_on_measurement=False,
        error_map=None,
        **kwargs
    ):
        super().__init__()
        self.pid = simple_pid.PID(
            Kp=Kp,
            Ki=Ki,
            Kd=Kd,
            setpoint=setpoint,
            sample_time=sample_time,
            output_limits=output_limits,
            auto_mode=auto_mode,
            proportional_on_measurement=proportional_on_measurement,
            error_map=error_map,
        )
        self.device = pid_device
        self.sample_time = sample_time
        self.stable_time = 0
        self.stability_delta = 0
        self.last = None
        self.starttime = 0
        self.current_value = 0.0
        self.still_running = True
        self.last_I = 0.0
        self.last_output = 0.0

    def run(self):
        self.starttime = time.monotonic()
        self.last = time.monotonic() - self.sample_time
        while self.still_running:
            self.pid_step()

    def pid_step(self):
        now = time.monotonic()
        dis = now - self.last
        if dis < self.sample_time:
            time.sleep(self.sample_time - dis)
            return
        self.current_value = self.device.read_function()
        if np.isnan(self.current_value):
            new_output = 0.0
        elif self.pid.auto_mode:
            new_output = self.pid(self.current_value)
        else:
            new_output = 0.0
        if new_output in self.pid.output_limits:
            self.pid._integral = self.last_I
        if np.isnan(new_output):
            new_output = self.last_output
        self.last_output = new_output
        self.last_I = self.pid._integral
        self.last = time.monotonic()
        if new_output is not None:
            self.device.set_function(new_output)
        if np.abs(self.pid.setpoint - self.current_value) <= self.stability_delta:
            self.stable_time += dis
        else:
            self.stable_time = 0.0
        self.new_data.emit(
            self.last - self.starttime,
            self.pid.setpoint,
            self.current_value,
            new_output or 0.0,
            self.pid.components,
        )
