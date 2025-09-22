from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.custom_function_signal import (
    Custom_Function_Signal,
    Custom_Function_SignalRO,
)
from ophyd import Device
from zhinst.toolkit import Session


class Zurich_Instruments_Hdawg(Device):
    upload_sequence_file = Cpt(
        Custom_Function_Signal,
        name="upload_sequence_file",
        metadata={
            "units": "",
            "description": "Upload the sequence file to the AWG. The sequence file can be any ASCII file.",
        },
    )
    enable = Cpt(
        Custom_Function_SignalRO,
        name="enable",
        metadata={
            "units": "",
            "description": "Enables and starts the AWG. Any sequence written to the AWG is executed.",
        },
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
        device_id="dev0000",
        server_host="127.0.0.1",
        port=8000,
        sequence_file="",
        awg_index=0,
        **kwargs
    ):
        super().__init__(
            prefix=prefix,
            name=name,
            kind=kind,
            read_attrs=read_attrs,
            configuration_attrs=configuration_attrs,
            parent=parent,
            **kwargs
        )
        self.device_id = device_id
        self.server_host = server_host
        self.port = port
        self.sequence_file = sequence_file
        self.awg_index = awg_index

        # self.upload_sequence_file.read_function = self.upload_sequence_file_read_function
        # self.enable.read_function = self.enable_read_function
        # self.upload_sequence_file.put_function = self.upload_sequence_file_put_function

        # This if statement prevents the lines of the init below to be run when starting up CAMELS.
        if name == "test":
            return
        self.session = Session(self.server_host)  ## connect to data server
        self.device = self.session.connect_device(self.device_id)  ## connect to device
        self.awg = self.device.awgs[self.awg_index]

    def upload_sequence_file_read_function(self):
        self.seqc_program = read_sequence_file_to_string(self.sequence_file)
        self.awg.load_sequencer_program(self.seqc_program)

    def enable_read_function(self):
        pass

    def upload_sequence_file_put_function(self, value):
        if value:
            self.seqc_program = read_sequence_file_to_string(self.sequence_file)
            self.awg.load_sequencer_program(self.seqc_program)


def read_sequence_file_to_string(file_path):
    with open(file_path, "r") as file:
        data = file.read()
    return data
