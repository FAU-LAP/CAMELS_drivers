from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.visa_signal import (
    VISA_Signal,
    VISA_Signal_RO,
    VISA_Device,
    list_resources
)
from nomad_camels.bluesky_handling.custom_function_signal import (
    Custom_Function_SignalRO,
    Custom_Function_Signal,
)


class Cryovac_TIC_500(VISA_Device):

    input_1 = Cpt(VISA_Signal_RO, name="input_1", metadata={"description": "Input 1."})
    input_2 = Cpt(VISA_Signal_RO, name="input_2", metadata={"description": "Input 2."})
    input_3 = Cpt(VISA_Signal_RO, name="input_3", metadata={"description": "Input 3."})
    input_4 = Cpt(VISA_Signal_RO, name="input_4", metadata={"description": "Input 4."})
    output_1 = Cpt(VISA_Signal, name="output_1", metadata={"description": "Output 1."})
    output_2 = Cpt(VISA_Signal, name="output_2", metadata={"description": "Output 2."})
    output_3 = Cpt(VISA_Signal, name="output_3", metadata={"description": "Output 3."})
    output_4 = Cpt(VISA_Signal, name="output_4", metadata={"description": "Output 4."})
    enable_pid_1 = Cpt(VISA_Signal, name="enable_pid_1", metadata={"description": "Enable PID 1."})
    enable_pid_2 = Cpt(VISA_Signal, name="enable_pid_2", metadata={"description": "Enable PID 2."})
    enable_pid_3 = Cpt(VISA_Signal, name="enable_pid_3", metadata={"description": "Enable PID 3."})
    enable_pid_4 = Cpt(VISA_Signal, name="enable_pid_4", metadata={"description": "Enable PID 4."})

    enable_outputs = Cpt(VISA_Signal, name="enable_outputs", metadata={"description": "Enable outputs."})



    def __init__(
        self,
        prefix="",
        *,
        name,
        kind=None,
        read_attrs=None,
        configuration_attrs=None,
        parent=None,
        resource_name="",
        read_termination="\r\n",
        write_termination="\r\n",
        baud_rate=9600,
        channels_in=None,
        channels_out=None,
        **kwargs,
    ):
        super().__init__(
            prefix=prefix,
            name=name,
            kind=kind,
            read_attrs=read_attrs,
            configuration_attrs=configuration_attrs,
            parent=parent,
            resource_name=resource_name,
            baud_rate=baud_rate,
            write_termination=write_termination,
            read_termination=read_termination,
            **kwargs,
        )

        self.input_settings = channels_in or []
        self.output_settings = channels_out or []

        comps = list(self.component_names)
        for i, setting in enumerate(self.input_settings):
            if not setting['use']:
                comps.remove(f'input_{i+1}')
        for i, setting in enumerate(self.output_settings):
            if not setting['use']:
                comps.remove(f'output_{i+1}')
                comps.remove(f'enable_pid_{i+1}')
            elif not setting['is_pid']:
                comps.remove(f'enable_pid_{i+1}')
        self.component_names = tuple(comps)
        
        if name == 'test':
            return
        self.visa_instrument.write('system.com.verbose Low')

        self.input_1.query = self.query_text(0)
        self.input_2.query = self.query_text(1)
        self.input_3.query = self.query_text(2)
        self.input_4.query = self.query_text(3)

        self.enable_outputs.write = self.enable_output_func

        self.enable_pid_1.write = lambda x, n=0: self.enable_pid_func(x, n)
        self.enable_pid_2.write = lambda x, n=1: self.enable_pid_func(x, n)
        self.enable_pid_3.write = lambda x, n=2: self.enable_pid_func(x, n)
        self.enable_pid_4.write = lambda x, n=3: self.enable_pid_func(x, n)
        
        self.output_1.write = lambda x, n=0: self.set_output(x, n)
        self.output_2.write = lambda x, n=1: self.set_output(x, n)
        self.output_3.write = lambda x, n=2: self.set_output(x, n)
        self.output_4.write = lambda x, n=3: self.set_output(x, n)
    
    def set_output(self, value, channel_number):
        is_pid = self.output_settings[channel_number]['is_pid']
        if is_pid:
            return f'"{self.output_settings[channel_number]["name"]}.PID.Setpoint" {value:g}'
        return f'"{self.output_settings[channel_number]["name"]}" {value:g}'

    def enable_output_func(self, enable):
        if enable:
            return 'outputEnable on'
        return 'outputEnable off'

    def enable_pid_func(self, enable, channel_number):
        s = f'"{self.output_settings[channel_number]["name"]}.PID.Mode" '
        s += 'On' if enable else 'Off'
        return s

    def query_text(self, channel_number):
        return f'"{self.input_settings[channel_number]["name"]}?"'