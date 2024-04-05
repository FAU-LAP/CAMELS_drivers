from typing import Dict, Tuple
import pysweepme
from ophyd import Component as Cpt
from ophyd import Device, Signal, SignalRO
import os
import re

port_manager = pysweepme.PortManager.PortManager()


def make_valid_python_identifier(s):
    """Returns a valid python identifier for the string "s". This is necessary since the parameters from SweepMe! drivers are handled as strings while they are python variables in the ophyd classes used by NOMAD CAMELS."""
    # Replace invalid characters
    s = re.sub("[^0-9a-zA-Z_]", "_", s)
    # Remove leading characters until we find a letter or underscore
    s = re.sub("^[^a-zA-Z_]+", "", s)
    return s


# those keys have specific meaning in SweepMe! drivers and are not converted to "normal" variables
special_keys = [
    "Label",
    "Port",
    "Device",
    "Channel",
    "SweepMode",
    "SweepValue",
    "Description",
]


def get_driver(path):
    """Returns the SweepMe! driver instance for the driver at the given path."""
    name = os.path.basename(path)
    folder = os.path.dirname(path)
    driver = pysweepme.DeviceManager.get_driver_instance(name=name, folder=folder)
    return driver


def get_ports(driver):
    """Uses SweepMe!'s port manager to get the available ports for the given driver."""
    keys = driver.port_types
    return port_manager.get_resources_available(keys)


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
    """Creates an ophyd instance for the given driver. The driver is used to create the ophyd class using `make_ophyd_class` and the instance is created with the given parameters."""
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
    """Creates an ophyd class for the given driver. The driver's GUI parameters are used to create the configuration signals, the sweep modes are used to create the set channels and the variables are used to create the readback signals. The class is created with the given class name."""
    driver = get_driver(driver_path)
    configs = driver.set_GUIparameter()
    config_signals = {}
    for config in configs.keys():
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
    """This class is a parent for wrappers of SweepMe! drivers. It loads the given `driver` and gives it to all its components. It also initializes the driver and connects to the device. The driver is disconnected and powered off when the device is finalized.

    Parameters
    ----------
    driver : str
        The path to the driver file.
    port : str
        The port the device is connected to.
    """

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
        driver_name = os.path.basename(driver)
        folder = os.path.dirname(driver)
        self.driver = pysweepme.DeviceManager.get_driver_instance(
            name=driver_name, folder=folder
        )
        if name != "test":
            self.driver = pysweepme.DeviceManager.get_driver(
                name=driver_name, folder=folder, port_string=port
            )
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
        """Calls ophyd's parent configure method, then calls configure on the driver to set the parameters."""
        ret = super().configure(d)
        self.driver.configure()
        return ret

    def finalize_steps(self):
        """Powers the device off, unconfigures it, deinitializes it and disconnects it."""
        self.driver.poweroff()
        self.driver.unconfigure()
        self.driver.deinitialize()
        self.driver.disconnect()


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
