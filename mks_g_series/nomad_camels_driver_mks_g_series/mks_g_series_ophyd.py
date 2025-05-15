from ophyd import Component as Cpt
from ophyd import Device
from nomad_camels.bluesky_handling.custom_function_signal import (
    Custom_Function_Signal,
    Custom_Function_SignalRO,
)
import serial
import time


def calc_checksum(command, reply=False):
    """Calculate checksum of command"""
    if not reply:
        com_string = "@" + command
    else:
        com_string = command
    total = 0
    for i in range(0, len(com_string)):
        total = total + ord(com_string[i])
    return (hex(total)[-2:]).upper()


class MKS_G_Series(Device):

    flow = Cpt(
        Custom_Function_SignalRO,
        name="flow",
        metadata={"units": "sccm", "description": "flow rate"},
    )
    setpoint = Cpt(
        Custom_Function_Signal,
        name="setpoint",
        metadata={"units": "sccm", "description": "setpoint"},
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
        resource_name=None,
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
        self.setpoint.put_function = self.put_setpoint
        self.flow.read_function = self.read_flow

        if name != "test":
            self.serial = serial.Serial(resource_name, baudrate=9600)
            self.serial.parity = serial.PARITY_NONE
            self.serial.bytesize = serial.EIGHTBITS
            self.serial.stopbits = serial.STOPBITS_ONE

    def comm(self, command, addr=254):
        """Implements communication protocol"""
        com_string = str(addr).zfill(3) + command + ";"
        checksum = calc_checksum(com_string)
        com_string = "@@@@" + com_string + checksum
        com_string = com_string.encode("ascii")
        self.serial.write(com_string)
        time.sleep(0.1)
        reply = self.serial.read(self.serial.inWaiting())
        try:
            reply = reply.decode("ascii")
        except UnicodeDecodeError:
            reply = reply.decode("ascii", "ignore")
            reply = reply.strip("\x00")
            reply = "@" + reply

        if len(reply) == 0:
            raise Exception("Could not communicate with device")
        else:
            if reply[-3:] == calc_checksum(reply[1:-3], reply=True):
                reply = reply[6:-3]  # Cut away master address and checksum
            else:
                raise Exception("Checksum error in reply")
            if reply[1:4] == "ACK":
                reply = reply[4:-3]
            else:
                raise Exception("Error in command")
        return reply

    def put_setpoint(self, value):
        """Set setpoint"""
        command = "SX!" + str(round(value, 1))
        self.comm(command)

    def read_flow(self):
        """Read flow"""
        command = "FX?"
        flow = -1
        for i in range(50):
            try:
                flow = float(self.comm(command))
                return flow
            except ValueError:
                continue
        return flow
