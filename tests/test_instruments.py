import os.path

from PySide6.QtCore import QItemSelectionModel, Qt
import sys
import pytest
import importlib

from nomad_camels.frontpanels import instrument_config
from nomad_camels.utility import variables_handling

driver_path = os.path.dirname(os.path.dirname(__file__))
variables_handling.device_driver_path = driver_path

# drivers that need special files from manufacturer (e.g. dll)
except_drivers = [
    "pi_stage_e709",
    "swabianinstruments_timetagger",
    "thorlabs_K10CR1",
    "thorlabs_MFF",
    "rhode_and_schwarz_smp_02",
    "zaber_rst240b_e08",
    "lakeshore_f41",
]

if os.name != "nt":
    # drivers that run only on windows
    except_drivers += ["mechonics_cu30cl"]
else:
    # drivers that don't run on windows
    except_drivers += []

try:
    with open("../driver_list.txt") as f:
        instr_list = [x.split("==")[0] for x in f.readlines()]
except:
    with open("driver_list.txt") as f:
        instr_list = [x.split("==")[0] for x in f.readlines()]

for driver in except_drivers:
    if driver in instr_list:
        instr_list.remove(driver)


@pytest.mark.parametrize("instr_under_test", instr_list)
def test_instruments(qtbot, instr_under_test):
    instr_path = f"{driver_path}/{instr_under_test}"
    sys.path.append(instr_path)
    module = importlib.import_module(
        f".{instr_under_test}", f"nomad_camels_driver_{instr_under_test}"
    )
    instr = module.subclass()
    assert instr is not None

    conf = instrument_config.Instrument_Config()
    qtbot.addWidget(conf)
    conf.build_table()

    item1 = None
    item2 = None
    for row in range(conf.tableWidget_instruments.rowCount()):
        item1 = conf.tableWidget_instruments.item(row, 0)
        item2 = conf.tableWidget_instruments.item(row, 1)
        if item1.text() == instr_under_test:
            break
    assert item1 is not None  # instrument should be in the installed table
    assert item2 is not None
    assert item1.text() == instr_under_test
    index1 = conf.tableWidget_instruments.indexFromItem(item1)
    conf.tableWidget_instruments.selectionModel().select(
        index1, QItemSelectionModel.Select
    )
    index2 = conf.tableWidget_instruments.indexFromItem(item2)
    conf.tableWidget_instruments.selectionModel().select(
        index2, QItemSelectionModel.Select
    )
    # two items need to be selected, since with a real click, the selection also
    # returns a list
    conf.table_click()  # select

    def check_instr_in():
        """ """
        # clicking on an added device, check whether it is actually added
        qtbot.mouseClick(conf.pushButton_add, Qt.MouseButton.LeftButton)
        instr = conf.get_config()
        assert instr_under_test in instr

    qtbot.waitUntil(check_instr_in)  # wait for the qt event loops
