from .swabianinstruments_timetagger_ophyd import TimeTagger
from nomad_camels.main_classes import device_class

from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QLineEdit,
    QCheckBox,
    QLabel,
    QPushButton,
    QTabWidget,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

import TimeTagger as TT

bold_font = QFont()
bold_font.setBold(True)


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="swabianinstruments_timetagger",
            virtual=False,
            ophyd_device=TimeTagger,
            ophyd_class_name="TimeTagger",
            **kwargs,
        )
        self.settings["serial_number"] = ""
        self.config["countrate_time"] = 1
        self.config["countrate_channels"] = "0 1"

        self.config["correlation_channel_1"] = 0
        self.config["correlation_channel_2"] = 1
        self.config["correlation_binwidth"] = 400
        self.config["correlation_bins"] = 1000
        self.config["correlation_meas_time"] = 1

        self.config["cbm_click_channel"] = 0
        self.config["cbm_begin_channel"] = 1
        self.config["cbm_end_channel"] = 2
        self.config["cbm_n_values"] = 1000
        self.config["cbm_meas_time"] = 1


class subclass_config(device_class.Simple_Config):
    """
    Automatically creates a GUI for the configuration values given here.
    This is perfect for simple devices with just a few settings.
    """

    def __init__(
        self,
        parent=None,
        data="",
        settings_dict=None,
        config_dict=None,
        additional_info=None,
    ):
        comboboxes = {"serial_number": TT.scanTimeTagger()}
        if "channels" in settings_dict:
            channels = settings_dict.pop("channels")
        else:
            channels = {}
        super().__init__(
            parent,
            "SwabianInstruments TimeTagger",
            data,
            settings_dict,
            config_dict,
            additional_info,
            comboBoxes=comboboxes,
            labels=None,
        )
        self.settings_dict["channels"] = channels
        self.pushButton_update_tagger = QPushButton("update available channels")
        self.pushButton_update_tagger.clicked.connect(self.get_tagger_channels)
        self.layout().addWidget(self.pushButton_update_tagger, 20, 0, 1, 5)
        self.channel_tabs = QTabWidget()
        self.layout().addWidget(self.channel_tabs, 21, 0, 1, 5)
        self.tabs = []
        self.channels = []
        self.get_tagger_channels()
        self.load_settings()

    def get_tagger_channels(self):
        self.setCursor(Qt.WaitCursor)
        sn = self.sub_widget.setting_combos["serial_number"].currentText()
        try:
            tagger = TT.createTimeTagger(serial=sn)
            channels = tagger.getChannelList()
            TT.freeTimeTagger(tagger)
            self.channels = channels
        except:
            self.setCursor(Qt.ArrowCursor)
            return
        negatives = False
        if not channels:
            return
        if min(channels) < 0:
            negatives = True
        self.tabs.clear()
        for i, channel in enumerate(channels):
            if (negatives and channel < 0) or (
                not negatives and i >= int(len(channels) / 2)
            ):
                continue
            settings = None
            settings_fall = None
            if str(channel) in self.settings_dict["channels"]:
                settings = self.settings_dict["channels"][str(channel)]
            if negatives and str(-1 * channel) in self.settings_dict["channels"]:
                settings_fall = self.settings_dict["channels"][str(-1 * channel)]
            elif (
                not negatives
                and str(int(channel + len(channels) / 2))
                in self.settings_dict["channels"]
            ):
                settings_fall = self.settings_dict["channels"][
                    str(int(channel + len(channels) / 2))
                ]
            tab = Channel_Settings(self, settings, settings_fall, channel)
            self.channel_tabs.addTab(tab, f"channel {channel}")
            self.tabs.append(tab)
        self.setCursor(Qt.ArrowCursor)

    def get_settings(self):
        settings = super().get_settings()
        settings["channels"].clear()
        negatives = False
        if not self.channels:
            return settings
        if min(self.channels) < 0:
            negatives = True
        for i, channel in enumerate(self.channels):
            if (negatives and channel < 0) or (
                not negatives and i >= int(len(self.channels) / 2)
            ):
                continue
            sets, sets_fall = self.tabs[i].get_settings()
            settings["channels"][str(channel)] = sets
            f_channel = (
                -1 * channel if negatives else int(channel + len(self.channels) / 2)
            )
            settings["channels"][str(f_channel)] = sets_fall
        return settings


