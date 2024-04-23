import pymeasure.instruments
import re
import importlib
import inspect
import ast
import pathlib
from ophyd import Signal, SignalRO, Device, Component as Cpt

arg_order = [
    "get_command",
    "set_command",
    "docs",
    "validator",
    "values",
    "map_values",
    "get_process",
    "set_process",
    "command_process",
    "check_set_errors",
    "check_get_errors",
    "dynamic",
    "preprocess_reply",
    "separator",
    "maxsplit",
    "cast",
    "values_kwargs",
]

validators = [
    "strict_range",
    "strict_discrete_range",
    "strict_discrete_set",
    "truncated_range",
    "modular_range",
    "modular_range_bidirectional",
    "truncated_discrete_set",
]


def eval_node(node, driver=None):
    if isinstance(node, ast.Name):
        if node.id in validators:
            return node.id
        # if node is joined validators, check arguments of function call
        elif node.id == "joined_validators":
            last_name = ""
            for arg in node.args:
                last_name = arg.id
                if arg.id in validators and "discrete_set" in last_name:
                    break
            return last_name
        elif driver and hasattr(driver, node.id):
            return getattr(driver, node.id)
    try:
        return ast.literal_eval(node)
    except ValueError:
        return str(node)


def get_args_and_kwargs(node, driver=None):
    args = [eval_node(arg, driver) for arg in node.args]
    kwargs = {kw.arg: eval_node(kw.value, driver) for kw in node.keywords}
    return args, kwargs


def get_control_infos(args, kwargs):
    for i, arg in enumerate(args):
        kwargs[arg_order[i]] = arg
    discrete = "validator" in kwargs and "discrete_set" in kwargs["validator"]
    boolean = False
    values = None
    if "values" in kwargs:
        try:
            values = list(kwargs["values"])
            if len(values) == 2 and True in values and False in values:
                boolean = True
        except TypeError:
            pass
    return {
        "discrete": discrete,
        "boolean": boolean,
        "values": values,
        "kwargs": kwargs,
    }


def get_classes_from_driver_file(driver):
    file = inspect.getfile(driver)
    # make to usual path
    file = pathlib.Path(file).as_posix()
    # Create a module spec from the file path
    if not "pymeasure/instruments" in file:
        return {}
    module_name = f'pymeasure.instruments.{file.split("pymeasure/instruments/")[1].split(".")[0].replace("/", ".")}'
    module = importlib.import_module(module_name)
    # Get all the classes in the module
    classes = {
        member[0]: [member[1], inspect.getsource(member[1])]
        for member in inspect.getmembers(module, inspect.isclass)
    }
    return classes


def get_driver(manufacturer, instrument):
    module = importlib.import_module(f"pymeasure.instruments.{manufacturer}")
    driver = getattr(module, instrument)
    return driver


def get_driver_information(manufacturer, instrument):
    driver = get_driver(manufacturer, instrument)
    return check_driver_info(driver)


def check_driver_info(driver, source=None):
    source = source or inspect.getsource(driver)
    tree = ast.parse(source)
    # read docstring
    docstring = ast.get_docstring(tree.body[0])

    controls = {}
    measurements = {}
    settings = {}
    channels = {}

    for node in ast.walk(tree):
        # Check if the node is an assignment
        if isinstance(node, ast.Assign):
            # Check if the value being assigned is a call to Instrument.control
            if not (
                isinstance(node.value, ast.Call) and hasattr(node.value.func, "attr")
            ):
                continue
            elif node.value.func.attr == "control":
                args, kwargs = get_args_and_kwargs(node.value, driver)
                info = get_control_infos(args, kwargs)
                controls[node.targets[0].id] = info
            elif node.value.func.attr == "measurement":
                args, kwargs = get_args_and_kwargs(node.value, driver)
                info = get_control_infos(args, kwargs)
                measurements[node.targets[0].id] = info
            elif node.value.func.attr == "setting":
                args, kwargs = get_args_and_kwargs(node.value, driver)
                info = get_control_infos(args, kwargs)
                settings[node.targets[0].id] = info
            elif node.value.func.attr == "ChannelCreator":
                name = node.value.args[0].id
                classes = get_classes_from_driver_file(driver)
                if name in classes:
                    channels[node.targets[0].id] = check_driver_info(*classes[name])
            # TODO support for MultiChannelCreator
    return {
        "controls": controls,
        "measurements": measurements,
        "settings": settings,
        "channels": channels,
        "docstring": docstring,
    }


def make_valid_python_identifier(s):
    """Returns a valid python identifier for the string "s". This is necessary since the parameters from SweepMe! drivers are handled as strings while they are python variables in the ophyd classes used by NOMAD CAMELS."""
    # Replace invalid characters
    s = re.sub("[^0-9a-zA-Z_]", "_", s)
    # Remove leading characters until we find a letter or underscore
    s = re.sub("^[^a-zA-Z_]+", "", s)
    return s


