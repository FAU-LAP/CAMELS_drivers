from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.visa_signal import VISA_Device

from nomad_camels.bluesky_handling.custom_function_signal import (
    Custom_Function_Signal,
    Custom_Function_SignalRO,
)


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
        metadata={"description": "turn the magnet on"},
    )

    polarity = Cpt(
        Custom_Function_Signal,
        name="polarity",
        metadata={"description": "set the polarity of the magnet"},
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
        if not val:
            ret = self.visa_instrument.query("Off")
            self.turned_on = False
        elif self.positive_polarity:
            ret = self.visa_instrument.query("B positive")
            self.turned_on = True
        else:
            ret = self.visa_instrument.query("B negative")
            self.turned_on = True
        if ret != "OK":
            raise ValueError(f"Unexpected response: {ret}")

    def set_polarity(self, val):
        if val:
            self.positive_polarity = True
        else:
            self.positive_polarity = False
        self.set_power_on(self.turned_on)
