import pymeasure.instruments
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


def get_driver_information(manufacturer, instrument):
    module = importlib.import_module(f"pymeasure.instruments.{manufacturer}")
    driver = getattr(module, instrument)
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


class PyMeasureSignal(Signal):
    pass


class PyMeasureSignalRO(SignalRO):
    pass


class PyMeasureDevice(Device):
    pass


if __name__ == "__main__":
    info = get_driver_information("toptica", "IBeamSmart")
    print(info)
