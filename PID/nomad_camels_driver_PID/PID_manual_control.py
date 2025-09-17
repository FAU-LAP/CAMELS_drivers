import time

from nomad_camels.main_classes.manual_control import (
    Manual_Control,
    Manual_Control_Config,
)
from .PID_config_sub import subclass_config_sub
from .PID_ophyd  import PID_Controller

from PySide6.QtWidgets import (
    QCheckBox,
    QLineEdit,
    QPushButton,
    QLabel,
    QSpacerItem,
    QSizePolicy,
    QFrame,
    QComboBox,
    QGridLayout,
)
from PySide6.QtCore import Signal, QThread

from nomad_camels.utility import variables_handling, device_handling


class PID_manual_control(Manual_Control):
    ophyd_device: PID_Controller
    def __init__(self, parent=None, control_data=None):
        control_data = control_data or {}
        if "name" in control_data:
            name = control_data["name"]
        else:
            name = "PID manual control"
        super().__init__(parent=parent, title=name)
        self.setLayout(QGridLayout())
        self.update_thread = None
        self.start_device(control_data["pid_name"])

    def device_ready(self):
        super().device_ready()
        self.settings_widge = subclass_config_sub(
            settings_dict=self.device.settings,
            config_dict=self.device.config,
            parent=self,
        )
        self.settings_widge.hide_settings()
        self.settings_widge.checkBox_plot.setHidden(True)

        label_state = QLabel("current state:")
        self.on_off_box = QCheckBox("Off")
        label_set = QLabel("Setpoint:")
        self.lineEdit_setpoint = QLineEdit(str(self.ophyd_device.setpoint.get()))
        self.lineEdit_setpoint_show = QLineEdit(str(self.ophyd_device.setpoint.get()))
        self.lineEdit_setpoint_show.setEnabled(False)
        label_pidval = QLabel("Actual value:")
        self.lineEdit_pid_val = QLineEdit(str(self.ophyd_device.current_value.get()))
        self.lineEdit_pid_val.setEnabled(False)
        label_output = QLabel("Output:")
        self.lineEdit_output = QLineEdit(str(self.ophyd_device.output_value.get()))
        self.lineEdit_output.setEnabled(False)

        label_update = QLabel("Update speed:")
        self.lineEdit_update = QLineEdit(str(self.ophyd_device.dt.get()))

        self.ramp_box = QCheckBox("Use Ramp?")
        label_ramp_to = QLabel("Ramp to:")
        self.lineEdit_ramp_to = QLineEdit(str(self.ophyd_device.ramp_to.get()))
        self.lineEdit_ramp_to_show = QLineEdit(str(self.ophyd_device.ramp_to.get()))
        self.lineEdit_ramp_to_show.setEnabled(False)
        label_ramp_speed = QLabel("Ramp speed (1/s):")
        self.lineEdit_ramp_speed = QLineEdit(str(self.ophyd_device.ramp_speed.get()))
        self.lineEdit_ramp_speed_show = QLineEdit(
            str(self.ophyd_device.ramp_speed.get())
        )
        self.lineEdit_ramp_speed_show.setEnabled(False)

        self.pushButton_plot = QPushButton("Show Plot")
        self.pushButton_settings = QPushButton("Show Settings")
        self.pushButton_update_settings = QPushButton("Update Settings")

        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line2 = QFrame(self)
        line2.setFrameShape(QFrame.HLine)
        line2.setFrameShadow(QFrame.Sunken)

        spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.layout().addWidget(label_state, 0, 0)
        self.layout().addWidget(self.on_off_box, 1, 0, 2, 1)
        self.layout().addWidget(label_set, 0, 1)
        self.layout().addWidget(self.lineEdit_setpoint, 1, 1)
        self.layout().addWidget(self.lineEdit_setpoint_show, 2, 1)
        self.layout().addWidget(label_pidval, 0, 2)
        self.layout().addWidget(self.lineEdit_pid_val, 1, 2, 2, 1)
        self.layout().addWidget(label_output, 0, 3)
        self.layout().addWidget(self.lineEdit_output, 1, 3, 2, 1)
        self.layout().addWidget(label_update, 0, 4)
        self.layout().addWidget(self.lineEdit_update, 1, 4, 2, 1)

        self.layout().addWidget(line, 5, 0, 1, 5)
        self.layout().addWidget(self.ramp_box, 6, 0, 2, 1)
        self.layout().addWidget(label_ramp_to, 6, 1, 1, 2)
        self.layout().addWidget(self.lineEdit_ramp_to, 7, 1)
        self.layout().addWidget(self.lineEdit_ramp_to_show, 7, 2)
        self.layout().addWidget(label_ramp_speed, 6, 3, 1, 2)
        self.layout().addWidget(self.lineEdit_ramp_speed, 7, 3)
        self.layout().addWidget(self.lineEdit_ramp_speed_show, 7, 4)
        self.layout().addWidget(line2, 8, 0, 1, 5)

        self.layout().addWidget(self.pushButton_plot, 9, 0, 1, 2)
        self.layout().addWidget(self.pushButton_settings, 9, 2, 1, 3)
        self.layout().addWidget(self.settings_widge, 10, 0, 1, 5)
        self.layout().addWidget(self.pushButton_update_settings, 11, 3, 1, 2)
        self.layout().addItem(spacer, 20, 0)

        self.settings_widge.setHidden(True)
        self.pushButton_update_settings.setHidden(True)

        self.on_off_box.clicked.connect(self.change_state)
        self.pushButton_settings.clicked.connect(self.show_settings)
        self.pushButton_update_settings.clicked.connect(self.update_settings)
        self.lineEdit_update.returnPressed.connect(self.change_update_time)
        self.lineEdit_setpoint.returnPressed.connect(self.change_setpoint)
        self.pushButton_plot.clicked.connect(self.change_show_plot)
        self.ramp_box.clicked.connect(self.change_ramp_state)
        self.lineEdit_ramp_speed.returnPressed.connect(self.change_ramp_speed)
        self.lineEdit_ramp_to.returnPressed.connect(self.change_ramp_to)

        return_tooltip = (
            "Attention!\nYou need to press Enter in order for changes to take effect."
        )
        self.lineEdit_setpoint.setToolTip(return_tooltip)
        self.lineEdit_update.setToolTip(return_tooltip)
        self.lineEdit_ramp_to.setToolTip(return_tooltip)
        self.lineEdit_ramp_speed.setToolTip(return_tooltip)

        self.change_show_plot()
        self.change_show_plot()

        self.update_thread = PID_update_thread(self, self.ophyd_device)
        self.update_thread.data_sig.connect(self.data_update)
        self.update_thread.start()

        self.sub_devices = []
        for dev in self.device_list:
            if dev in device_handling.running_devices:
                self.sub_devices.append(device_handling.running_devices[dev])
        self.adjustSize()

    def change_show_plot(self):
        showing = self.ophyd_device.plot.livePlot.show_plot
        self.ophyd_device.show_plot.put(not showing)
        if showing:
            self.pushButton_plot.setText("show plot")
        else:
            self.pushButton_plot.setText("hide plot")

    def update_settings(self):
        table = self.settings_widge.val_table.update_table_data()
        self.ophyd_device.pid_val_table.put(table)
        self.ophyd_device._configuring = True
        self.ophyd_device.interpolate_auto.put(
            self.settings_widge.checkBox_interpolate_auto.isChecked()
        )
        self.ophyd_device.read_conversion_func.put(
            self.settings_widge.comboBox_read_function.currentText()
        )
        self.ophyd_device.set_conversion_func.put(
            self.settings_widge.comboBox_set_function.currentText()
        )
        self.ophyd_device.custom_read_conv.put(
            self.settings_widge.lineEdit_read_function.text()
        )
        self.ophyd_device.custom_set_conv.put(
            self.settings_widge.lineEdit_set_function.text()
        )
        self.ophyd_device.set_conv_file.put(
            self.settings_widge.functions_set_file.get_path()
        )
        self.ophyd_device.read_conv_file.put(
            self.settings_widge.functions_read_file.get_path()
        )
        self.ophyd_device._configuring = False
        self.ophyd_device.update_read_conv_func()
        self.ophyd_device.update_set_conv_func()
        self.ophyd_device.update_PID_vals(float(self.lineEdit_setpoint.text()))

    def data_update(self, setp, pid_val, output, on, ramp_on, ramp_to, ramp_speed):
        self.lineEdit_setpoint_show.setText(f"{setp:.3e}")
        self.lineEdit_pid_val.setText(f"{pid_val:.3e}")
        self.lineEdit_output.setText(f"{output:.3e}")
        self.lineEdit_ramp_to_show.setText(f"{ramp_to:.3e}")
        self.lineEdit_ramp_speed_show.setText(f"{ramp_speed:.3e}")
        self.ramp_box.setChecked(ramp_on)
        self.change_on_state(on)

    def change_setpoint(self):
        setp = float(self.lineEdit_setpoint.text())
        self.ophyd_device.setpoint.put(setp)
        # self.run_thread.device.pid_val.put(setp)

    def change_update_time(self):
        self.ophyd_device.dt.put(float(self.lineEdit_update.text()))
        # self.run_thread.update_time = float(self.lineEdit_update.text())

    def change_on_state(self, on):
        self.on_off_box.setChecked(on)
        col = variables_handling.get_color("dark_green" if on else "strong_red", True)
        self.on_off_box.setText("On" if on else "Off")
        self.on_off_box.setStyleSheet(f"color: rgb{col}")

    def change_ramp_state(self):
        ramp_on = self.ramp_box.isChecked()
        self.ophyd_device.ramp_on.put(ramp_on)

    def change_ramp_speed(self):
        self.ophyd_device.ramp_speed.put(float(self.lineEdit_ramp_speed.text()))

    def change_ramp_to(self):
        self.ophyd_device.ramp_to.put(float(self.lineEdit_ramp_to.text()))

    def change_state(self):
        on = self.on_off_box.isChecked()
        if on:
            for dev in self.sub_devices:
                if hasattr(dev, "turn_on_output") and callable(dev.turn_on_output):
                    dev.turn_on_output()
        col = variables_handling.get_color("dark_green" if on else "strong_red", True)
        self.on_off_box.setText("On" if on else "Off")
        self.on_off_box.setStyleSheet(f"color: rgb{col}")
        self.ophyd_device.pid_on.put(on)

    def show_settings(self):
        hidden = self.settings_widge.isHidden()
        self.settings_widge.setHidden(not hidden)
        self.pushButton_update_settings.setHidden(not hidden)
        if hidden:
            self.pushButton_settings.setText("Hide Settings")
        else:
            self.pushButton_settings.setText("Show Settings")
        self.adjustSize()

    def close(self) -> bool:
        if self.update_thread is not None:
            self.update_thread.still_running = False
        return super().close()

    def closeEvent(self, a0) -> None:
        if self.update_thread is not None:
            self.update_thread.still_running = False
        return super().closeEvent(a0)


