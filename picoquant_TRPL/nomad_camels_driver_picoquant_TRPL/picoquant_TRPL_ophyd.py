from ophyd import Device
from ophyd import Component as Cpt
from nomad_camels.bluesky_handling.custom_function_signal import (
    Custom_Function_Signal,
    Custom_Function_SignalRO,
)

from snAPI.Main import snAPI, LogLevel, MeasMode


class Picoquant_TRPL(Device):
    histogram_data = Cpt(Custom_Function_SignalRO, name="histogram_data")
    histogram_bins = Cpt(Custom_Function_SignalRO, name="histogram_bins")

    acquisition_time = Cpt(
        Custom_Function_Signal,
        value=1,
        name="acquisition_time",
        kind="config",
        metadata={"units": "s"},
    )
    sync_edge = Cpt(Custom_Function_Signal, value=1, name="sync_edge", kind="config")
    sync_level = Cpt(
        Custom_Function_Signal, value=-300, name="sync_level", kind="config"
    )
    sync_offset = Cpt(
        Custom_Function_Signal, value=0, name="sync_offset", kind="config"
    )
    chan1_edge = Cpt(Custom_Function_Signal, value=1, name="chan1_edge", kind="config")
    chan1_level = Cpt(
        Custom_Function_Signal, value=-120, name="chan1_level", kind="config"
    )
    chan1_offset = Cpt(
        Custom_Function_Signal, value=0, name="chan1_offset", kind="config"
    )
    resolution = Cpt(
        Custom_Function_Signal, value=1e-9, name="resolution", kind="config"
    )
    chan_stop = Cpt(Custom_Function_Signal, value=5, name="chan_stop", kind="config")

    def __init__(
        self,
        prefix="",
        *,
        name,
        kind=None,
        read_attrs=None,
        configuration_attrs=None,
        parent=None,
        meas_mode="Histogram",
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
        self.sn = snAPI()
        self.sn.getDevice()
        self.sn.setLogLevel(logLevel=LogLevel.DataFile, onOff=True)
        if meas_mode == "Histogram":
            self.sn.initDevice(MeasMode.Histogram)
        elif meas_mode == "T2":
            self.sn.initDevice(MeasMode.T2)
        elif meas_mode == "T3":
            self.sn.initDevice(MeasMode.T3)

        self.resolution.put_function = self.set_resolution
        self.sync_level.put_function = self.set_syncLevel
        self.sync_edge.put_function = self.set_syncEdge
        self.sync_offset.put_function = self.set_syncOffset
        self.chan1_level.put_function = self.set_chan1Level
        self.chan1_edge.put_function = self.set_chan1Edge
        self.chan1_offset.put_function = self.set_chan1Offset
        self.chan_stop.put_function = self.set_chanStop

        self.histogram_data.read_function = self.measure_histogram
        self.histogram_bins.read_function = self.get_histogram_bins

    def set_resolution(self, value):
        binning_factor = int(np.log2(value / (250 * 1e-12)))
        self.sn.device.setHistoLength(self.chan_stop.get())
        self.sn.device.setBinning(binning_factor)

    def set_syncLevel(self, value):
        self.sn.device.setSyncEdgeTrig(value, self.sync_edge.get())

    def set_syncEdge(self, value):
        self.sn.device.setSyncEdgeTrig(self.sync_level.get(), value)

    def set_syncOffset(self, value):
        self.sn.device.setSyncChannelOffset(value)

    def set_chan1Level(self, value):
        self.sn.device.setInputEdgeTrig(0, value, self.chan1_edge.get())

    def set_chan1Edge(self, value):
        self.sn.device.setInputEdgeTrig(0, self.chan1_level.get(), value)

    def set_chan1Offset(self, value):
        self.sn.device.setInputChannelOffset(0, value)

    def set_chanStop(self, value):
        self.sn.device.setHistoLength(value)

    def measure_histogram(self):
        self.sn.histogram.measure(
            acqTime=int(1e3 * self.acquisition_time.get()),
            savePTU=True,
            waitFinished=True,
        )
        return self.sn.histogram.getData()[0]

    def get_histogram_bins(self):
        return self.sn.histogram.bins
