from ophyd import Component as Cpt
import numpy as np

from nomad_camels.bluesky_handling.custom_function_signal import (
    Custom_Function_Signal,
    Custom_Function_SignalRO,
    Sequential_Device,
)


def make_ophyd_instance_labview_cryo(
    prefix="",
    *args,
    name,
    kind=None,
    read_attrs=None,
    configuration_attrs=None,
    parent=None,
    # These are the arguments you want to pass to the ophyd class
    # These are the settings you defined in the .py file
    # We will pass the number of channels we selected in the drop down and are defined in the .py file
    file_name="",
    delimiter=",",
    variables=None,
    **kwargs,
):
    ophyd_class = make_ophyd_class(variables)
    return ophyd_class(
        prefix,
        *args,
        name=name,
        kind=kind,
        read_attrs=read_attrs,
        configuration_attrs=configuration_attrs,
        parent=parent,
        file_name=file_name,
        delimiter=delimiter,
        n_variables=len(variables),
        **kwargs,
    )


def read_function_generator(index):
    def read_function(_self_instance):
        return lambda: _self_instance.get_data(index)

    return read_function


def _trigger_function(_self_instance):
    return lambda: _self_instance._read_file()


def make_ophyd_class(variables):
    signal_dict = {}
    for i, variable in enumerate(variables):
        signal_dict[variable] = Cpt(
            Custom_Function_SignalRO,
            name=variable,
            read_function=read_function_generator(i),
            trigger_function=_trigger_function,
        )
    return type("Labview_Cryo_Ophyd", (Labview_Cryo,), {**signal_dict})


class Labview_Cryo(Sequential_Device):
    """
    This class is used to control the LabVIEW Cryo system.
    It reads the file coming from the LabVIEW code.
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
        file_name="",
        delimiter=",",
        n_variables=0,
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
        self.file_name = file_name
        self.delimiter = delimiter.encode().decode("unicode_escape")
        self._was_triggered = False
        self.n_variables = n_variables
        self.newest_data = [np.nan] * n_variables

    def _read_file(self):
        """
        This function reads the file from the LabVIEW Cryo system.
        It is called by the Custom_Function_Signal when the signal is read.
        """
        if self._was_triggered:
            return
        self._was_triggered = True
        for i in range(3):
            try:
                with open(self.file_name, "r") as file:
                    lines = file.readlines()
                newest_data = lines[-1].strip().split(self.delimiter)
                if len(newest_data) != self.n_variables:
                    raise ValueError(
                        f"Expected {self.n_variables} variables, but got {len(newest_data)}"
                    )
                newest_data = [float(x) for x in newest_data]
                self.newest_data = np.array(newest_data)
                break
            except:
                self.newest_data = [np.nan] * self.n_variables
                # If the file is not found or cannot be read, we wait and try again
                if i == 2:
                    raise Exception(
                        f"Could not read the file {self.file_name} after 3 attempts."
                    )
                import time

                time.sleep(0.1)

    def get_data(self, index=0):
        self._was_triggered = False
        return self.newest_data[index]