class PID_Manual_Control_Config(Manual_Control_Config):
    def __init__(self, parent=None, control_data=None):
        super().__init__(
            parent=parent,
            control_data=control_data,
            title="PID Control Config",
            control_type="PID_manual_control",
        )
        control_data = control_data or {}
        select_label = QLabel("PID Controller:")

        self.pid_box = QComboBox()
        pids = []
        for name, device in variables_handling.devices.items():
            if device.name == "PID":
                pids.append(name)
        self.pid_box.addItems(pids)
        if "pid_name" in control_data and control_data["pid_name"] in pids:
            self.pid_box.setCurrentText(control_data["pid_name"])
        self.layout().addWidget(select_label, 2, 0)
        self.layout().addWidget(self.pid_box, 2, 1)

    def accept(self):
        self.control_data["pid_name"] = self.pid_box.currentText()
        super().accept()


class PID_update_thread(QThread):
    data_sig = Signal(float, float, float, bool, bool, float, float)

    def __init__(self, parent=None, device=None):
        super().__init__(parent=parent)
        self.device = device
        self.update_time = device.dt.get()
        self.stopping = False
        self.starttime = 0.0
        self.still_running = True

    def run(self):
        self.starttime = time.time()
        self.do_reading()
        while self.still_running:
            if self.update_time < 0.0:
                time.sleep(5)
                continue
            time.sleep(self.update_time)
            self.do_reading()

    def do_reading(self):
        setp = self.device.setpoint.get()
        pid_val = self.device.current_value.get()
        output = self.device.output_value.get()
        on = bool(self.device.pid_on.get())
        ramp_on = bool(self.device.ramp_on.get())
        ramp_to = self.device.ramp_to.get()
        ramp_speed = self.device.ramp_speed.get()
        self.data_sig.emit(setp, pid_val, output, on, ramp_on, ramp_to, ramp_speed)
