from PySide6.QtCore import Qt
from .cryovac_tic_500_ophyd import Cryovac_TIC_500

from nomad_camels.main_classes import device_class

from PySide6.QtWidgets import QGridLayout, QLabel, QLineEdit, QWidget, QCheckBox, QComboBox



class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="cryovac_tic_500",
            virtual=False,
            tags=["DMM", "voltage", "current"],
            ophyd_device=Cryovac_TIC_500,
            ophyd_class_name="Cryovac_TIC_500",
            **kwargs
        )
        self.settings['channels_in'] = []
        self.settings['channels_out'] = []

    def get_settings(self):
        return super().get_settings()


    def get_channels(self):
        channels = dict(super().get_channels())
        if not self.settings:
            return channels
        removes = []
        for i, setting in enumerate(self.settings['channels_in']):
            if not setting['use']:
                for key in channels:
                    if key.endswith(f'input_{i+1}'):
                        removes.append(key)
        for i, setting in enumerate(self.settings['channels_out']):
            if not setting['use']:
                for key in channels:
                    if key.endswith(f'output_{i+1}') or key.endswith(f'enable_pid_{i+1}'):
                        removes.append(key)
            elif not setting['is_pid']:
                for key in channels:
                    if key.endswith(f'enable_pid_{i+1}'):
                        removes.append(key)
        for r in removes:
            channels.pop(r)
        return channels



class subclass_config(device_class.Device_Config):
    def __init__(
        self,
        parent=None,
        data="",
        settings_dict=None,
        config_dict=None,
        additional_info=None,
    ):
        super().__init__(
            parent,
            "Agilent 34401",
            data,
            settings_dict,
            config_dict,
            additional_info,
        )
        # self.comboBox_connection_type.addItem("Local VISA")
        self.load_settings()
        label_resource = QLabel('Resource Name')
        self.lineEdit_resource = QLineEdit()
        if "resource_name" in settings_dict:
            self.lineEdit_resource.setText(settings_dict['resource_name'])
        self.layout().addWidget(label_resource, 9, 0, 1, 2)
        self.layout().addWidget(self.lineEdit_resource, 9, 2, 1, 3)
        
        self.in_widgets = []
        self.out_widgets = []
        self.layout().addWidget(QLabel('Input Channels'), 10, 0, 1, 2)
        self.layout().addWidget(QLabel('Output Channels'), 10, 2, 1, 3)
        for i in range(4):
            if i < len(self.settings_dict['channels_in']):
                settings_dict = self.settings_dict['channels_in'][i]
            else:
                settings_dict = {}
            widget = Channel_Config(self, settings_dict, is_input=True)
            self.layout().addWidget(widget, i+11, 0, 1, 2)
            self.in_widgets.append(widget)
            
            if i < len(self.settings_dict['channels_out']):
                settings_dict = self.settings_dict['channels_out'][i]
            else:
                settings_dict = {}
            widget = Channel_Config(self, settings_dict, is_input=False)
            self.layout().addWidget(widget, i+11, 2, 1, 3)
            self.out_widgets.append(widget)
        
    def get_settings(self):
        settings_dict = super().get_settings()
        settings_dict['channels_in'] = [widget.get_config() for widget in self.in_widgets]
        settings_dict['channels_out'] = [widget.get_config() for widget in self.out_widgets]
        settings_dict['resource_name'] = self.lineEdit_resource.text()
        return settings_dict



class Channel_Config(QWidget):
    def __init__(self, parent=None, settings_dict=None, is_input=True):
        super().__init__(parent)
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        settings_dict = settings_dict or {}
        
        self.is_input = is_input
        
        self.use_box = QCheckBox("Use")
        if 'use' in settings_dict:
            self.use_box.setChecked(settings_dict['use'])
        self.use_box.stateChanged.connect(self.use_changed)
        
        self.label_name = QLabel('Name')
        self.line_name = QLineEdit()
        if 'name' in settings_dict:
            self.line_name.setText(settings_dict['name'])

        self.is_pid_box = QCheckBox("PID?")
        if 'is_pid' in settings_dict:
            self.is_pid_box.setChecked(settings_dict['is_pid'])


        layout.addWidget(self.use_box, 0, 0)
        layout.addWidget(self.label_name, 1, 0)
        layout.addWidget(self.line_name, 1, 1)
        layout.addWidget(self.is_pid_box, 2, 1)

        self.use_changed()
    
    def use_changed(self):
        in_use = self.use_box.isChecked()
        self.label_name.setHidden(not in_use)
        self.line_name.setHidden(not in_use)
        self.is_pid_box.setHidden(not in_use or self.is_input)
        self.adjustSize()

    def get_config(self):
        return {
            'use': self.use_box.isChecked(),
            'name': self.line_name.text(),
            'is_pid': self.is_pid_box.isChecked()
        }



        
