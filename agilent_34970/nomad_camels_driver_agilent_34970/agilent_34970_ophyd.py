from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.visa_signal import VISA_Device, VISA_Signal_RO

from nomad_camels.bluesky_handling.custom_function_signal import (
    Custom_Function_Signal,
    Custom_Function_SignalRO,
)


v_range_dict = {
    "100 mV": ".1,",
    "1 V": "1,",
    "10 V": "10,",
    "100 V": "100,",
    "300 V": "300,",
    "Auto": "AUTO",
    "Minimum": "MIN,",
    "Maximum": "MAX,",
}

c_range_dict = {
    "10 mA": ".01,",
    "100 mA": ".1,",
    "1 A": "1,",
    "Auto": "AUTO",
    "Minimum": "MIN,",
    "Maximum": "MAX,",
}

r_range_dict = {
    "100 Ohm": "1e2,",
    "1 kOhm": "1e3,",
    "10 kOhm": "10e3,",
    "100 kOhm": "100e3,",
    "1 MOhm": "1e6,",
    "10 MOhm": "10e6,",
    "100 MOhm": "100e6,",
    "Auto": "AUTO",
    "Minimum": "MIN,",
    "Maximum": "MAX,",
}

resolution_dict = {
    "Least": "MIN",
    "Highest": "MAX",
    "Default": "DEF",
}

temp_unit_dict = {
    "Kelvin": "K",
    "Celsius": "C",
    "Fahrenheit": "F",
}


