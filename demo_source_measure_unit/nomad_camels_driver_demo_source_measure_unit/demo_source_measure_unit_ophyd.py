from ophyd import Component as Cpt

from nomad_camels_sandbox.server_signals import (
    Demo_Server_Signal,
    Demo_Server_SignalRO,
    Demo_Server_Device,
)
import requests


class Demo_SMU(Demo_Server_Device):
    mesV1 = Cpt(
        Demo_Server_SignalRO,
        name="mesV1",
        parameter_name="smu_diode.U",
        metadata={"units": "V", "description": "Voltage of the sample"},
    )
    mesI1 = Cpt(
        Demo_Server_SignalRO,
        name="mesI1",
        parameter_name="smu_diode.I",
        metadata={"units": "A", "description": "Current of the sample"},
    )
    mesV2 = Cpt(
        Demo_Server_SignalRO,
        name="mesV2",
        parameter_name="smu_heater.U",
        metadata={"units": "V", "description": "Voltage of the heater"},
    )
    mesI2 = Cpt(
        Demo_Server_SignalRO,
        name="mesI2",
        parameter_name="smu_heater.I",
        metadata={"units": "A", "description": "Current of the heater"},
    )
    setV1 = Cpt(
        Demo_Server_Signal,
        name="setV1",
        parameter_name="smu_diode.U",
        metadata={"units": "V", "description": "Voltage of the sample"},
    )
    setI1 = Cpt(
        Demo_Server_Signal,
        name="setI1",
        parameter_name="smu_diode.I",
        metadata={"units": "A", "description": "Current of the sample"},
    )
    setV2 = Cpt(
        Demo_Server_Signal,
        name="setV2",
        parameter_name="smu_heater.U",
        metadata={"units": "V", "description": "Voltage of the heater"},
    )
    setI2 = Cpt(
        Demo_Server_Signal,
        name="setI2",
        parameter_name="smu_heater.I",
        metadata={"units": "A", "description": "Current of the heater"},
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

    compliance_1 = Cpt(
        Demo_Server_Signal,
        name="compliance_1",
        parameter_name="smu_diode.COMPL",
        kind="config",
    )

    compliance_2 = Cpt(
        Demo_Server_Signal,
        name="compliance_2",
        parameter_name="smu_heater.COMPL",
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
        demo_server_port=8080,
        demo_server_host="localhost",
        experiment="diode_on_heater",
        **kwargs,
    ):
        super().__init__(
            prefix=prefix,
            name=name,
            kind=kind,
            read_attrs=read_attrs,
            configuration_attrs=configuration_attrs,
            parent=parent,
            demo_server_port=demo_server_port,
            demo_server_host=demo_server_host,
            **kwargs,
        )
        if experiment == "semiconductor_resistor_on_heater":
            for signal in [
                self.mesV1,
                self.mesI1,
                self.setV1,
                self.setI1,
                self.NPLC1,
                self.compliance_1,
            ]:
                signal.parameter_name = signal.parameter_name.replace("diode", "sample")
            requests.get(
                f"http://{self.demo_server_host}:{self.demo_server_port}/set_experiment",
                params={"experiment.setup": experiment},
            )


if __name__ == "__main__":
    smu = Demo_SMU(name="smu")
    smu.finalize_steps()
