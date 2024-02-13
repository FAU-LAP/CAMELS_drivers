import time
import numpy as np

from PySide6.QtWidgets import QPushButton, QLabel, QComboBox, QGridLayout
from PySide6.QtCore import Signal, QThread, Qt

from nomad_camels.main_classes.manual_control import Manual_Control, Manual_Control_Config
from nomad_camels.main_classes.device_class import Simple_Config_Sub
from nomad_camels.utility import variables_handling

from .agilent_33220a_ophyd import generate_waveform


class Virtual_Lab(Manual_Control):
    def __init__(self, parent=None, control_data=None):
        control_data = control_data or {}
        if 'name' in control_data:
            name = control_data['name']
        else:
            name = 'Virtual Lab'
        super().__init__(parent=parent, title=name)
        self.setLayout(QGridLayout())
        config_dict = {'coffee machine': False,
                       'computer': False,
                       'monitor': False,
                       'oscilloscope': False,
                       'DMM': False,
                       'function generator': False}
        self.sub_widget = Simple_Config_Sub(config_dict=config_dict)
        self.layout().addWidget(self.sub_widget, 0, 0)
        self.run_button = QPushButton('run')
        self.layout().addWidget(self.run_button, 1, 0)
        self.sub_widget.config_changed.connect(self.change_set)
        self.run_button.clicked.connect(self.change_run)

        self.run_thread = None
        self.running = False
        self.adjustSize()
        self.start_device(control_data['device'])
    
    def change_run(self):
        if self.running:
            self.run_button.setText('run')
            self.running = False
        else:
            self.run_button.setText('stop')
            self.running = True
        self.change_set()
    
    def set_done(self):
        self.setCursor(Qt.ArrowCursor)
        self.setEnabled(True)
    
    def start_set(self):
        self.setCursor(Qt.WaitCursor)
        self.setEnabled(False)
    
    def device_ready(self):
        super().device_ready()
        self.run_thread = Run_Thread(device=self.ophyd_device)
        self.run_thread.set_done.connect(self.set_done)
        self.run_thread.still_running = True
        self.run_thread.start()
    
    def change_set(self):
        config_dict = self.sub_widget.get_config()
        config_dict['running'] = self.running
        self.start_set()
        self.run_thread.current_settings = config_dict


    def close(self) -> bool:
        self.run_thread.still_running = False
        return super().close()

    def closeEvent(self, a0):
        self.run_thread.still_running = False
        return super().closeEvent(a0)


class Run_Thread(QThread):
    set_done = Signal()

    def __init__(self, parent=None, device=None):
        super().__init__(parent=parent)
        self.device = device
        self.still_running = False
        self.current_settings = None
        self.last_settings = None
    
    def run(self):
        while self.still_running:
            time.sleep(0.1)
            if self.current_settings and self.current_settings != self.last_settings:
                self.update_settings()
    
    def update_settings(self):
        self.device.output.put(0)
        if 'running' in self.current_settings and self.current_settings['running']:
            params = []
            if 'coffee machine' in self.current_settings and self.current_settings['coffee machine']:
                params.append({'frequency': 50, 'amplitude': 2, 'phase': 0})
            if 'computer' in self.current_settings and self.current_settings['computer']:
                params.append({'frequency': 53910, 'amplitude': 1,
                               'phase': np.random.uniform(0, 360)})
            if 'monitor' in self.current_settings and self.current_settings['monitor']:
                params.append({'frequency': 66700, 'amplitude': 3,
                               'phase': np.random.uniform(0, 360)})
                params.append({'frequency': 55300, 'amplitude': 3,
                               'phase': np.random.uniform(0, 360)})
            if 'oscilloscope' in self.current_settings and self.current_settings['oscilloscope']:
                params.append({'frequency': 81600, 'amplitude': 2,
                               'phase': np.random.uniform(0, 360)})
            if 'DMM' in self.current_settings and self.current_settings['DMM']:
                params.append({'frequency': 94700, 'amplitude': 2.5,
                               'phase': np.random.uniform(0, 360)})
            if 'function generator' in self.current_settings and self.current_settings['function generator']:
                params.append({'frequency': 45800, 'amplitude': 3,
                               'phase': np.random.uniform(0, 360)})
                params.append({'frequency': 61200, 'amplitude': 3,
                               'phase': np.random.uniform(0, 360)})
            wave_form = generate_waveform(tone_params=params, noise_level=1.0,
                                          offset=0.0, sampling_rate=200000,
                                          num_samples=20000)
            self.device.configure_arbitrary_waveform(wave_form)
            self.device.set_arbitrary_waveform(frequency=10)
            self.device.output.put(1)
        self.last_settings = dict(self.current_settings)
        self.set_done.emit()







class Virtual_Lab_Config(Manual_Control_Config):
    def __init__(self, parent=None, control_data=None):
        super().__init__(parent=parent, control_data=control_data,
                         title='Virtual Lab config',
                         control_type='Virtual_Lab')
        control_data = control_data or {}
        select_label = QLabel('Function Generator:')

        self.dev_box = QComboBox()
        devs = []
        for name, device in variables_handling.devices.items():
            if device.name == 'agilent_33220a':
                devs.append(name)
        self.dev_box.addItems(devs)
        if 'device' in control_data and control_data['device'] in devs:
            self.dev_box.setCurrentText(control_data['device'])

        self.layout().addWidget(select_label, 2, 0)
        self.layout().addWidget(self.dev_box, 2, 1)

    def accept(self):
        self.control_data['device'] = self.dev_box.currentText()
        super().accept()