class Agilent_34970(VISA_Device):
    idn = Cpt(VISA_Signal_RO, query="*IDN?", name="idn", kind="config")

    read_DMM = Cpt(
        Custom_Function_SignalRO,
        name="read_DMM",
        metadata={"description": "Read the data from the internal DMM"},
    )

    activate_channels = Cpt(
        Custom_Function_Signal,
        value="101, 102",
        name="activate_channels",
        metadata={
            "description": "Comma separated list of channels to activate\nMatrix module: closes the circuit\nMultiplexer module: route this channel to the DMM (caveat: only one possible!)"
        },
    )
    deactivate_channels = Cpt(
        Custom_Function_Signal,
        value="101, 102",
        name="deactivate_channels",
        metadata={
            "description": "Comma separated list of channels to deactivate\nMatrix module: opens the circuit\nMultiplexer module: route this channel to the null"
        },
    )

    measurement_type = Cpt(
        Custom_Function_Signal,
        value="DC Voltage",
        name="measurement_type",
        kind="config",
    )
    transducer_type = Cpt(
        Custom_Function_Signal,
        value="Thermocouple",
        name="transducer_type",
        kind="config",
    )
    thermocouple_type = Cpt(
        Custom_Function_Signal,
        value="K",
        name="thermocouple_type",
        kind="config",
    )
    thermistor_type = Cpt(
        Custom_Function_Signal,
        value="2252",
        name="thermistor_type",
        kind="config",
    )
    RTD_type = Cpt(
        Custom_Function_Signal,
        value="85",
        name="RTD_type",
        kind="config",
    )
    RTD_reference_resistance = Cpt(
        Custom_Function_Signal,
        value="1000",
        name="RTD_reference_resistance",
        kind="config",
    )
    temperature_unit = Cpt(
        Custom_Function_Signal,
        value="Kelvin",
        name="temperature_unit",
        kind="config",
    )
    measurement_range = Cpt(
        Custom_Function_Signal,
        value="Auto",
        name="measurement_range",
        kind="config",
        metadata={
            "description": "Range for voltage, frequency and period measurements."
        },
    )
    measurement_resolution = Cpt(
        Custom_Function_Signal,
        value="Default",
        name="measurement_resolution",
        kind="config",
    )
    current_range = Cpt(
        Custom_Function_Signal,
        value="Auto",
        name="current_range",
        kind="config",
    )
    current_resolution = Cpt(
        Custom_Function_Signal,
        value="Default",
        name="current_resolution",
        kind="config",
    )
    resistance_range = Cpt(
        Custom_Function_Signal,
        value="Auto",
        name="resistance_range",
        kind="config",
    )
    resistance_resolution = Cpt(
        Custom_Function_Signal,
        value="Default",
        name="resistance_resolution",
        kind="config",
    )
    measurement_channel = Cpt(
        Custom_Function_Signal,
        value="201",
        name="measurement_channel",
        kind="config",
        metadata={
            "description": "Comma separated list of channels. Use call function to apply the other settings to these channels. You may later apply other settings to other channels."
        },
    )
    display_on = Cpt(
        Custom_Function_Signal,
        value=True,
        name="display_on",
        kind="config",
        metadata={
            "description": "Turns the instrument's display on or off."
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
        self.last_channel = None
        self.read_DMM.read_function = self.read_from_DMM
        self.activate_channels.put_function = self.set_active_channels
        self.deactivate_channels.put_function = self.set_inactive_channels
        self.display_on.put_function = self.set_display_on_off
    
    def set_display_on_off(self, value):
        if value:
            val = 'ON'
        else:
            val = 'OFF'
        self.visa_instrument.write(f'DISP {val}')

    def set_active_channels(self, channels):
        if not isinstance(channels, str):
            channels = ",".join([str(int(x)) for x in channels])
        set_str = f"ROUT:CLOS (@{channels})"
        self.visa_instrument.write(set_str)

    def set_inactive_channels(self, channels):
        if not isinstance(channels, str):
            channels = ",".join([str(int(x)) for x in channels])
        set_str = f"ROUT:OPEN (@{channels})"
        self.visa_instrument.write(set_str)

    def read_from_DMM(self):
        channel = self.measurement_channel.get()
        if channel != self.last_channel:
            self.visa_instrument.write(f"ROUT:MON (@{channel})")
            self.visa_instrument.write("ROUT:MON:STAT ON")
        return float(self.visa_instrument.query("ROUT:MON:DATA?"))

    def apply_configuration(self):
        config_string = "CONF"
        if self.measurement_type.get() == "DC Voltage":
            config_string += ":VOLT:DC "
            config_string = self.add_range_res_to_string(config_string)
        elif self.measurement_type.get() == "AC Voltage":
            config_string += ":VOLT:AC "
            config_string = self.add_range_res_to_string(config_string)
        elif self.measurement_type.get() == "DC Current":
            config_string += ":CURR:DC "
            config_string = self.add_range_res_to_string(config_string, c_range_dict)
        elif self.measurement_type.get() == "AC Current":
            config_string += ":CURR:AC "
            config_string = self.add_range_res_to_string(config_string, c_range_dict)
        elif self.measurement_type.get() == "Resistance":
            config_string += ":RES "
            config_string = self.add_range_res_to_string(config_string, r_range_dict)
        elif self.measurement_type.get() == "4-Wire Resistance":
            config_string += ":FRES "
            config_string = self.add_range_res_to_string(config_string, r_range_dict)
        elif self.measurement_type.get() == "Frequency":
            config_string += ":FREQ 20,"
            config_string += v_range_dict[self.measurement_range.get()]
        elif self.measurement_type.get() == "Period":
            config_string += ":PER .05,"
            config_string += v_range_dict[self.measurement_range.get()]
        elif self.measurement_type.get() == "Digital":
            config_string += ":DIG:BYTE "
        elif self.measurement_type.get() == "Totalizer":
            config_string += ":TOT READ,"
        elif self.measurement_type.get() == "Temperature":
            config_string += ":TEMP "
            if self.transducer_type.get() == "Thermocouple":
                config_string += "TC,"
                config_string += self.thermocouple_type.get()
            elif self.transducer_type.get() == "Thermistor":
                config_string += "THER,"
                config_string += self.thermistor_type.get()
            elif self.transducer_type.get() == "RTD":
                config_string += "RTD,"
                config_string += self.RTD_type.get()
                config_string += ","
                config_string += self.RTD_reference_resistance.get()
            elif self.transducer_type.get() == "4-Wire RTD":
                config_string += "FRTD,"
                config_string += self.RTD_type.get()
                config_string += ","
                config_string += f" (@{self.measurement_channel.get()})"
                config_string += f";:SENS:TEMP:TRAN:FRTD:RES:REF {float(self.RTD_reference_resistance.get()):3.2e}"
            config_string += ","
        config_string += f"(@{self.measurement_channel.get()})"
        config_string += f";:UNIT:TEMP {temp_unit_dict[self.temperature_unit.get()]}"
        self.visa_instrument.write(config_string)

    def add_range_res_to_string(self, config_string, range_dict=v_range_dict):
        range_val = range_dict[self.measurement_range.get()]
        config_string += range_dict[range_val]
        if range_val != "AUTO":
            config_string += resolution_dict[self.measurement_resolution.get()]
        config_string += ","
        return config_string
