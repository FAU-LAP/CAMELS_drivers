import os.path

from PySide6.QtCore import QItemSelectionModel, Qt
import sys
import pytest

camels_path = r'C:\Users\od93yces\FAIRmat\CAMELS'
sys.path.append(camels_path)

with open('../driver_list.txt') as f:
    instr_list = [x.split('==')[0] for x in f.readlines()]


@pytest.mark.parametrize('instr_under_test', instr_list)
def test_instruments(qtbot, instr_under_test):
    from nomad_camels.frontpanels import manage_instruments
    from nomad_camels.utility import variables_handling
    variables_handling.device_driver_path = os.path.dirname(os.path.dirname(__file__))

    manager = manage_instruments.ManageInstruments()
    qtbot.addWidget(manager)

    conf = manager.config_widget
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
    conf.tableWidget_instruments.selectionModel().select(index1, QItemSelectionModel.Select)
    index2 = conf.tableWidget_instruments.indexFromItem(item2)
    conf.tableWidget_instruments.selectionModel().select(index2, QItemSelectionModel.Select)
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