def make_signal_cpt(name, info, is_channel=False, provide_read=False, only_read=False):
    if is_channel:
        kind = "hinted"
    else:
        kind = "config"
    values = None
    if info["discrete"]:
        values = info["values"]
        if info["boolean"]:
            value = False
        else:
            value = info["values"][0]
    else:
        value = 0.0
    signals = {}
    if provide_read and is_channel:
        if only_read:
            signals[name] = Cpt(
                PyMeasureSignalRO, name=name, kind=kind, value=value, property_name=name
            )
        else:
            signals[f"{name}_set"] = Cpt(
                PyMeasureSignal,
                name=f"{name}_set",
                kind=kind,
                value=value,
                values=values,
                property_name=name,
            )
            signals[f"{name}_get"] = Cpt(
                PyMeasureSignal,
                name=f"{name}_get",
                kind=kind,
                value=value,
                values=values,
                property_name=name,
            )
    elif provide_read:
        signals[name] = Cpt(
            PyMeasureSignalRO, name=name, kind=kind, value=value, property_name=name
        )
    else:
        signals[name] = Cpt(
            PyMeasureSignal,
            name=name,
            kind=kind,
            value=value,
            property_name=name,
            values=values,
        )
    return signals


def make_pymeasure_instruments_ophyd_instance(
    prefix="",
    *args,
    name,
    manufacturer,
    instrument,
    measurements,
    settings,
    controls,
    channels,
    config_info,
    kind=None,
    read_attrs=None,
    configuration_attrs=None,
    parent=None,
    resource_name=None,
    **kwargs,
):
    ophyd_class = make_pymeasure_instruments_ophyd_class(
        instrument,
        manufacturer,
        controls,
        measurements,
        settings,
        channels,
        config_info,
    )
    return ophyd_class(
        prefix,
        *args,
        name=name,
        kind=kind,
        parent=parent,
        read_attrs=read_attrs,
        configuration_attrs=configuration_attrs,
        resource_name=resource_name,
        instrument=instrument,
        manufacturer=manufacturer,
        **kwargs,
    )


def make_pymeasure_instruments_ophyd_class(
    instrument, manufacturer, controls, measurements, settings, channels, config_info
):
    if not config_info or not config_info["name"]:
        return
    class_name = f"PyMeasure_{manufacturer}_{instrument}"
    signals = make_signals(controls, measurements, settings, config_info)
    for channel_name, info in channels.items():
        channel_signals = make_signals(
            channel_name,
            manufacturer,
            info["controls"],
            info["measurements"],
            info["settings"],
            info["channels"],
            config_info,
        )
        for name, signal in channel_signals.items():
            signals[f"{channel_name}_{name}"] = signal
    return type(class_name, (PyMeasureDevice,), signals)


def make_signals(controls, measurements, settings, config_info):
    signals = {}
    for name, info in controls.items():
        n = config_info["name"].index(name)
        is_channel = config_info["is channel"][n]
        provide_read = config_info["provide read (if channel)"][n]
        signals.update(
            make_signal_cpt(name, info, is_channel, provide_read, only_read=False)
        )
    for name, info in measurements.items():
        n = config_info["name"].index(name)
        is_channel = config_info["is channel"][n]
        signals.update(
            make_signal_cpt(
                name, info, is_channel=is_channel, provide_read=True, only_read=True
            )
        )
    for name, info in settings.items():
        n = config_info["name"].index(name)
        is_channel = config_info["is channel"][n]
        signals.update(
            make_signal_cpt(
                name, info, is_channel=is_channel, provide_read=False, only_read=False
            )
        )
    return signals


class PyMeasureSignal(Signal):
    def __init__(self, property_name, driver=None, values=None, **kwargs):
        super().__init__(**kwargs)
        self.property_name = property_name
        self.driver = driver
        self.values = values

    def put(self, value, *, timestamp=None, force=False, metadata=None, **kwargs):
        """Sets the SweepMode of the driver to the mode of the signal, then calls `configure` on the driver, before writing the value."""
        if not self.driver:
            raise ValueError(f"Driver not set for signal {self.name}")
        if self.values and value not in self.values:
            try:
                value = type(self.values)(value)
            except ValueError:
                try:
                    value = self.values[value]
                except KeyError:
                    raise ValueError(
                        f"Value {value} of type {type(value)} not supported for {self.name} with values {self.values}"
                    )
        setattr(self.driver, self.property_name, value)
        super().put(
            value, timestamp=timestamp, force=force, metadata=metadata, **kwargs
        )


class PyMeasureSignalRO(SignalRO):
    def __init__(self, property_name, driver=None, **kwargs):
        super().__init__(**kwargs)
        self.property_name = property_name
        self.driver = driver

    def get(self, **kwargs):
        if not self.driver:
            raise ValueError(f"Driver not set for signal {self.name}")
        self._readback = getattr(self.driver, self.property_name)
        return super().get(**kwargs)


class PyMeasureDevice(Device):
    def __init__(
        self,
        prefix="",
        *,
        name,
        kind=None,
        read_attrs=None,
        configuration_attrs=None,
        parent=None,
        resource_name=None,
        instrument=None,
        manufacturer=None,
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
        self.driver = get_driver(manufacturer, instrument)(resource_name)
        # give the driver to all components
        for component in self.walk_signals():
            if isinstance(
                component.item,
                (PyMeasureSignal, PyMeasureSignalRO),
            ):
                component.item.driver = self.driver


if __name__ == "__main__":
    info = get_driver_information("toptica", "IBeamSmart")
    print(info)