class Channel_Settings(QWidget):
    def __init__(
        self, parent=None, settings=None, settings_fall=None, channel_number=0
    ):
        super().__init__(parent)
        layout = QGridLayout()
        self.setLayout(layout)
        settings = settings or {}
        settings_fall = settings_fall or {}
        label_main = QLabel(f"Channel {channel_number}")
        label_main.setFont(bold_font)
        layout.addWidget(label_main, 0, 0)

        label_dead_time = QLabel("dead time (ps)")
        label_input_delay = QLabel("input delay (ps)")
        label_trigger_level = QLabel("trigger level (V)")
        label_rising_edge = QLabel("rising edge")
        label_rising_edge.setFont(bold_font)

        self.line_dead_time = QLineEdit(str(6000))
        if "dead_time" in settings:
            self.line_dead_time.setText(str(settings["dead_time"]))
        self.line_input_delay = QLineEdit(str(0))
        if "input_delay" in settings:
            self.line_input_delay.setText(str(settings["input_delay"]))
        self.line_trigger_level = QLineEdit(str(0.5))
        if "trigger_level" in settings:
            self.line_trigger_level.setText(str(settings["trigger_level"]))

        self.check_test_signal = QCheckBox("test signal")
        if "test_signal" in settings:
            self.check_test_signal.setChecked(settings["test_signal"])

        layout.addWidget(label_rising_edge, 11, 0, 1, 2)
        layout.addWidget(label_trigger_level, 10, 0)
        layout.addWidget(self.line_trigger_level, 10, 1)
        layout.addWidget(label_dead_time, 12, 0)
        layout.addWidget(self.line_dead_time, 12, 1)
        layout.addWidget(label_input_delay, 13, 0)
        layout.addWidget(self.line_input_delay, 13, 1)
        layout.addWidget(self.check_test_signal, 0, 1)

        label_dead_time = QLabel("dead time (ps)")
        label_input_delay = QLabel("input delay (ps)")
        label_falling_edge = QLabel("falling edge")
        label_falling_edge.setFont(bold_font)

        self.line_dead_time_fall = QLineEdit(str(6000))
        if "dead_time" in settings_fall:
            self.line_dead_time_fall.setText(str(settings_fall["dead_time"]))
        self.line_input_delay_fall = QLineEdit(str(0))
        if "input_delay" in settings_fall:
            self.line_input_delay_fall.setText(str(settings_fall["input_delay"]))

        layout.addWidget(label_falling_edge, 20, 0, 1, 2)
        layout.addWidget(label_dead_time, 22, 0)
        layout.addWidget(self.line_dead_time_fall, 22, 1)
        layout.addWidget(label_input_delay, 23, 0)
        layout.addWidget(self.line_input_delay_fall, 23, 1)

    def get_settings(self):
        settings = {}
        settings_fall = {}
        settings["trigger_level"] = float(self.line_trigger_level.text())
        settings["dead_time"] = int(self.line_dead_time.text())
        settings["input_delay"] = int(self.line_input_delay.text())
        settings["test_signal"] = self.check_test_signal.isChecked()
        settings_fall["trigger_level"] = float(self.line_trigger_level.text())
        settings_fall["dead_time"] = int(self.line_dead_time_fall.text())
        settings_fall["input_delay"] = int(self.line_input_delay_fall.text())
        settings_fall["test_signal"] = self.check_test_signal.isChecked()
        return settings, settings_fall
