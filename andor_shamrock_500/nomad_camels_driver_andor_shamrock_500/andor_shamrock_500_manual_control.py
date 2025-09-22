import importlib
import time

import numpy as np
from nomad_camels.main_classes.manual_control import (
    Manual_Control,
    Manual_Control_Config,
)
from .andor_shamrock_500_config_sub import subclass_config_sub
from nomad_camels.main_classes.plot_widget import PlotWidget_NoBluesky
from nomad_camels.ui_widgets.warn_popup import WarnPopup

from PySide6.QtWidgets import (
    QCheckBox,
    QPushButton,
    QLabel,
    QComboBox,
    QGridLayout,
    QWidget,
    QFileDialog,
)
from PySide6.QtCore import Signal, QThread, Qt

from nomad_camels.utility import variables_handling


class Andor_Manual_Control(Manual_Control):
    def __init__(self, parent=None, control_data=None):
        control_data = control_data or {}
        if "name" in control_data:
            name = control_data["name"]
        else:
            name = "Andor Spectrometer - Manual Control"
        super().__init__(parent=parent, title=name)
        self.setLayout(QGridLayout())
        self.device = variables_handling.devices[control_data["spectrometer"]]

        self.settings_widge = subclass_config_sub(
            parent=self, config_dict=self.device.config
        )
        self.camera = variables_handling.devices[control_data["camera"]]
        cam_type = self.camera.name
        py_package = importlib.import_module(
            f"nomad_camels_driver_{cam_type}.{cam_type}"
        )
        self.camera_widge = py_package.subclass_config_sub(
            parent=self, config_dict=self.camera.config
        )

        self.layout().addWidget(self.settings_widge, 0, 0)
        self.layout().addWidget(self.camera_widge, 0, 1)

        self.meas_widget = QWidget()
        lay = QGridLayout()
        self.meas_widget.setLayout(lay)
        self.acquire_button = QPushButton("acquire spectrum")
        self.continuous_button = QPushButton("continuous spectra")
        self.save_button = QPushButton("save spectrum")
        self.checkBox_clear_plot = QCheckBox("clear plot every spectrum")
        self.checkBox_clear_plot.setChecked(True)
        lay.addWidget(self.save_button, 0, 0)
        lay.addWidget(self.checkBox_clear_plot, 0, 1)
        lay.addWidget(self.continuous_button, 0, 2)
        lay.addWidget(self.acquire_button, 0, 3)

        self.layout().addWidget(self.meas_widget, 1, 0, 1, 2)

        self.spectrum_plot = PlotWidget_NoBluesky(
            "wavelength (nm)", "intensity (counts)", title="Spectrum"
        )
        self.image_plot = None
        self.current_data = {}

        self.acquire_button.clicked.connect(self.measure_spectrum)
        self.continuous_meas = False
        self.continuous_button.clicked.connect(self.continuous_spectra)

        self.settings_widge.set_grating_number.lineEdit().returnPressed.connect(
            self.set_grating
        )
        self.settings_widge.initial_wavelength.lineEdit().returnPressed.connect(
            self.set_wavelength
        )
        self.settings_widge.input_port.currentTextChanged.connect(self.set_input_port)
        self.settings_widge.output_port.currentTextChanged.connect(self.set_output_port)
        self.settings_widge.input_slit_size.lineEdit().returnPressed.connect(
            self.set_input_slit_size
        )
        self.settings_widge.output_slit_size.lineEdit().returnPressed.connect(
            self.set_output_slit_size
        )
        self.settings_widge.checkBox_horizontal_flip.clicked.connect(
            self.set_horizontal_flip
        )
        self.camera_widge.config_changed.connect(self.change_camera_config)
        self.save_button.clicked.connect(self.save_spectrum)

        self.spectrometer_thread = None
        self.start_device(control_data["spectrometer"])

    def device_ready(self):
        super().device_ready()
        self.spectrometer_thread = Spectrometer_Work_Thread(self, self.ophyd_device)
        self.spectrometer_thread.job_done.connect(self.stop_job)
        self.spectrometer_thread.spectrum_data_signal.connect(self.show_spectrum)
        self.spectrometer_thread.new_cam_config.connect(self.update_cam_config)
        self.spectrometer_thread.new_spec_config.connect(self.update_config)
        self.spectrometer_thread.start()

    def save_spectrum(self):
        if not self.current_data:
            return
        file = QFileDialog.getSaveFileName(self, "Save Spectrum", "*.txt")[0]
        if not file:
            return
        import numpy as np

        if self.current_data["intensity"].ndim > 1:
            arr = np.column_stack(
                [
                    self.current_data["wavelength"],
                    self.current_data["intensity"].transpose(),
                ]
            )
        else:
            arr = np.stack(
                [self.current_data["wavelength"], self.current_data["intensity"]]
            ).transpose()
        np.savetxt(file, arr, delimiter="\t", header="wavelength (nm)\t(intensity)")

    def update_config(self, config_dict):
        self.settings_widge.config_dict = config_dict
        self.settings_widge.load_config()

    def update_cam_config(self, config_dict):
        self.camera_widge.config_dict = config_dict
        self.camera_widge.load_config()

    def start_job(self):
        self.setCursor(Qt.WaitCursor)
        self.setEnabled(False)

    def stop_job(self):
        self.setCursor(Qt.ArrowCursor)
        self.setEnabled(True)

    def set_grating(self):
        val = self.settings_widge.set_grating_number.value()
        self.spectrometer_thread.do_function("set_grating", val)
        self.start_job()

    def set_wavelength(self):
        val = self.settings_widge.initial_wavelength.value()
        self.spectrometer_thread.do_function("set_wavelength", val)
        self.start_job()

    def set_input_port(self):
        val = self.settings_widge.input_port.currentText()
        self.spectrometer_thread.do_function("set_input_port", val)
        self.start_job()

    def set_output_port(self):
        val = self.settings_widge.output_port.currentText()
        self.spectrometer_thread.do_function("set_output_port", val)
        self.start_job()

    def set_input_slit_size(self):
        val = self.settings_widge.input_slit_size.value()
        self.spectrometer_thread.do_function("set_input_slit_size", val)
        self.start_job()

    def set_output_slit_size(self):
        val = self.settings_widge.output_slit_size.value()
        self.spectrometer_thread.do_function("set_output_slit_size", val)
        self.start_job()

    def set_horizontal_flip(self):
        self.ophyd_device.horizontal_cam_flip.put(
            self.settings_widge.checkBox_horizontal_flip.isChecked()
        )

    def measure_spectrum(self):
        self.spectrometer_thread.do_function("measure_spectrum", None)
        self.start_job()

    def show_spectrum(self, wl, intensity):
        try:
            self.current_data["intensity"] = intensity
            self.current_data["wavelength"] = wl
            if intensity.ndim > 1:
                if self.image_plot is None:
                    import matplotlib.pyplot as plt

                    self.image_plot = plt.subplots()
                x, y = np.meshgrid(wl, range(len(intensity)))
                self.image_plot[1].clear()
                self.image_plot[1].pcolormesh(x, y, intensity)
                self.image_plot[0].show()
            else:
                self.spectrum_plot.plot.add_data(
                    wl,
                    {"intensity": intensity},
                    add=not self.checkBox_clear_plot.isChecked(),
                )
                self.spectrum_plot.show()
        except Exception as e:
            WarnPopup(self, str(e), "error")

    def continuous_spectra(self):
        if not self.continuous_meas:
            self.setCursor(Qt.WaitCursor)
            self.continuous_button.setText("stop acquisition")
            self.acquire_button.setEnabled(False)
            self.save_button.setEnabled(False)
            self.settings_widge.setEnabled(False)
            self.camera_widge.setEnabled(False)
            self.continuous_meas = True
            self.spectrometer_thread.continuous = True
        else:
            self.spectrometer_thread.continuous = False
            self.setCursor(Qt.ArrowCursor)
            self.continuous_button.setText("continuous spectra")
            self.acquire_button.setEnabled(True)
            self.save_button.setEnabled(True)
            self.settings_widge.setEnabled(True)
            self.camera_widge.setEnabled(True)
            self.continuous_meas = False

    def change_camera_config(self, x, conf):
        configs = self.camera_widge.get_config()
        value = configs[conf]
        self.spectrometer_thread.do_function("change_camera_config", [value, conf])
        self.start_job()

    def close(self) -> bool:
        if self.spectrometer_thread:
            self.spectrometer_thread.still_running = False
            self.spectrometer_thread.continuous = False
        return super().close()

    def closeEvent(self, a0):
        if self.spectrometer_thread:
            self.spectrometer_thread.still_running = False
            self.spectrometer_thread.continuous = False
        self.spectrum_plot.close()
        if self.image_plot is not None:
            import matplotlib.pyplot as plt

            plt.close(self.image_plot[0])
            self.image_plot = None
        return super().closeEvent(a0)


