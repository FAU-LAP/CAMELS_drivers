from ophyd import Component as Cpt
from nomad_camels.bluesky_handling.visa_signal import (
    VISA_Signal_RO,
    VISA_Signal,
    VISA_Device,
)
from nomad_camels.bluesky_handling.custom_function_signal import Custom_Function_Signal
import time as ttime


class Keysight_E5270B(VISA_Device):
    speedADCPLC = Cpt(Custom_Function_Signal, name="speedADCPLC", kind="config")
    resADCPLC = Cpt(Custom_Function_Signal, name="resADCPLC", kind="config")
    speedADCmode = Cpt(VISA_Signal, name="speedADCmode", kind="config")
    resADCmode = Cpt(VISA_Signal, name="resADCmode", kind="config")
    idn = Cpt(VISA_Signal_RO, name="idn", kind="config", query=lambda: "*IDN?")
    err = Cpt(VISA_Signal_RO, name="err", query="ERR?")
    # --------------------Channel 1----------------------------------------
    setV1 = Cpt(VISA_Signal, name="setV1", metadata={"units": "V"})
    setI1 = Cpt(VISA_Signal, name="setI1", metadata={"units": "A"})
    mesI1 = Cpt(VISA_Signal_RO, name="mesI1", metadata={"units": "A"})
    mesV1 = Cpt(VISA_Signal_RO, name="mesV1", metadata={"units": "V"})
    enable_ch_1 = Cpt(
        VISA_Signal,
        name="enable_ch_1",
    )
    disable_ch_1 = Cpt(
        VISA_Signal,
        name="disable_ch_1",
    )
    # Config settings of the device
    measMode1 = Cpt(
        VISA_Signal,
        name="measMode1",
        kind="config",
    )
    # used in setting current DI and setting voltage DV, only a variable
    currComp1 = Cpt(
        Custom_Function_Signal,
        name="currComp1",
        kind="config",
    )
    voltComp1 = Cpt(Custom_Function_Signal, name="voltComp1", kind="config")
    # voltage range used when setting DV
    VoutRange1 = Cpt(Custom_Function_Signal, name="VoutRange1", kind="config")
    # current range used when setting DI
    IoutRange1 = Cpt(Custom_Function_Signal, name="IoutRange1", kind="config")
    # voltage range used when simply using (MM, CMM and XE)
    VmeasRange1 = Cpt(VISA_Signal, name="VmeasRange1", kind="config")
    # current range used when simply using (MM, CMM and XE)
    ImeasRange1 = Cpt(VISA_Signal, name="ImeasRange1", kind="config")
    # sets ADC to high resolution(=1) or high speed(=0), default is high speed
    setADC1 = Cpt(
        VISA_Signal,
        name="setADC1",
        kind="config",
    )
    # sets filter mode: 0 for disconnect, 1 for connect of the filter
    outputFilter1 = Cpt(
        VISA_Signal,
        name="outputFilter1",
        kind="config",
    )
    # --------------------Channel 2----------------------------------------
    setV2 = Cpt(VISA_Signal, name="setV2", metadata={"units": "V"})
    setI2 = Cpt(VISA_Signal, name="setI2", metadata={"units": "A"})
    mesI2 = Cpt(VISA_Signal_RO, name="mesI2", metadata={"units": "A"})
    mesV2 = Cpt(VISA_Signal_RO, name="mesV2", metadata={"units": "V"})
    enable_ch_2 = Cpt(
        VISA_Signal,
        name="enable_ch_2",
    )
    disable_ch_2 = Cpt(
        VISA_Signal,
        name="disable_ch_2",
    )
    # Config settings of the device
    measMode2 = Cpt(
        VISA_Signal,
        name="measMode2",
        kind="config",
    )
    # used in setting current DI and setting voltage DV, only a variable
    currComp2 = Cpt(
        Custom_Function_Signal,
        name="currComp2",
        kind="config",
    )
    voltComp2 = Cpt(Custom_Function_Signal, name="voltComp2", kind="config")
    # voltage range used when setting DV
    VoutRange2 = Cpt(Custom_Function_Signal, name="VoutRange2", kind="config")
    # current range used when setting DI
    IoutRange2 = Cpt(Custom_Function_Signal, name="IoutRange2", kind="config")
    # voltage range used when simply using (MM, CMM and XE)
    VmeasRange2 = Cpt(VISA_Signal, name="VmeasRange2", kind="config")
    # current range used when simply using (MM, CMM and XE)
    ImeasRange2 = Cpt(VISA_Signal, name="ImeasRange2", kind="config")
    # sets ADC to high resolution(=1) or high speed(=0), default is high speed
    setADC2 = Cpt(
        VISA_Signal,
        name="setADC2",
        kind="config",
    )
    # sets filter mode: 0 for disconnect, 1 for connect of the filter
    outputFilter2 = Cpt(
        VISA_Signal,
        name="outputFilter2",
        kind="config",
    )
    # --------------------Channel 3----------------------------------------
    setV3 = Cpt(VISA_Signal, name="setV3", metadata={"units": "V"})
    setI3 = Cpt(VISA_Signal, name="setI3", metadata={"units": "A"})
    mesI3 = Cpt(VISA_Signal_RO, name="mesI3", metadata={"units": "A"})
    mesV3 = Cpt(VISA_Signal_RO, name="mesV3", metadata={"units": "V"})
    enable_ch_3 = Cpt(
        VISA_Signal,
        name="enable_ch_3",
    )
    disable_ch_3 = Cpt(
        VISA_Signal,
        name="disable_ch_3",
    )
    # Config settings of the device
    measMode3 = Cpt(
        VISA_Signal,
        name="measMode3",
        kind="config",
    )
    # used in setting current DI and setting voltage DV, only a variable
    currComp3 = Cpt(
        Custom_Function_Signal,
        name="currComp3",
        kind="config",
    )
    voltComp3 = Cpt(Custom_Function_Signal, name="voltComp3", kind="config")
    # voltage range used when setting DV
    VoutRange3 = Cpt(Custom_Function_Signal, name="VoutRange3", kind="config")
    # current range used when setting DI
    IoutRange3 = Cpt(Custom_Function_Signal, name="IoutRange3", kind="config")
    # voltage range used when simply using (MM, CMM and XE)
    VmeasRange3 = Cpt(VISA_Signal, name="VmeasRange3", kind="config")
    # current range used when simply using (MM, CMM and XE)
    ImeasRange3 = Cpt(VISA_Signal, name="ImeasRange3", kind="config")
    # sets ADC to high resolution(=1) or high speed(=0), default is high speed
    setADC3 = Cpt(
        VISA_Signal,
        name="setADC3",
        kind="config",
    )
    # sets filter mode: 0 for disconnect, 1 for connect of the filter
    outputFilter3 = Cpt(
        VISA_Signal,
        name="outputFilter3",
        kind="config",
    )
    # --------------------Channel 4----------------------------------------
    setV4 = Cpt(VISA_Signal, name="setV4", metadata={"units": "V"})
    setI4 = Cpt(VISA_Signal, name="setI4", metadata={"units": "A"})
    mesI4 = Cpt(VISA_Signal_RO, name="mesI4", metadata={"units": "A"})
    mesV4 = Cpt(VISA_Signal_RO, name="mesV4", metadata={"units": "V"})
    enable_ch_4 = Cpt(
        VISA_Signal,
        name="enable_ch_4",
    )
    disable_ch_4 = Cpt(
        VISA_Signal,
        name="disable_ch_4",
    )
    # Config settings of the device
    measMode4 = Cpt(
        VISA_Signal,
        name="measMode4",
        kind="config",
    )
    # used in setting current DI and setting voltage DV, only a variable
    currComp4 = Cpt(
        Custom_Function_Signal,
        name="currComp4",
        kind="config",
    )
    voltComp4 = Cpt(Custom_Function_Signal, name="voltComp4", kind="config")
    # voltage range used when setting DV
    VoutRange4 = Cpt(Custom_Function_Signal, name="VoutRange4", kind="config")
    # current range used when setting DI
    IoutRange4 = Cpt(Custom_Function_Signal, name="IoutRange4", kind="config")
    # voltage range used when simply using (MM, CMM and XE)
    VmeasRange4 = Cpt(VISA_Signal, name="VmeasRange4", kind="config")
    # current range used when simply using (MM, CMM and XE)
    ImeasRange4 = Cpt(VISA_Signal, name="ImeasRange4", kind="config")
    # sets ADC to high resolution(=1) or high speed(=0), default is high speed
    setADC4 = Cpt(
        VISA_Signal,
        name="setADC4",
        kind="config",
    )
    # sets filter mode: 0 for disconnect, 1 for connect of the filter
    outputFilter4 = Cpt(
        VISA_Signal,
        name="outputFilter4",
        kind="config",
    )
    # --------------------Channel 5----------------------------------------
    setV5 = Cpt(VISA_Signal, name="setV5", metadata={"units": "V"})
    setI5 = Cpt(VISA_Signal, name="setI5", metadata={"units": "A"})
    mesI5 = Cpt(VISA_Signal_RO, name="mesI5", metadata={"units": "A"})
    mesV5 = Cpt(VISA_Signal_RO, name="mesV5", metadata={"units": "V"})
    enable_ch_5 = Cpt(
        VISA_Signal,
        name="enable_ch_5",
    )
    disable_ch_5 = Cpt(
        VISA_Signal,
        name="disable_ch_5",
    )
    # Config settings of the device
    measMode5 = Cpt(
        VISA_Signal,
        name="measMode5",
        kind="config",
    )
    # used in setting current DI and setting voltage DV, only a variable
    currComp5 = Cpt(
        Custom_Function_Signal,
        name="currComp5",
        kind="config",
    )
    voltComp5 = Cpt(Custom_Function_Signal, name="voltComp5", kind="config")
    # voltage range used when setting DV
    VoutRange5 = Cpt(Custom_Function_Signal, name="VoutRange5", kind="config")
    # current range used when setting DI
    IoutRange5 = Cpt(Custom_Function_Signal, name="IoutRange5", kind="config")
    # voltage range used when simply using (MM, CMM and XE)
    VmeasRange5 = Cpt(VISA_Signal, name="VmeasRange5", kind="config")
    # current range used when simply using (MM, CMM and XE)
    ImeasRange5 = Cpt(VISA_Signal, name="ImeasRange5", kind="config")
    # sets ADC to high resolution(=1) or high speed(=0), default is high speed
    setADC5 = Cpt(
        VISA_Signal,
        name="setADC5",
        kind="config",
    )
    # sets filter mode: 0 for disconnect, 1 for connect of the filter
    outputFilter5 = Cpt(
        VISA_Signal,
        name="outputFilter5",
        kind="config",
    )
    # --------------------Channel 6----------------------------------------
    setV6 = Cpt(VISA_Signal, name="setV6", metadata={"units": "V"})
    setI6 = Cpt(VISA_Signal, name="setI6", metadata={"units": "A"})
    mesI6 = Cpt(VISA_Signal_RO, name="mesI6", metadata={"units": "A"})
    mesV6 = Cpt(VISA_Signal_RO, name="mesV6", metadata={"units": "V"})
    enable_ch_6 = Cpt(
        VISA_Signal,
        name="enable_ch_6",
    )
    disable_ch_6 = Cpt(
        VISA_Signal,
        name="disable_ch_6",
    )
    # Config settings of the device
    measMode6 = Cpt(
        VISA_Signal,
        name="measMode6",
        kind="config",
    )
    # used in setting current DI and setting voltage DV, only a variable
    currComp6 = Cpt(
        Custom_Function_Signal,
        name="currComp6",
        kind="config",
    )
    voltComp6 = Cpt(Custom_Function_Signal, name="voltComp6", kind="config")
    # voltage range used when setting DV
    VoutRange6 = Cpt(Custom_Function_Signal, name="VoutRange6", kind="config")
    # current range used when setting DI
    IoutRange6 = Cpt(Custom_Function_Signal, name="IoutRange6", kind="config")
    # voltage range used when simply using (MM, CMM and XE)
    VmeasRange6 = Cpt(VISA_Signal, name="VmeasRange6", kind="config")
    # current range used when simply using (MM, CMM and XE)
    ImeasRange6 = Cpt(VISA_Signal, name="ImeasRange6", kind="config")
    # sets ADC to high resolution(=1) or high speed(=0), default is high speed
    setADC6 = Cpt(
        VISA_Signal,
        name="setADC6",
        kind="config",
    )
    # sets filter mode: 0 for disconnect, 1 for connect of the filter
    outputFilter6 = Cpt(
        VISA_Signal,
        name="outputFilter6",
        kind="config",
    )
    # --------------------Channel 7----------------------------------------
    setV7 = Cpt(VISA_Signal, name="setV7", metadata={"units": "V"})
    setI7 = Cpt(VISA_Signal, name="setI7", metadata={"units": "A"})
    mesI7 = Cpt(VISA_Signal_RO, name="mesI7", metadata={"units": "A"})
    mesV7 = Cpt(VISA_Signal_RO, name="mesV7", metadata={"units": "V"})
    enable_ch_7 = Cpt(
        VISA_Signal,
        name="enable_ch_7",
    )
    disable_ch_7 = Cpt(
        VISA_Signal,
        name="disable_ch_7",
    )
    # Config settings of the device
    measMode7 = Cpt(
        VISA_Signal,
        name="measMode7",
        kind="config",
    )
    # used in setting current DI and setting voltage DV, only a variable
    currComp7 = Cpt(
        Custom_Function_Signal,
        name="currComp7",
        kind="config",
    )
    voltComp7 = Cpt(Custom_Function_Signal, name="voltComp7", kind="config")
    # voltage range used when setting DV
    VoutRange7 = Cpt(Custom_Function_Signal, name="VoutRange7", kind="config")
    # current range used when setting DI
    IoutRange7 = Cpt(Custom_Function_Signal, name="IoutRange7", kind="config")
    # voltage range used when simply using (MM, CMM and XE)
    VmeasRange7 = Cpt(VISA_Signal, name="VmeasRange7", kind="config")
    # current range used when simply using (MM, CMM and XE)
    ImeasRange7 = Cpt(VISA_Signal, name="ImeasRange7", kind="config")
    # sets ADC to high resolution(=1) or high speed(=0), default is high speed
    setADC7 = Cpt(
        VISA_Signal,
        name="setADC7",
        kind="config",
    )
    # sets filter mode: 0 for disconnect, 1 for connect of the filter
    outputFilter7 = Cpt(
        VISA_Signal,
        name="outputFilter7",
        kind="config",
    )
    # --------------------Channel 8----------------------------------------
    setV8 = Cpt(VISA_Signal, name="setV8", metadata={"units": "V"})
    setI8 = Cpt(VISA_Signal, name="setI8", metadata={"units": "A"})
    mesI8 = Cpt(VISA_Signal_RO, name="mesI8", metadata={"units": "A"})
    mesV8 = Cpt(VISA_Signal_RO, name="mesV8", metadata={"units": "V"})
    enable_ch_8 = Cpt(
        VISA_Signal,
        name="enable_ch_8",
    )
    disable_ch_8 = Cpt(
        VISA_Signal,
        name="disable_ch_8",
    )
    # Config settings of the device
    measMode8 = Cpt(
        VISA_Signal,
        name="measMode8",
        kind="config",
    )
    # used in setting current DI and setting voltage DV, only a variable
    currComp8 = Cpt(
        Custom_Function_Signal,
        name="currComp8",
        kind="config",
    )
    voltComp8 = Cpt(Custom_Function_Signal, name="voltComp8", kind="config")
    # voltage range used when setting DV
    VoutRange8 = Cpt(Custom_Function_Signal, name="VoutRange8", kind="config")
    # current range used when setting DI
    IoutRange8 = Cpt(Custom_Function_Signal, name="IoutRange8", kind="config")
    # voltage range used when simply using (MM, CMM and XE)
    VmeasRange8 = Cpt(VISA_Signal, name="VmeasRange8", kind="config")
    # current range used when simply using (MM, CMM and XE)
    ImeasRange8 = Cpt(VISA_Signal, name="ImeasRange8", kind="config")
    # sets ADC to high resolution(=1) or high speed(=0), default is high speed
    setADC8 = Cpt(
        VISA_Signal,
        name="setADC8",
        kind="config",
    )
    # sets filter mode: 0 for disconnect, 1 for connect of the filter
    outputFilter8 = Cpt(
        VISA_Signal,
        name="outputFilter8",
        kind="config",
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
        use_channels=(),
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
        self.use_channels = use_channels

        if use_channels:
            comps = list(self.component_names)
            for comp in self.component_names:
                for i in range(1, 9):
                    if i not in self.use_channels and str(i) in comp:
                        comps.remove(comp)
                        break
            self.component_names = tuple(comps)

        # array of current compliances for each of the 8 channels
        # array[i] corresponds to channel number i+1
        self.curr_compliance_array = [0, 0, 0, 0, 0, 0, 0, 0]
        # array of voltage compliances for each of the 8 channels
        # array[i] corresponds to channel number i+1
        self.volt_compliance_array = [0, 0, 0, 0, 0, 0, 0, 0]
        # arrays containing the last values set for MM and CMM for each channel
        self.last_MM_value = [None, None, None, None, None, None, None, None]
        self.last_CMM_value = [None, None, None, None, None, None, None, None]
        # the last channel set in with the MM command is read when executing 'XE'
        self.last_MM_channel = None
        # Mode and NPLC of the High Res AD converters for the entire SMU
        self.resADCmode.write = lambda x: self.set_resADC_mode(1, x)
        # Mode and NPLC of the High Speed AD converters for the entire SMU
        self.speedADCmode.write = lambda x: self.set_speedADC_mode(0, x)
        # --------------------Channel 1----------------------------------------
        # set array element of volt compliance to the value entered
        self.voltComp1.put_function = lambda x: self.set_voltCompliance(x, 1)
        self.setI1.write = lambda x: self.source_current(
            x,
            1,
            self.IoutRange1,
        )
        # set array element of curr compliance to the value entered
        self.currComp1.put_function = lambda x: self.set_currCompliance(
            x,
            1,
        )
        self.setV1.write = lambda x: self.source_voltage(x, 1, self.VoutRange1)
        self.enable_ch_1.write = lambda x: f"CN 1"
        self.disable_ch_1.write = lambda x: f"CL 1"
        self.setADC1.write = lambda x: self.setADC_function(1, x)
        self.outputFilter1.write = lambda x: f"FL {x},1"
        # Read single voltage value using MM, CMM and XE command
        # check to see if the current settings of MM and CMM are correct for the desired
        # voltage measurement, the passed value is the channel number to check for
        self.mesV1.query = lambda: self.measure_single_voltage(1)
        # Read single current value using MM, CMM and XE command
        # check to see if the current settings of MM and CMM are correct for the desired
        # current measurement, the passed value is the channel number to check for
        self.mesI1.query = lambda: self.measure_single_current(1)
        # function called when putting value to measMode1
        self.measMode1.write = lambda x: self.set_MM_value(x, 1)
        # function called when putting value to currComp1
        self.ImeasRange1.write = lambda x: f"RI 1,{x}"
        # function called when putting value to voltComp1
        self.VmeasRange1.write = lambda x: f"RV 1,{x}"

        # --------------------Channel 2----------------------------------------
        # set array element of volt compliance to the value entered
        self.voltComp2.put_function = lambda x: self.set_voltCompliance(x, 2)
        self.setI2.write = lambda x: self.source_current(
            x,
            2,
            self.IoutRange2,
        )
        # set array element of curr compliance to the value entered
        self.currComp2.put_function = lambda x: self.set_currCompliance(
            x,
            2,
        )
        self.setV2.write = lambda x: self.source_voltage(x, 2, self.VoutRange2)
        self.enable_ch_2.write = lambda x: f"CN 2"
        self.disable_ch_2.write = lambda x: f"CL 2"
        self.setADC2.write = lambda x: self.setADC_function(2, x)
        self.outputFilter2.write = lambda x: f"FL {x},2"
        # Read single voltage value using MM, CMM and XE command
        # check to see if the current settings of MM and CMM are correct for the desired
        # voltage measurement, the passed value is the channel number to check for
        self.mesV2.query = lambda: self.measure_single_voltage(2)
        # Read single current value using MM, CMM and XE command
        # check to see if the current settings of MM and CMM are correct for the desired
        # current measurement, the passed value is the channel number to check for
        self.mesI2.query = lambda: self.measure_single_current(2)
        # function called when putting value to measMode2
        self.measMode2.write = lambda x: self.set_MM_value(x, 2)
        # function called when putting value to currComp2
        self.ImeasRange2.write = lambda x: f"RI 2,{x}"
        # function called when putting value to voltComp2
        self.VmeasRange2.write = lambda x: f"RV 2,{x}"
        # --------------------Channel 3----------------------------------------
        # set array element of volt compliance to the value entered
        self.voltComp3.put_function = lambda x: self.set_voltCompliance(x, 3)
        self.setI3.write = lambda x: self.source_current(
            x,
            3,
            self.IoutRange3,
        )
        # set array element of curr compliance to the value entered
        self.currComp3.put_function = lambda x: self.set_currCompliance(
            x,
            3,
        )
        self.setV3.write = lambda x: self.source_voltage(x, 3, self.VoutRange3)
        self.enable_ch_3.write = lambda x: f"CN 3"
        self.disable_ch_3.write = lambda x: f"CL 3"
        self.setADC3.write = lambda x: self.setADC_function(3, x)
        self.outputFilter3.write = lambda x: f"FL {x},3"
        # Read single voltage value using MM, CMM and XE command
        # check to see if the current settings of MM and CMM are correct for the desired
        # voltage measurement, the passed value is the channel number to check for
        self.mesV3.query = lambda: self.measure_single_voltage(3)
        # Read single current value using MM, CMM and XE command
        # check to see if the current settings of MM and CMM are correct for the desired
        # current measurement, the passed value is the channel number to check for
        self.mesI3.query = lambda: self.measure_single_current(3)
        # function called when putting value to measMode3
        self.measMode3.write = lambda x: self.set_MM_value(x, 3)
        # function called when putting value to currComp3
        self.ImeasRange3.write = lambda x: f"RI 3,{x}"
        # function called when putting value to voltComp3
        self.VmeasRange3.write = lambda x: f"RV 3,{x}"
        # --------------------Channel 4----------------------------------------
        # set array element of volt compliance to the value entered
        self.voltComp4.put_function = lambda x: self.set_voltCompliance(x, 4)
        self.setI4.write = lambda x: self.source_current(
            x,
            4,
            self.IoutRange4,
        )
        # set array element of curr compliance to the value entered
        self.currComp4.put_function = lambda x: self.set_currCompliance(
            x,
            4,
        )
        self.setV4.write = lambda x: self.source_voltage(x, 4, self.VoutRange4)
        self.enable_ch_4.write = lambda x: f"CN 4"
        self.disable_ch_4.write = lambda x: f"CL 4"
        self.setADC4.write = lambda x: self.setADC_function(4, x)
        self.outputFilter4.write = lambda x: f"FL {x},4"
        # Read single voltage value using MM, CMM and XE command
        # check to see if the current settings of MM and CMM are correct for the desired
        # voltage measurement, the passed value is the channel number to check for
        self.mesV4.query = lambda: self.measure_single_voltage(4)
        # Read single current value using MM, CMM and XE command
        # check to see if the current settings of MM and CMM are correct for the desired
        # current measurement, the passed value is the channel number to check for
        self.mesI4.query = lambda: self.measure_single_current(4)
        # function called when putting value to measMode4
        self.measMode4.write = lambda x: self.set_MM_value(x, 4)
        # function called when putting value to currComp4
        self.ImeasRange4.write = lambda x: f"RI 4,{x}"
        # function called when putting value to voltComp4
        self.VmeasRange4.write = lambda x: f"RV 4,{x}"
        # --------------------Channel 5----------------------------------------
        # set array element of volt compliance to the value entered
        self.voltComp5.put_function = lambda x: self.set_voltCompliance(x, 5)
        self.setI5.write = lambda x: self.source_current(
            x,
            5,
            self.IoutRange5,
        )
        # set array element of curr compliance to the value entered
        self.currComp5.put_function = lambda x: self.set_currCompliance(
            x,
            5,
        )
        self.setV5.write = lambda x: self.source_voltage(x, 5, self.VoutRange5)
        self.enable_ch_5.write = lambda x: f"CN 5"
        self.disable_ch_5.write = lambda x: f"CL 5"
        self.setADC5.write = lambda x: self.setADC_function(5, x)
        self.outputFilter5.write = lambda x: f"FL {x},5"
        # Read single voltage value using MM, CMM and XE command
        # check to see if the current settings of MM and CMM are correct for the desired
        # voltage measurement, the passed value is the channel number to check for
        self.mesV5.query = lambda: self.measure_single_voltage(5)
        # Read single current value using MM, CMM and XE command
        # check to see if the current settings of MM and CMM are correct for the desired
        # current measurement, the passed value is the channel number to check for
        self.mesI5.query = lambda: self.measure_single_current(5)
        # function called when putting value to measMode5
        self.measMode5.write = lambda x: self.set_MM_value(x, 5)
        # function called when putting value to currComp5
        self.ImeasRange5.write = lambda x: f"RI 5,{x}"
        # function called when putting value to voltComp5
        self.VmeasRange5.write = lambda x: f"RV 5,{x}"
        # --------------------Channel 6----------------------------------------
        # set array element of volt compliance to the value entered
        self.voltComp6.put_function = lambda x: self.set_voltCompliance(x, 6)
        self.setI6.write = lambda x: self.source_current(
            x,
            6,
            self.IoutRange6,
        )
        # set array element of curr compliance to the value entered
        self.currComp6.put_function = lambda x: self.set_currCompliance(
            x,
            6,
        )
        self.setV6.write = lambda x: self.source_voltage(x, 6, self.VoutRange6)
        self.enable_ch_6.write = lambda x: f"CN 6"
        self.disable_ch_6.write = lambda x: f"CL 6"
        self.setADC6.write = lambda x: self.setADC_function(6, x)
        self.outputFilter6.write = lambda x: f"FL {x},6"
        # Read single voltage value using MM, CMM and XE command
        # check to see if the current settings of MM and CMM are correct for the desired
        # voltage measurement, the passed value is the channel number to check for
        self.mesV6.query = lambda: self.measure_single_voltage(6)
        # Read single current value using MM, CMM and XE command
        # check to see if the current settings of MM and CMM are correct for the desired
        # current measurement, the passed value is the channel number to check for
        self.mesI6.query = lambda: self.measure_single_current(6)
        # function called when putting value to measMode6
        self.measMode6.write = lambda x: self.set_MM_value(x, 6)
        # function called when putting value to currComp6
        self.ImeasRange6.write = lambda x: f"RI 6,{x}"
        # function called when putting value to voltComp6
        self.VmeasRange6.write = lambda x: f"RV 6,{x}"
        # --------------------Channel 7----------------------------------------
        # set array element of volt compliance to the value entered
        self.voltComp7.put_function = lambda x: self.set_voltCompliance(x, 7)
        self.setI7.write = lambda x: self.source_current(
            x,
            7,
            self.IoutRange7,
        )
        # set array element of curr compliance to the value entered
        self.currComp7.put_function = lambda x: self.set_currCompliance(
            x,
            7,
        )
        self.setV7.write = lambda x: self.source_voltage(x, 7, self.VoutRange7)
        self.enable_ch_7.write = lambda x: f"CN 7"
        self.disable_ch_7.write = lambda x: f"CL 7"
        self.setADC7.write = lambda x: self.setADC_function(7, x)
        self.outputFilter7.write = lambda x: f"FL {x},7"
        # Read single voltage value using MM, CMM and XE command
        # check to see if the current settings of MM and CMM are correct for the desired
        # voltage measurement, the passed value is the channel number to check for
        self.mesV7.query = lambda: self.measure_single_voltage(7)
        # Read single current value using MM, CMM and XE command
        # check to see if the current settings of MM and CMM are correct for the desired
        # current measurement, the passed value is the channel number to check for
        self.mesI7.query = lambda: self.measure_single_current(7)
        # function called when putting value to measMode7
        self.measMode7.write = lambda x: self.set_MM_value(x, 7)
        # function called when putting value to currComp7
        self.ImeasRange7.write = lambda x: f"RI 7,{x}"
        # function called when putting value to voltComp7
        self.VmeasRange7.write = lambda x: f"RV 7,{x}"
        # --------------------Channel 8----------------------------------------
        # set array element of volt compliance to the value entered
        self.voltComp8.put_function = lambda x: self.set_voltCompliance(x, 8)
        self.setI8.write = lambda x: self.source_current(
            x,
            8,
            self.IoutRange8,
        )
        # set array element of curr compliance to the value entered
        self.currComp8.put_function = lambda x: self.set_currCompliance(
            x,
            8,
        )
        self.setV8.write = lambda x: self.source_voltage(x, 8, self.VoutRange8)
        self.enable_ch_8.write = lambda x: f"CN 8"
        self.disable_ch_8.write = lambda x: f"CL 8"
        self.setADC8.write = lambda x: self.setADC_function(8, x)
        self.outputFilter8.write = lambda x: f"FL {x},8"
        # Read single voltage value using MM, CMM and XE command
        # check to see if the current settings of MM and CMM are correct for the desired
        # voltage measurement, the passed value is the channel number to check for
        self.mesV8.query = lambda: self.measure_single_voltage(8)
        # Read single current value using MM, CMM and XE command
        # check to see if the current settings of MM and CMM are correct for the desired
        # current measurement, the passed value is the channel number to check for
        self.mesI8.query = lambda: self.measure_single_current(8)
        # function called when putting value to measMode8
        self.measMode8.write = lambda x: self.set_MM_value(x, 8)
        # function called when putting value to currComp8
        self.ImeasRange8.write = lambda x: f"RI 8,{x}"
        # function called when putting value to voltComp8
        self.VmeasRange8.write = lambda x: f"RV 8,{x}"

    def enable_used_channels(self):
        for channel in self.use_channels:
            self.visa_instrument.write(f"CN {channel}")

    def wait_for_connection(self, all_signals=False, timeout=2.0):
        self.wait_conn_sub(all_signals, timeout)

    def wait_conn_sub(self, all_signals=False, timeout=2.0):
        """Wait for signals to connect

        Parameters
        ----------
        all_signals : bool, optional
            Wait for all signals to connect (including lazy ones)
        timeout : float or None
            Overall timeout
        """
        signals = []
        for walk in self.walk_signals(include_lazy=all_signals):
            name = walk.item.attr_name
            use = True
            for i in range(1, 9):
                if i not in self.use_channels and str(i) in name:
                    use = False
                    break
            if use:
                signals.append(walk.item)

        pending_funcs = {
            dev: getattr(dev, "_required_for_connection", {})
            for name, dev in self.walk_subdevices(include_lazy=all_signals)
        }
        pending_funcs[self] = self._required_for_connection

        t0 = ttime.time()
        while timeout is None or (ttime.time() - t0) < timeout:
            connected = all(sig.connected for sig in signals)
            if connected and not any(pending_funcs.values()):
                self.visa_instrument.write("FMT 2,0;RED 1")
                self.enable_used_channels()
                return
            ttime.sleep(min((0.05, timeout / 10.0)))

        def get_name(sig):
            sig_name = f"{self.name}.{sig.dotted_name}"
            return f"{sig_name} ({sig.pvname})" if hasattr(sig, "pvname") else sig_name

        reasons = []
        unconnected = ", ".join(get_name(sig) for sig in signals if not sig.connected)
        if unconnected:
            reasons.append(f"Failed to connect to all signals: {unconnected}")
        if any(pending_funcs.values()):
            pending = ", ".join(
                description.format(device=dev)
                for dev, funcs in pending_funcs.items()
                for obj, description in funcs.items()
            )
            reasons.append(f"Pending operations: {pending}")
        raise TimeoutError("; ".join(reasons))

    def setADC_function(self, channel, value):
        return f"AAD {channel}, {value}"

    def set_resADC_mode(self, type_res_or_speed, mode):
        if mode == 2 or mode == 1:
            plc = self.resADCPLC.get()
            return f"AIT {type_res_or_speed},{mode},{int(plc)}"
        if mode == 0:
            return f"AIT {type_res_or_speed},{mode}"

    def set_speedADC_mode(self, type_res_or_speed, mode):
        if mode == 2 or mode == 1:
            plc = self.speedADCPLC.get()
            return f"AIT {type_res_or_speed},{mode},{int(plc)}"
        if mode == 0:
            return f"AIT {type_res_or_speed},{mode}"

    def set_MM_value(self, val, chnum):
        self.last_MM_channel = chnum
        self.last_MM_value[chnum - 1] = val
        self.visa_instrument.write(f"MM {val},{chnum}")
        return f"MM {val},{chnum}"

    def set_CMM_value(self, val, chnum):
        self.last_CMM_value[chnum - 1] = val
        self.visa_instrument.write(f"CMM {chnum},{val}")
        return f"CMM {chnum},{val}"

    def measure_single_voltage(self, chnum):
        if self.last_MM_channel != chnum:
            self.set_MM_value(1, chnum)
        elif self.last_MM_value[chnum - 1] != 1:
            self.set_MM_value(1, chnum)
        if self.last_CMM_value[chnum - 1] != 2:
            self.set_CMM_value(2, chnum)
        return "XE"

    def measure_single_current(self, chnum):
        if self.last_MM_channel != chnum:
            self.set_MM_value(1, chnum)
        if self.last_MM_value[chnum - 1] != 1:
            self.set_MM_value(1, chnum)
        if self.last_CMM_value[chnum - 1] != 1:
            self.set_CMM_value(1, chnum)
        return "XE"

    def set_currCompliance(
        self,
        value,
        chan,
    ):
        self.curr_compliance_array[chan - 1] = value

    def set_voltCompliance(self, value, chan):
        self.volt_compliance_array[chan - 1] = value

    def source_current(
        self,
        current,
        chnum,
        range_signal,
    ):
        irange = range_signal.get()
        Vcomp = self.volt_compliance_array[chnum - 1]
        return f"DI {chnum},{irange},{current},{Vcomp}"

    def source_voltage(
        self,
        voltage,
        chnum,
        range_signal,
    ):
        vrange = range_signal.get()
        Icomp = self.curr_compliance_array[chnum - 1]
        return f"DV {chnum},{vrange},{voltage},{Icomp}"


if __name__ == "__main__":
    e5270b = Keysight_E5270B(prefix="Default:", name="e5270b", use_channels=[1, 8])
    # comps = e5270b.walk_components()
    # for comp in comps:
    #     print(comp)
