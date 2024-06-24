from typing import Dict, Tuple
import pysweepme
from ophyd import Component as Cpt
from ophyd import Device, Signal, SignalRO
import os
import re

port_manager = None


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
    global port_manager
    if port_manager is None:
        port_manager = pysweepme.PortManager.PortManager()
    return port_manager.get_resources_available(keys)


def make_SweepMe_ophyd_instance(
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
    """Creates an ophyd instance for the given driver. The driver is used to create the ophyd class using `make_SweepMe_ophyd_class` and the instance is created with the given parameters.

    Parameters
    ----------
    driver : str
        The path to the SweepMe! driver
    port : str
        The port the device is connected to. This is handled by SweepMe's port manager
    """
    driver_name = os.path.basename(driver)
    class_name = make_valid_python_identifier(f"SweepMe_{driver_name}")
    ophyd_class = make_SweepMe_ophyd_class(driver, class_name)
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


def make_SweepMe_ophyd_class(driver_path, class_name, GUI_config=None):
    """Creates an ophyd class for the given driver. The driver's GUI parameters are used to create the configuration signals, the sweep modes are used to create the set channels and the variables are used to create the readback signals. The class is created with the given class name."""
    driver = get_driver(driver_path)
    configs = driver.set_GUIparameter()

    # Creates a new dictionary with all the keys of set_GUIparameter, parameters not in GUI_config are set to None
    # Executes get_GUIparameter with the new dictionary. This populates the self.variables of many instruments. Otherwise most channels are missing.
    if GUI_config:
        new_config = {key: GUI_config.get(key, None) for key in configs.keys()}
        driver.get_GUIparameter(new_config)

    # create the signals for the driver's parameters
    config_signals = {}
    for config in configs.keys():
        if config in special_keys:
            continue
        name = make_valid_python_identifier(config)
        config_signals[name] = Cpt(
            SweepMe_Parameter_Signal, name=name, parameter_name=config, kind="config"
        )
    # create the signals for the sweep modes
    set_channels = {}
    if "SweepMode" in configs:
        sweep_modes = configs["SweepMode"]
        for mode in sweep_modes:
            # make one signal for each channel
            if "Channel" in configs:
                for channel in configs["Channel"]:
                    name = make_valid_python_identifier(f"set_{mode}_{channel}")
                    set_channels[name] = Cpt(
                        SweepMe_Signal, name=name, mode_name=mode, channel=channel
                    )
            else:
                name = make_valid_python_identifier(f"set_{mode}")
                set_channels[name] = Cpt(SweepMe_Signal, name=name, mode_name=mode)
    # create the signals for the variables
    variables = {}
    for i, var_name in enumerate(driver.variables):
        # make one signal for each channel
        if "Channel" in configs:
            for channel in configs["Channel"]:
                name = make_valid_python_identifier(f"read_{var_name}_{channel}")
                variables[name] = Cpt(
                    SweepMe_SignalRO,
                    name=name,
                    variable_name=var_name,
                    metadata={"units": driver.units[i]},
                    channel=channel,
                )
        else:
            name = make_valid_python_identifier(f"read_{var_name}")
            variables[name] = Cpt(
                SweepMe_SignalRO,
                name=name,
                variable_name=var_name,
                metadata={"units": driver.units[i]},
            )
    # create a class inheriting from SweepMe_Device with the signals created above
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
            # do SweeMe! initialization
            self.driver.connect()
            self.driver.initialize()
            self.driver.poweron()
        # give the driver to all components
        for component in self.walk_signals():
            if isinstance(
                component.item,
                (SweepMe_Signal, SweepMe_SignalRO, SweepMe_Parameter_Signal),
            ):
                component.item.driver = self.driver

    def configure(self, d):
        """Calls ophyd's parent configure method, then calls configure on the driver to actually set the parameters."""
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
    """This class is a wrapper to make SweepMe!'s SweepMode a settable signal. It sets the SweepMode of the driver to the mode of the signal before writing the value. The driver is given to the signal when it is created, but can also be changed later.

    Parameters
    ----------
    mode_name : str
        The name of the SweepMode to set.
    driver : pysweepme.Driver
        The driver to use for communication.
    """

    def __init__(self, mode_name, driver=None, channel=None, **kwargs):
        super().__init__(**kwargs)
        self.mode_name = mode_name
        self.driver = driver
        self.channel = channel

    def put(self, value, *, timestamp=None, force=False, metadata=None, **kwargs):
        """Sets the SweepMode of the driver to the mode of the signal, then calls `configure` on the driver, before writing the value."""
        if not self.driver:
            raise ValueError(f"Driver not set for signal {self.name}")
        last_mode = self.driver.get_parameters()["SweepMode"]
        if last_mode != self.mode_name or not self.check_last_channel():
            if self.channel:
                self.driver.set_parameters(
                    {"SweepMode": self.mode_name, "Channel": self.channel}
                )
            else:
                self.driver.set_parameters({"SweepMode": self.mode_name})
            self.driver.configure()
        self.driver.write(value)
        super().put(
            value, timestamp=timestamp, force=force, metadata=metadata, **kwargs
        )

    def check_last_channel(self):
        """Checks if the driver's last channel is the same as the one of the signal."""
        if not self.driver:
            raise ValueError(f"Driver not set for signal {self.name}")
        if not self.channel:
            return True
        last_channel = self.driver.get_parameters()["Channel"]
        if last_channel != self.channel:
            return False
        return True


class SweepMe_SignalRO(SignalRO):
    """This class is a wrapper to make SweepMe!'s variables readable. It reads the value from the driver when the signal is read. The driver is given to the signal when it is created, but can also be changed later.

    Parameters
    ----------
    variable_name : str
        The name of the variable to read. It is used to get the position of the variable in the driver's variables list.
    driver : pysweepme.Driver
        The driver to use for communication.
    """

    def __init__(self, variable_name, driver=None, channel=None, **kwargs):
        super().__init__(**kwargs)
        self.variable_name = variable_name
        self.data_position = None
        self.driver = driver
        self.channel = channel

    def get(self, **kwargs):
        """Reads the value from the driver and returns it."""
        if not self.driver:
            raise ValueError(f"Driver not set for signal {self.name}")
        if not self.check_last_channel():
            self.driver.set_parameters({"Channel": self.channel})
            self.driver.configure()
        if self.data_position is None:
            self.data_position = self.driver.variables.index(self.variable_name)
        data = self.driver.read()
        self._readback = data[self.data_position]
        return super().get(**kwargs)

    def check_last_channel(self):
        """Checks if the driver's last channel is the same as the one of the signal."""
        if not self.driver:
            raise ValueError(f"Driver not set for signal {self.name}")
        if not self.channel:
            return True
        last_channel = self.driver.get_parameters()["Channel"]
        if last_channel != self.channel:
            return False
        return True


class SweepMe_Parameter_Signal(Signal):
    """This class is a wrapper to make SweepMe!'s parameters settable. It sets the parameter of the driver to the value of the signal before writing the value. The driver is given to the signal when it is created, but can also be changed later."""

    def __init__(self, parameter_name, driver=None, **kwargs):
        super().__init__(**kwargs)
        self.parameter_name = parameter_name
        self.driver = driver

    def put(self, value, *, timestamp=None, force=False, metadata=None, **kwargs):
        """Sets the parameter of the driver to the value of the signal. It does not call `configure`, since this is done by the SweepMe_Device or when changing the SweepMode."""
        if not self.driver:
            raise ValueError(f"Driver not set for parameter signal {self.name}")
        self.driver.set_parameters({self.parameter_name: value})
        super().put(
            value, timestamp=timestamp, force=force, metadata=metadata, **kwargs
        )