class Spectrometer_Work_Thread(QThread):
    job_done = Signal()
    spectrum_data_signal = Signal(object, object)
    new_spec_config = Signal(dict)
    new_cam_config = Signal(dict)

    def __init__(self, parent=None, spectrometer=None):
        super().__init__(parent=parent)
        self.spectrometer = spectrometer
        self.still_running = True
        self.continuous = False
        self.function_to_do = None
        self.function_value = None
        self.last_config = None
        self.last_cam_config = None

    def run(self):
        i = 100
        while self.still_running:
            time.sleep(0.1)
            if self.function_to_do:
                getattr(self, self.function_to_do)(self.function_value)
                self.function_to_do = None
                self.function_value = None
                self.job_done.emit()
            if self.continuous:
                self.continuous_function()
            if i >= 100:
                self.update_configs()
                i = 0
            i += 1

    def update_configs(self):
        spec_config = self.spectrometer.read_configuration()
        cam_config = self.spectrometer.get_camera_device().read_configuration()
        if spec_config != self.last_config:
            self.last_config = spec_config
            conf = {}
            name = self.spectrometer.name
            for k, v in spec_config.items():
                conf[k.split(f"{name}_")[1]] = v["value"]
            conf["wavelength"] = self.spectrometer.wavelength.get()
            self.new_spec_config.emit(conf)
        if cam_config != self.last_cam_config:
            name = self.spectrometer.get_camera_device().name
            conf = {}
            for k, v in cam_config.items():
                conf[k.split(f"{name}_")[1]] = v["value"]
            self.last_cam_config = cam_config
            self.new_cam_config.emit(conf)

    def do_function(self, name, value):
        self.function_to_do = name
        self.function_value = value

    def set_grating(self, value):
        try:
            self.spectrometer.set_grating_number.put(value)
        except Exception as e:
            WarnPopup(None, str(e), "error")

    def set_wavelength(self, value):
        try:
            self.spectrometer.center_wavelength.put(value)
        except Exception as e:
            WarnPopup(None, str(e), "error")

    def set_input_port(self, value):
        try:
            self.spectrometer.input_port.put(value)
        except Exception as e:
            WarnPopup(None, str(e), "error")

    def set_output_port(self, value):
        try:
            self.spectrometer.output_port.put(value)
        except Exception as e:
            WarnPopup(None, str(e), "error")

    def set_input_slit_size(self, value):
        try:
            self.spectrometer.input_slit_size.put(value)
        except Exception as e:
            WarnPopup(None, str(e), "error")

    def set_output_slit_size(self, value):
        try:
            self.spectrometer.output_slit_size.put(value)
        except Exception as e:
            WarnPopup(None, str(e), "error")

    def measure_spectrum(self, value):
        try:
            intensity = self.spectrometer.spectrum.get()
            wl = self.spectrometer.wavelength.get()
            self.spectrum_data_signal.emit(wl, intensity)
        except Exception as e:
            WarnPopup(None, str(e), "error")

    def continuous_function(self):
        cam = self.spectrometer.get_camera_device().camera
        cam.start_acquisition()
        while self.continuous:
            time.sleep(0.1)
            im = cam.read_newest_image()
            if im is not None:
                wl = self.spectrometer.wavelength.get()
                if len(im) == 1:
                    im = im[0]
                self.spectrum_data_signal.emit(wl, im)

    def change_camera_config(self, value):
        value, conf = value
        try:
            cam = self.spectrometer.get_camera_device()
            set_signal = getattr(cam, conf)
            set_signal.put(value)
        except Exception as e:
            WarnPopup(None, str(e), "error")


