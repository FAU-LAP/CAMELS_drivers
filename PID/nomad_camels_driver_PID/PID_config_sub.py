import pandas as pd

from PySide6.QtWidgets import (
    QGridLayout,
    QCheckBox,
    QComboBox,
    QLabel,
    QLineEdit,
    QHBoxLayout,
)

from nomad_camels.main_classes import device_class

from nomad_camels.ui_widgets.add_remove_table import AddRemoveTable
from nomad_camels.ui_widgets.path_button_edit import Path_Button_Edit
from nomad_camels.utility import variables_handling


class subclass_config_sub(device_class.Device_Config_Sub):
    def __init__(self, settings_dict=None, parent=None, config_dict=None):
        super().__init__(
            settings_dict=settings_dict, parent=parent, config_dict=config_dict
        )
        self.settings_dict = settings_dict
        self.config_dict = config_dict

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.checkBox_interpolate_auto = QCheckBox("Interpolate PID values")
        # self.checkBox_auto_select_values = QCheckBox('auto select values')
        self.comboBox_pid_vals = QComboBox()
        val_choice = ["Table", "File"]
        self.comboBox_pid_vals.addItems(val_choice)
        if "interpolate_auto" in config_dict:
            self.checkBox_interpolate_auto.setChecked(config_dict["interpolate_auto"])
        elif "interpolate_auto" in settings_dict:
            self.checkBox_interpolate_auto.setChecked(
                settings_dict.pop("interpolate_auto")
            )
        if "val_choice" in settings_dict and settings_dict["val_choice"] in val_choice:
            self.comboBox_pid_vals.setCurrentText(settings_dict.pop("val_choice"))
        self.file_box = Path_Button_Edit(self)
        if "val_file" in settings_dict:
            self.file_box.set_path(settings_dict.pop("val_file"))
        headerlabels = [
            "setpoint",
            "kp",
            "ki",
            "kd",
            "max_value",
            "min_value",
            "bias",
            "stability-delta",
            "stability-time",
        ]
        tableData = None
        if "pid_val_table" in config_dict:
            tableData = config_dict["pid_val_table"]
        elif "pid_val_table" in settings_dict:
            tableData = settings_dict.pop("pid_val_table")
        self.val_table = AddRemoveTable(
            editables=range(len(headerlabels)),
            headerLabels=headerlabels,
            parent=self,
            tableData=tableData,
        )

        self.input_label = QLabel("Input Channel:")
        self.output_label = QLabel("Output Channel:")
        self.bias_label = QLabel("Bias Channel:")
        self.timer_label = QLabel("Time Delta:")
        self.comboBox_input = QComboBox()
        self.comboBox_output = QComboBox()
        self.comboBox_bias = QComboBox()
        self.lineEdit_time = QLineEdit("1")
        self.comboBox_input.addItems(
            sorted(variables_handling.channels.keys(), key=lambda x: x.lower())
        )
        self.comboBox_bias.addItem("None")
        for chan in sorted(variables_handling.channels.keys(), key=lambda x: x.lower()):
            if variables_handling.channels[chan].output:
                self.comboBox_output.addItem(chan)
                self.comboBox_bias.addItem(chan)
        if (
            "read_signal_name" in settings_dict
            and type(settings_dict["read_signal_name"]) is str
        ):
            channel = settings_dict["read_signal_name"]
            if channel in variables_handling.channels:
                self.comboBox_input.setCurrentText(channel)
        if (
            "set_signal_name" in settings_dict
            and type(settings_dict["set_signal_name"]) is str
        ):
            channel = settings_dict["set_signal_name"]
            if channel in variables_handling.channels:
                self.comboBox_output.setCurrentText(channel)
        if (
            "bias_signal_name" in settings_dict
            and type(settings_dict["bias_signal_name"]) is str
        ):
            channel = settings_dict["bias_signal_name"]
            if channel in variables_handling.channels:
                self.comboBox_bias.setCurrentText(channel)
        if "dt" in config_dict:
            self.lineEdit_time.setText(str(config_dict["dt"]))
        self.read_label = QLabel("Conversion function for reading:")
        self.set_label = QLabel("Conversion function for setting:")
        read_conv = ""
        if "read_conversion_func" in config_dict:
            read_conv = str(config_dict["read_conversion_func"]) or ""
        elif "read_conv_func" in settings_dict:
            read_conv = str(settings_dict.pop("read_conv_func")) or ""
        set_conv = ""
        if "set_conversion_func" in config_dict:
            set_conv = str(config_dict["set_conversion_func"]) or ""
        elif "set_conv_func" in settings_dict:
            set_conv = str(settings_dict.pop("set_conv_func")) or ""

        conversion_items = ["No conversion", "Pt1000", "Pt100", "Custom", "From file"]

        custom_read_conv = ""
        if "custom_read_conv" in config_dict:
            custom_read_conv = config_dict["custom_read_conv"]
        custom_set_conv = ""
        if "custom_set_conv" in config_dict:
            custom_set_conv = config_dict["custom_set_conv"]
        read_conv_file = ""
        if "read_conv_file" in config_dict:
            read_conv_file = config_dict["read_conv_file"]
        set_conv_file = ""
        if "set_conv_file" in config_dict:
            set_conv_file = config_dict["set_conv_file"]

        read_layout = QHBoxLayout()
        read_layout.setContentsMargins(0, 0, 0, 0)

        self.lineEdit_read_function = QLineEdit(custom_read_conv)
        self.lineEdit_read_function.setToolTip(
            'Custom function evaluates for "x"\nIf "From file" is selected, give the name of the function here'
        )
        self.functions_read_file = Path_Button_Edit(self, path=read_conv_file)
        read_layout.addWidget(self.lineEdit_read_function)
        read_layout.addWidget(self.functions_read_file)
        self.comboBox_read_function = QComboBox()
        self.comboBox_read_function.addItems(conversion_items)
        self.comboBox_read_function.currentTextChanged.connect(
            self.read_function_changed
        )
        if read_conv in conversion_items:
            self.comboBox_read_function.setCurrentText(read_conv)
        self.read_function_changed()

        set_layout = QHBoxLayout()
        set_layout.setContentsMargins(0, 0, 0, 0)

        self.lineEdit_set_function = QLineEdit(custom_set_conv)
        self.lineEdit_set_function.setToolTip(
            'Custom function evaluates for "x"\nIf "From file" is selected, give the name of the function here'
        )
        self.functions_set_file = Path_Button_Edit(self, path=set_conv_file)
        set_layout.addWidget(self.lineEdit_set_function)
        set_layout.addWidget(self.functions_set_file)
        self.comboBox_set_function = QComboBox()
        self.comboBox_set_function.addItems(conversion_items)
        self.comboBox_set_function.currentTextChanged.connect(self.set_function_changed)
        if set_conv in conversion_items:
            self.comboBox_set_function.setCurrentText(set_conv)
        self.set_function_changed()

        self.checkBox_plot = QCheckBox("Plot PID values?")
        if "show_plot" in config_dict:
            self.checkBox_plot.setChecked(config_dict["show_plot"])
        elif "show_plot" in settings_dict:
            self.checkBox_plot.setChecked(settings_dict.pop("show_plot"))

        layout.addWidget(self.checkBox_plot, 0, 0, 1, 2)
        layout.addWidget(self.input_label, 1, 0)
        layout.addWidget(self.comboBox_input, 1, 1)
        layout.addWidget(self.output_label, 2, 0)
        layout.addWidget(self.comboBox_output, 2, 1)
        layout.addWidget(self.bias_label, 3, 0)
        layout.addWidget(self.comboBox_bias, 3, 1)

        layout.addWidget(self.read_label, 4, 0)
        layout.addWidget(self.comboBox_read_function, 4, 1)
        layout.addLayout(read_layout, 5, 0, 1, 2)

        layout.addWidget(self.set_label, 6, 0)
        layout.addWidget(self.comboBox_set_function, 6, 1)
        layout.addLayout(set_layout, 7, 0, 1, 2)

        layout.addWidget(self.timer_label, 10, 0)
        layout.addWidget(self.lineEdit_time, 10, 1)
        # layout.addWidget(self.checkBox_auto_select_values, 7, 0)
        layout.addWidget(self.checkBox_interpolate_auto, 11, 0, 1, 2)
        layout.addWidget(self.comboBox_pid_vals, 12, 0)
        layout.addWidget(self.file_box, 12, 1)
        layout.addWidget(self.val_table, 13, 0, 1, 2)

        # self.checkBox_auto_select_values.stateChanged.connect(self.auto_selection_switch)
        self.comboBox_pid_vals.currentTextChanged.connect(self.val_choice_switch)
        self.val_choice_switch()
        # self.auto_selection_switch()
        self.file_box.path_changed.connect(self.file_changed)

    def read_function_changed(self):
        text = self.comboBox_read_function.currentText()
        if text == "From file":
            self.functions_read_file.setHidden(False)
            self.lineEdit_read_function.setHidden(False)
        elif text == "Custom":
            self.functions_read_file.setHidden(True)
            self.lineEdit_read_function.setHidden(False)
        else:
            self.functions_read_file.setHidden(True)
            self.lineEdit_read_function.setHidden(True)

    def set_function_changed(self):
        text = self.comboBox_set_function.currentText()
        if text == "From file":
            self.functions_set_file.setHidden(False)
            self.lineEdit_set_function.setHidden(False)
        elif text == "Custom":
            self.functions_set_file.setHidden(True)
            self.lineEdit_set_function.setHidden(False)
        else:
            self.functions_set_file.setHidden(True)
            self.lineEdit_set_function.setHidden(True)

    def val_choice_switch(self):
        table = self.comboBox_pid_vals.currentText() == "Table"
        if not table:
            self.file_changed()
        self.file_box.setEnabled(not table)
        self.val_table.setEnabled(table)

    def file_changed(self):
        try:
            df = pd.read_csv(self.file_box.get_path(), delimiter="\t")
            self.val_table.tableData = df
            self.val_table.load_table_data()
        except Exception as e:
            print(e)

    def get_settings(self):
        self.settings_dict["val_choice"] = self.comboBox_pid_vals.currentText()
        self.settings_dict["val_file"] = self.file_box.get_path()
        bias_text = "None"
        if variables_handling.channels:
            inp_chan = variables_handling.channels[self.comboBox_input.currentText()]
            out_chan = variables_handling.channels[self.comboBox_output.currentText()]
            self.settings_dict["!non_string!_read_signal"] = inp_chan.get_bluesky_name()
            self.settings_dict["!non_string!_set_signal"] = out_chan.get_bluesky_name()
            bias_text = self.comboBox_bias.currentText()
            if bias_text != "None":
                bias_chan = variables_handling.channels[bias_text]
                self.settings_dict["!non_string!_bias_signal"] = (
                    bias_chan.get_bluesky_name()
                )
            else:
                self.settings_dict["!non_string!_bias_signal"] = None
        self.settings_dict["read_signal_name"] = self.comboBox_input.currentText()
        self.settings_dict["set_signal_name"] = self.comboBox_output.currentText()
        if bias_text == "None":
            self.settings_dict["bias_signal_name"] = None
        else:
            self.settings_dict["bias_signal_name"] = bias_text
        return self.settings_dict

    def get_config(self):
        self.config_dict["pid_val_table"] = self.val_table.update_table_data()
        self.config_dict["dt"] = float(self.lineEdit_time.text())
        self.config_dict["set_conversion_func"] = (
            self.comboBox_set_function.currentText()
        )
        self.config_dict["read_conversion_func"] = (
            self.comboBox_read_function.currentText()
        )
        self.config_dict["custom_set_conv"] = self.lineEdit_set_function.text()
        self.config_dict["custom_read_conv"] = self.lineEdit_read_function.text()
        self.config_dict["set_conv_file"] = self.functions_set_file.get_path()
        self.config_dict["read_conv_file"] = self.functions_read_file.get_path()
        self.config_dict["interpolate_auto"] = (
            self.checkBox_interpolate_auto.isChecked()
        )
        self.config_dict["show_plot"] = self.checkBox_plot.isChecked()
        return self.config_dict

    def hide_settings(self):
        self.comboBox_bias.hide()
        self.bias_label.hide()
        self.comboBox_input.hide()
        self.input_label.hide()
        self.comboBox_output.hide()
        self.output_label.hide()
