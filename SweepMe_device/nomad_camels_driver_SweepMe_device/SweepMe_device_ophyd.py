from typing import Dict, Tuple
import pysweepme
from ophyd import Component as Cpt
from ophyd import Device, Signal, SignalRO
import os
import re


def make_valid_python_identifier(s):
    # Replace invalid characters
    s = re.sub("[^0-9a-zA-Z_]", "_", s)
    # Remove leading characters until we find a letter or underscore
    s = re.sub("^[^a-zA-Z_]+", "", s)
    return s


special_keys = [
    "Label",
    "Port",
    "Device",
    "Channel",
    "SweepMode",
    "SweepValue",
    "Description",
]


def get_driver(path, port=""):
    name = os.path.basename(path)
    folder = os.path.dirname(path)
    driver = pysweepme.get_driver(name, folder, port)
    return driver


def get_ports(driver):
    keys = driver.port_types
    return pysweepme.Ports.get_resources(keys)


def make_ophyd_instance(
    prefix="",
    *args,
    name,
    driver,
    kind=None,
    read_attrs=None,
    configuration_attrs=None,
    parent=None,
    port="",
    **kwargs,
):
    driver_name = os.path.basename(driver)
    class_name = make_valid_python_identifier(f"SweepMe_{driver_name}")
    ophyd_class = make_ophyd_class(driver, class_name)
    kwargs["driver"] = driver
    return ophyd_class(
        prefix,
        *args,
        name=name,
        kind=kind,
        read_attrs=read_attrs,
        configuration_attrs=configuration_attrs,
        parent=parent,
        port=port,
        **kwargs,
    )


def make_ophyd_class(driver_path, class_name):
    driver = get_driver(driver_path)
    configs = driver.set_GUIparameter().keys()
    config_signals = {}
    for config in configs:
        if config in special_keys:
            continue
        name = make_valid_python_identifier(config)
        config_signals[name] = Cpt(
            SweepMe_Parameter_Signal, name=name, parameter_name=config, kind="config"
        )
    set_channels = {}
    if "SweepMode" in configs:
        sweep_modes = configs["SweepMode"]
        for mode in sweep_modes:
            name = make_valid_python_identifier(mode)
            set_channels[name] = Cpt(SweepMe_Signal, name=name, mode_name=mode)
    variables = {}
    for i, var_name in enumerate(driver.variables):
        name = make_valid_python_identifier(var_name)
        variables[name] = Cpt(
            SweepMe_SignalRO,
            name=name,
            variable_name=var_name,
            metadata={"units": driver.units[i]},
        )
    return type(
        make_valid_python_identifier(class_name),
        (SweepMe_Device,),
        {**config_signals, **set_channels, **variables},
    )


class SweepMe_Device(Device):
    def __init__(
        self,
        prefix="",
        *,
        name,
        kind=None,
        read_attrs=None,
        configuration_attrs=None,
        parent=None,
        driver=None,
        port="",
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
        self.driver = get_driver(driver, port)
        self.driver.connect()
        self.driver.initialize()
        self.driver.poweron()
        for component in self.walk_signals():
            if isinstance(
                component.item,
                (SweepMe_Signal, SweepMe_SignalRO, SweepMe_Parameter_Signal),
            ):
                component.item.driver = self.driver

    def configure(self, d):
        ret = super().configure(d)
        self.driver.configure()
        return ret

    def finalize_steps(self):
        self.driver.poweroff()
        self.driver.unconfigure()
        self.driver.deinitialize()
        self.driver.disconnect()
        self.driver.measure()


class SweepMe_Signal(Signal):
    def __init__(self, mode_name, driver=None, **kwargs):
        super().__init__(**kwargs)
        self.mode_name = mode_name
        self.driver = driver

    def put(self, value, *, timestamp=None, force=False, metadata=None, **kwargs):
        if not self.driver:
            raise ValueError(f"Driver not set for signal {self.name}")
        last_mode = self.driver.get_parameters()["SweepMode"]
        if last_mode != self.mode_name:
            self.driver.set_parameters({"SweepMode": self.mode_name})
            self.driver.configure()
        self.driver.write(value)
        super().put(
            value, timestamp=timestamp, force=force, metadata=metadata, **kwargs
        )


class SweepMe_SignalRO(SignalRO):
    def __init__(self, variable_name, driver=None, **kwargs):
        super().__init__(**kwargs)
        self.variable_name = variable_name
        self.data_position = None
        self.driver = driver

    def get(self, **kwargs):
        if not self.driver:
            raise ValueError(f"Driver not set for signal {self.name}")
        if self.data_position is None:
            self.data_position = self.driver.variables.index(self.variable_name)
        data = self.driver.read()
        self._readback = data[self.data_position]
        return super().get(**kwargs)


class SweepMe_Parameter_Signal(Signal):
    def __init__(self, parameter_name, driver=None, **kwargs):
        super().__init__(**kwargs)
        self.parameter_name = parameter_name
        self.driver = driver

    def put(self, value, *, timestamp=None, force=False, metadata=None, **kwargs):
        if not self.driver:
            raise ValueError(f"Driver not set for parameter signal {self.name}")
        self.driver.set_parameters({self.parameter_name: value})
        super().put(
            value, timestamp=timestamp, force=force, metadata=metadata, **kwargs
        )
