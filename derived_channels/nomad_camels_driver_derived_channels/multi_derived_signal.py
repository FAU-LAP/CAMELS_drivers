from ophyd import Signal, SignalRO, PseudoPositioner
from nomad_camels.utility.device_handling import get_channel_from_string
from nomad_camels.utility import variables_handling
from nomad_camels.bluesky_handling.evaluation_helper import Evaluator


class MultiDerivedSignal(Signal):
    """
    A signal that can be derived from multiple sources.
    This class extends the DerivedSignal to allow for multiple input signals.
    """

    def __init__(
        self,
        derived_from,
        *,
        write_access=False,
        name=None,
        parent=None,
        read_formula=None,
        write_formula=None,
        conversion_type="Simple Function",
        conversion_file="",
        **kwargs,
    ):
        if not isinstance(derived_from, list):
            derived_from = [derived_from]
        if write_access and len(derived_from) > 1:
            raise ValueError(
                "write_access is not supported for signals derived from multiple signals."
            )
        super().__init__(
            name=name,
            parent=parent,
            **kwargs,
        )
        self.derived_from = derived_from.copy()
        self._is_connected = False
        self.eva = Evaluator()
        self._read_formula = read_formula
        self._write_formula = write_formula
        self._conversion_type = conversion_type
        self._conversion_file = conversion_file
        self._conversion_function = None
        if self._conversion_type == "From File":
            if not self._conversion_file:
                raise ValueError("No conversion file provided conversion with file.")
            import importlib.util
            import os

            # import the function from the file
            name = os.path.basename(self._conversion_file)[:-3]
            spec = importlib.util.spec_from_file_location(name, self._conversion_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if write_access:
                self._conversion_function = getattr(module, self._write_formula)
            else:
                self._conversion_function = getattr(module, self._read_formula)

    def _connect(self):
        for i, signal in enumerate(self.derived_from):
            if isinstance(signal, str):
                channel = variables_handling.channels[signal]
                bluesky_name = channel.get_bluesky_name()
                try:
                    self.derived_from[i] = get_channel_from_string(bluesky_name)
                except Exception as e:
                    return False
        self._is_connected = True
        return True

    def describe(self):
        desc = super().describe()[self.name]
        if not self._is_connected:
            self._connect()
        if self.derived_from:
            desc["derived_from"] = [sig.name for sig in self.derived_from]
        if self.write_access:
            desc["formula"] = self._write_formula
        else:
            desc["formula"] = self._read_formula
        return {self.name: desc}

    def trigger(self):
        """
        Trigger the derived signals to update their values.
        """
        for signal in self.derived_from:
            signal.trigger()
        return super().trigger()

    def get(self, **kwargs):
        """
        Override the get method to handle multiple derived signals.
        """
        if self.write_access:
            return self._readback
        values = {}
        for signal in self.derived_from:
            values[signal.name] = signal.get(**kwargs)
        self._readback = self.inverse(**values)
        return self._readback

    def put(self, value, **kwargs):
        if not self.write_access:
            raise ValueError("This signal is not writable.")
        set_val = self.forward(value)
        res = self.derived_from[0].put(set_val, **kwargs)
        self._metadata["timestamp"] = self.derived_from[0].timestamp
        super().put(value, **kwargs)

    def inverse(self, **values):
        if not self._read_formula:
            raise ValueError("No calculation formula provided for inverse operation.")
        if self._conversion_type == "Simple Function":
            self.eva.namespace.update(values)
            try:
                return self.eva.eval(self._read_formula)
            except Exception as e:
                raise ValueError(f"Error evaluating calculation formula: {e}")
        else:
            return self._conversion_function(**values)

    def forward(self, value):
        if not self._write_formula:
            raise ValueError("No calculation formula provided for forward operation.")
        if self._conversion_type == "Simple Function":
            self.eva.namespace[self.name] = value
            self.eva.namespace["x"] = value
            try:
                return self.eva.eval(self._write_formula)
            except Exception as e:
                raise ValueError(f"Error evaluating calculation formula: {e}")
        else:
            return self._conversion_function(value)

    @property
    def connected(self):
        """
        Check if all derived signals are connected.
        """
        if not self._is_connected:
            self._connect()
        return all(signal.connected for signal in self.derived_from)


class MultiDerivedSignalRO(SignalRO, MultiDerivedSignal):
    """
    A read-only version of MultiDerivedSignal.
    This class inherits from MultiDerivedSignal and SignalRO to provide read-only access.
    """

    def __init__(
        self,
        derived_from,
        *,
        name=None,
        parent=None,
        read_formula=None,
        conversion_type="Simple Function",
        conversion_file="",
        **kwargs,
    ):
        super().__init__(
            derived_from=derived_from,
            write_access=False,
            name=name,
            parent=parent,
            read_formula=read_formula,
            write_formula=None,
            conversion_type=conversion_type,
            conversion_file=conversion_file,
            **kwargs,
        )
