import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt

from nomad_camels.main_classes.manual_control import Manual_Control, Manual_Control_Config
from nomad_camels.main_classes.plot_widget import PlotWidget_NoBluesky
from nomad_camels.ui_widgets.warn_popup import WarnPopup
from nomad_camels.main_classes.device_class import Simple_Config_Sub

from PySide6.QtWidgets import QCheckBox, QPushButton, QLabel, QComboBox, QGridLayout, QWidget, QFileDialog
from PySide6.QtCore import Signal, QThread, Qt

from nomad_camels.utility import variables_handling


class Agilent_6000_Manual_Control(Manual_Control):
    def __init__(self, parent=None, control_data=None):
        control_data = control_data or {}
        if 'name' in control_data:
            name = control_data['name']
        else:
            name = 'Agilent 6000 - Manual Control'
        super().__init__(parent, name, control_data)
        layout = QGridLayout()
        self.setLayout(layout)
        self.device = variables_handling.devices[control_data['device']]

        comboboxes = {'image_type': ['png', 'bmp8bit', 'bmp', 'tiff']}
        self.settings_widge = Simple_Config_Sub(config_dict=self.device.config,
                                                comboBoxes=comboboxes)
        
        self.screenshot_button = QPushButton('Screenshot')
        self.get_data_button = QPushButton('Get Data')

        layout.addWidget(self.settings_widge, 0, 0, 1, 2)
        layout.addWidget(self.screenshot_button, 1, 0)
        layout.addWidget(self.get_data_button, 1, 1)

        self.image = None
        self.data = None
        self.osci_thread = None
        self.adjustSize()
        self.start_device(control_data['device'])
    
    def device_ready(self):
        super().device_ready()
        self.osci_thread = Oscilloscope_Thread(self.ophyd_device)
        self.osci_thread.image_signal.connect(self.show_image)
        self.osci_thread.data_signal.connect(self.show_data)
        self.screenshot_button.clicked.connect(self.get_image)
        self.get_data_button.clicked.connect(self.get_data)
        self.settings_widge.config_changed.connect(self.configure)
        self.osci_thread.job_done.connect(self.end_job)
        self.osci_thread.exception_signal.connect(self.propagate_exception)
        self.osci_thread.start()

    def propagate_exception(self, exception):
        raise exception
    
    def close(self):
        self.osci_thread.still_running = False
        return super().close()
    
    def closeEvent(self, a0):
        self.osci_thread.still_running = False
        return super().closeEvent(a0)

    def start_job(self):
        self.setCursor(Qt.WaitCursor)
        self.setEnabled(False)
    
    def end_job(self):
        self.setEnabled(True)
        self.setCursor(Qt.ArrowCursor)
    
    def get_image(self):
        self.start_job()
        self.osci_thread.image_queried = True
    
    def get_data(self):
        self.start_job()
        self.osci_thread.data_queried = True

    def configure(self):
        self.start_job()
        self.osci_thread.configuration = self.settings_widge.get_config()
    
    def show_image(self, image):
        self.image = image
        plt.imshow(image)
        plt.show()
    
    def show_data(self, data):
        self.data = data
        # TODO

    



class Oscilloscope_Thread(QThread):
    image_signal = Signal(np.ndarray)
    data_signal = Signal(dict)
    job_done = Signal()
    exception_signal = Signal(Exception)

    def __init__(self, device, parent=None):
        super().__init__(parent)
        self.device = device
        self.still_running = True
        self.image_queried = False
        self.data_queried = False
        self.configuration = None
        self.last_config = device.configure({})

    def run(self):
        while self.still_running:
            if self.image_queried:
                self.get_image()
            if self.data_queried:
                self.get_data()
            if self.configuration is not None:
                self.do_config()
            time.sleep(0.1)
    
    def get_image(self):
        try:
            img_data = self.device.image.get()
            self.image_signal.emit(img_data)
        except Exception as e:
            self.exception_signal.emit(e)
        finally:
            self.image_queried = False
            self.job_done.emit()
    
    def get_data(self):
        try:
            data = {}
            channels = [self.device.channel1, self.device.channel2,
                        self.device.channel3, self.device.channel4]
            digitals = [self.device.digital1, self.device.digital2]
            for i in range(4):
                disp = self.device.visa_instrument.query(f':CHAN{i+1}:DISP?;')
                if '0' in disp:
                    continue
                data[f'channel {i+1}'] = channels[i].get()
                data[f'time {i+1}'] = self.device.times_analog[i]
            disp = self.device.visa_instrument.query(f':FUNC:DISP?;')
            if '0' not in disp:
                data['math'] = self.device.math_data.get()
                data['time math'] = self.device.times_math
            for i in range(2):
                disp = self.device.visa_instrument.query(f':POD{i+1}:DISP?;')
                if '0' in disp:
                    continue
                data[f'digital {i+1}'] = digitals[i].get()
                data[f'time digital {i+1}'] = self.device.times_digital[i]
            # data = pd.DataFrame(data)
            self.data_signal.emit(data)
        except Exception as e:
            self.exception_signal.emit(e)
        finally:
            self.data_queried = False
            self.job_done.emit()

    def do_config(self):
        try:
            if self.configuration != self.last_config:
                self.last_config = self.device.configure(self.configuration)
        except Exception as e:
            self.exception_signal.emit(e)
        finally:
            self.configuration = None
            self.job_done.emit()


class Agilent_6000_Manual_Control_Config(Manual_Control_Config):
    def __init__(self, parent=None, control_data=None):
        super().__init__(parent, control_data,
                         title='Agilent 6000 manual Control Config', 
                         control_type='Agilent_6000_Manual_Control')
        control_data = control_data or {}
        self.layout().addWidget(QLabel('Oscilloscope:'), 2, 0)
        self.comboBox_device = QComboBox()
        self.layout().addWidget(self.comboBox_device, 2, 1)
        oscis = []
        for name, device in variables_handling.devices.items():
            if device.name == 'agilent_6000':
                oscis.append(name)
        self.comboBox_device.addItems(oscis)
        if 'device' in control_data and control_data['device'] in oscis:
            self.comboBox_device.setCurrentText(control_data['device'])
        
    def accept(self):
        self.control_data['device'] = self.comboBox_device.currentText()
        super().accept()

