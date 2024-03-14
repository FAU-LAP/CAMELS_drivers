from ophyd import Component as Cpt
from nomad_camels_sandbox.server_signals import (
    Demo_Server_Signal,
    Demo_Server_SignalRO,
    Demo_Server_Device,
)


class Demo_DMM(Demo_Server_Device):
    # V_DC = Cpt(
    #     VISA_Signal_RO, name="V_DC", parse=r".*?([-+eE\d.]+).*", metadata={"units": "V"}
    # )
    # V_AC = Cpt(
    #     VISA_Signal_RO, name="V_AC", parse=r".*?([-+eE\d.]+).*", metadata={"units": "V"}
    # )
    # I_DC = Cpt(
    #     VISA_Signal_RO, name="I_DC", parse=r".*?([-+eE\d.]+).*", metadata={"units": "A"}
    # )
    # I_AC = Cpt(
    #     VISA_Signal_RO, name="I_AC", parse=r".*?([-+eE\d.]+).*", metadata={"units": "A"}
    # )
    resistance = Cpt(
        Demo_Server_SignalRO,
        name="resistance",
        parameter_name="dmm_pt1000.R",
        metadata={
            "units": "Ohm",
            "description": "Resistance of the Pt1000 temperature sensor",
        },
    )
    # resistance_4_wire = Cpt(
    #     VISA_Signal_RO,
    #     name="resistance_4_wire",
    #     parse=r".*?([-+eE\d.]+).*",
    #     metadata={"units": "Ohm"},
    # )

    # idn = Cpt(VISA_Signal_RO, name="idn", kind="config", query="*IDN?")
    NPLC = Cpt(
        Demo_Server_Signal, name="NPLC", kind="config", parameter_name="dmm_pt1000.NPLC"
    )


if __name__ == "__main__":
    testk = Demo_DMM(name="testk")
