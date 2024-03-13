from ophyd import Component as Cpt

from nomad_camels_sandbox.server_signals import (
    Demo_Server_Signal,
    Demo_Server_SignalRO,
    Demo_Server_Device,
)


class Demo_SMU(Demo_Server_Device):
    mesV1 = Cpt(
        Demo_Server_SignalRO,
        name="mesV1",
        parameter_name="smu_diode.U",
        metadata={"units": "V"},
    )
    mesI1 = Cpt(
        Demo_Server_SignalRO,
        name="mesI1",
        parameter_name="smu_diode.I",
        metadata={"units": "A"},
    )
    mesV2 = Cpt(
        Demo_Server_SignalRO,
        name="mesV2",
        parameter_name="smu_heater.U",
        metadata={"units": "V"},
    )
    mesI2 = Cpt(
        Demo_Server_SignalRO,
        name="mesI2",
        parameter_name="smu_heater.I",
        metadata={"units": "A"},
    )
    setV1 = Cpt(
        Demo_Server_Signal,
        name="setV1",
        parameter_name="smu_diode.U",
        metadata={"units": "V"},
    )
    setI1 = Cpt(
        Demo_Server_Signal,
        name="setI1",
        parameter_name="smu_diode.I",
        metadata={"units": "A"},
    )
    setV2 = Cpt(
        Demo_Server_Signal,
        name="setV2",
        parameter_name="smu_heater.U",
        metadata={"units": "V"},
    )
    setI2 = Cpt(
        Demo_Server_Signal,
        name="setI2",
        parameter_name="smu_heater.I",
        metadata={"units": "A"},
    )

    NPLC1 = Cpt(
        Demo_Server_Signal,
        name="NPLC1",
        kind="config",
        parameter_name="smu_diode.NPLC",
    )

    NPLC2 = Cpt(
        Demo_Server_Signal,
        name="NPLC2",
        parameter_name="smu_heater.NPLC",
        kind="config",
    )


if __name__ == "__main__":
    smu = Demo_SMU(name="smu")
    smu.finalize_steps()
