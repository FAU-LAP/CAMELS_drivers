from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.visa_signal import VISA_Device

from nomad_camels.bluesky_handling.custom_function_signal import (
    Custom_Function_Signal,
    Custom_Function_SignalRO,
)
import time
from pyvisa import constants


class Lab_Course_Magnet(VISA_Device):
    status = Cpt(
        Custom_Function_SignalRO,
        name="status",
        metadata={
            "description": "status of the magnet (idle / busy; protection contactor; current on/off; polarity)"
        },
    )

    power_on = Cpt(
        Custom_Function_Signal,
        name="power_on",
        metadata={"description": "turn the magnet on (1 on / 0 off)"},
    )

    polarity = Cpt(
        Custom_Function_Signal,
        name="polarity",
        metadata={
            "description": "set the polarity of the magnet (1 positive / -1 negative)"
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
        self.force_sequential = True
        self.currently_reading = False
        self.status.read_function = self.read_status
        self.power_on.put_function = self.set_power_on
        self.polarity.put_function = self.set_polarity
        self.positive_polarity = True
        self.turned_on = False

    def read_status(self):
        self.visa_instrument.flush(192)
        stat = self.visa_instrument.query("s")
        if stat[:4] not in ["idle", "busy"]:
            raise ValueError(f"Unexpected magnet status: {stat}")
        active = stat[:4]
        prot = "open" if stat[7] == "0" else "closed"
        current = "off" if stat[9] == "0" else "on"
        polarity = "positive" if stat[11] == "0" else "negative"
        return {
            "status": active,
            "protection contactor": prot,
            "current": current,
            "polarity": polarity,
        }

    def set_power_on(self, val):
        self.visa_instrument.flush(192)
        stat = self.read_status()
        if not val:
            if stat["current"] == "off":
                return
            self.visa_instrument.write("0")
            time.sleep(0.5)
            ret = self.visa_instrument.read()
            self.turned_on = False
        elif self.positive_polarity:
            if stat["current"] == "on" and stat["polarity"] == "negative":
                self.visa_instrument.write("0")
                time.sleep(20)
                ret_mid = self.visa_instrument.read()
                if ret_mid != "OK":
                    raise ValueError(f"Unexpected response: {ret_mid}")
            elif stat["current"] == "on" and stat["polarity"] == "positive":
                self.turned_on = True
                return
            self.visa_instrument.write("+")
            time.sleep(0.5)
            ret = self.visa_instrument.read()
            self.turned_on = True
        else:
            if stat["current"] == "on" and stat["polarity"] == "positive":
                self.visa_instrument.write("0")
                time.sleep(20)
                ret_mid = self.visa_instrument.read()
                if ret_mid != "OK":
                    raise ValueError(f"Unexpected response: {ret_mid}")
            elif stat["current"] == "on" and stat["polarity"] == "negative":
                self.turned_on = True
                return
            self.visa_instrument.write("-")
            time.sleep(0.5)
            ret = self.visa_instrument.read()
            self.turned_on = True
        if ret != "OK":
            raise ValueError(f"Unexpected response: {ret}")

    def set_polarity(self, val):
        if val:
            if isinstance(val, (float, int)) and val < 0:
                self.positive_polarity = False
            else:
                self.positive_polarity = True
        else:
            self.positive_polarity = False
        self.set_power_on(self.turned_on)
