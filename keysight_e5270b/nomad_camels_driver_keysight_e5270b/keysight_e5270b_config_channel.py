# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'keysight_e5270b_config_channel.ui'
#
# Created by: PySide6 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide6 import QtCore, QtGui, QtWidgets


class Ui_keysight_e5270b_config_channel(object):
    def setupUi(self, keysight_e5270b_config_channel):
        keysight_e5270b_config_channel.setObjectName("keysight_e5270b_config_channel")
        keysight_e5270b_config_channel.resize(451, 200)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            keysight_e5270b_config_channel.sizePolicy().hasHeightForWidth()
        )
        keysight_e5270b_config_channel.setSizePolicy(sizePolicy)
        keysight_e5270b_config_channel.setMaximumSize(QtCore.QSize(16777215, 200))
        self.gridLayout = QtWidgets.QGridLayout(keysight_e5270b_config_channel)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit_currComp = QtWidgets.QLineEdit(keysight_e5270b_config_channel)
        self.lineEdit_currComp.setObjectName("lineEdit_currComp")
        self.gridLayout.addWidget(self.lineEdit_currComp, 4, 1, 1, 1)
        self.lineEdit_voltComp = QtWidgets.QLineEdit(keysight_e5270b_config_channel)
        self.lineEdit_voltComp.setObjectName("lineEdit_voltComp")
        self.gridLayout.addWidget(self.lineEdit_voltComp, 4, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(keysight_e5270b_config_channel)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 4, 2, 1, 1)
        self.comboBox_currMeasRange = QtWidgets.QComboBox(
            keysight_e5270b_config_channel
        )
        self.comboBox_currMeasRange.setObjectName("comboBox_currMeasRange")
        self.gridLayout.addWidget(self.comboBox_currMeasRange, 6, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(keysight_e5270b_config_channel)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 5, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(keysight_e5270b_config_channel)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 5, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(keysight_e5270b_config_channel)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(QtGui.QFont.Weight(75))
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 2)
        self.label_7 = QtWidgets.QLabel(keysight_e5270b_config_channel)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 6, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(keysight_e5270b_config_channel)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(QtGui.QFont.Weight(75))
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 2, 1, 2)
        self.label = QtWidgets.QLabel(keysight_e5270b_config_channel)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(keysight_e5270b_config_channel)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 6, 2, 1, 1)
        self.comboBox_voltRange = QtWidgets.QComboBox(keysight_e5270b_config_channel)
        self.comboBox_voltRange.setObjectName("comboBox_voltRange")
        self.gridLayout.addWidget(self.comboBox_voltRange, 5, 1, 1, 1)
        self.comboBox_voltMeasRange = QtWidgets.QComboBox(
            keysight_e5270b_config_channel
        )
        self.comboBox_voltMeasRange.setObjectName("comboBox_voltMeasRange")
        self.gridLayout.addWidget(self.comboBox_voltMeasRange, 6, 3, 1, 1)
        self.comboBox_currRange = QtWidgets.QComboBox(keysight_e5270b_config_channel)
        self.comboBox_currRange.setObjectName("comboBox_currRange")
        self.gridLayout.addWidget(self.comboBox_currRange, 5, 3, 1, 1)
        self.radioButton_highSpeedADC = QtWidgets.QRadioButton(
            keysight_e5270b_config_channel
        )
        self.radioButton_highSpeedADC.setObjectName("radioButton_highSpeedADC")
        self.gridLayout.addWidget(self.radioButton_highSpeedADC, 1, 2, 1, 1)
        self.checkBox_outputFilter = QtWidgets.QCheckBox(keysight_e5270b_config_channel)
        self.checkBox_outputFilter.setObjectName("checkBox_outputFilter")
        self.gridLayout.addWidget(self.checkBox_outputFilter, 2, 0, 1, 1)
        self.radioButton_highResADC = QtWidgets.QRadioButton(
            keysight_e5270b_config_channel
        )
        self.radioButton_highResADC.setChecked(True)
        self.radioButton_highResADC.setObjectName("radioButton_highResADC")
        self.gridLayout.addWidget(self.radioButton_highResADC, 2, 2, 1, 1)
        self.checkBox_channel_active = QtWidgets.QCheckBox(
            keysight_e5270b_config_channel
        )
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(QtGui.QFont.Weight(75))
        self.checkBox_channel_active.setFont(font)
        self.checkBox_channel_active.setObjectName("checkBox_channel_active")
        self.gridLayout.addWidget(self.checkBox_channel_active, 1, 0, 1, 1)

        self.retranslateUi(keysight_e5270b_config_channel)
        QtCore.QMetaObject.connectSlotsByName(keysight_e5270b_config_channel)

    def retranslateUi(self, keysight_e5270b_config_channel):
        _translate = QtCore.QCoreApplication.translate
        keysight_e5270b_config_channel.setWindowTitle(
            _translate("keysight_e5270b_config_channel", "Form")
        )
        self.label_2.setText(
            _translate("keysight_e5270b_config_channel", "Voltage Compliance")
        )
        self.label_5.setText(
            _translate("keysight_e5270b_config_channel", "Voltage Range")
        )
        self.label_6.setText(
            _translate("keysight_e5270b_config_channel", "Current Range")
        )
        self.label_3.setText(
            _translate("keysight_e5270b_config_channel", "Voltage Source")
        )
        self.label_7.setText(
            _translate("keysight_e5270b_config_channel", "Current Measurement Range")
        )
        self.label_4.setText(
            _translate("keysight_e5270b_config_channel", "Current Source")
        )
        self.label.setText(
            _translate("keysight_e5270b_config_channel", "Current Compliance")
        )
        self.label_8.setText(
            _translate("keysight_e5270b_config_channel", "Voltage Measurement Range")
        )
        self.radioButton_highSpeedADC.setText(
            _translate("keysight_e5270b_config_channel", "High Speed ADC")
        )
        self.checkBox_outputFilter.setText(
            _translate("keysight_e5270b_config_channel", "Output Filter")
        )
        self.radioButton_highResADC.setText(
            _translate("keysight_e5270b_config_channel", "High Res ADC")
        )
        self.checkBox_channel_active.setText(
            _translate("keysight_e5270b_config_channel", "Channel active")
        )