class Andor_Manual_Control_Config(Manual_Control_Config):
    def __init__(self, parent=None, control_data=None):
        super().__init__(
            parent=parent,
            control_data=control_data,
            title="Spectrometer control config",
            control_type="Andor_Manual_Control",
        )
        control_data = control_data or {}
        select_label = QLabel("Spectrometer:")
        cam_label = QLabel("Camera:")

        self.spec_box = QComboBox()
        specs = []
        for name, device in variables_handling.devices.items():
            if device.name == "andor_shamrock_500":
                specs.append(name)
        self.spec_box.addItems(specs)
        if "spectrometer" in control_data and control_data["spectrometer"] in specs:
            self.spec_box.setCurrentText(control_data["spectrometer"])

        self.cam_box = QComboBox()
        cams = []
        for name, device in variables_handling.devices.items():
            cams.append(name)
        self.cam_box.addItems(cams)
        if "camera" in control_data and control_data["camera"] in cams:
            self.cam_box.setCurrentText(control_data["camera"])
        self.layout().addWidget(select_label, 2, 0)
        self.layout().addWidget(self.spec_box, 2, 1)
        self.layout().addWidget(cam_label, 3, 0)
        self.layout().addWidget(self.cam_box, 3, 1)

    def accept(self):
        self.control_data["spectrometer"] = self.spec_box.currentText()
        self.control_data["camera"] = self.cam_box.currentText()
        super().accept()
