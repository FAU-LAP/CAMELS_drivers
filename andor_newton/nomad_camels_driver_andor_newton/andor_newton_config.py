# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'andor_newton_config.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QDoubleSpinBox,
    QFrame, QGridLayout, QLabel, QLineEdit,
    QSizePolicy, QSpacerItem, QSpinBox, QWidget)

class Ui_andor_newton_config(object):
    def setupUi(self, andor_newton_config):
        if not andor_newton_config.objectName():
            andor_newton_config.setObjectName(u"andor_newton_config")
        andor_newton_config.resize(377, 283)
        self.gridLayout = QGridLayout(andor_newton_config)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame_5 = QFrame(andor_newton_config)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_5)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_15 = QLabel(self.frame_5)
        self.label_15.setObjectName(u"label_15")
        font = QFont()
        font.setPointSize(9)
        font.setBold(True)
        self.label_15.setFont(font)

        self.gridLayout_5.addWidget(self.label_15, 0, 0, 1, 1)

        self.set_temperature = QSpinBox(self.frame_5)
        self.set_temperature.setObjectName(u"set_temperature")
        self.set_temperature.setMinimum(-99)
        self.set_temperature.setValue(-60)

        self.gridLayout_5.addWidget(self.set_temperature, 1, 0, 1, 1)

        self.lineEdit_current_temperature = QLineEdit(self.frame_5)
        self.lineEdit_current_temperature.setObjectName(u"lineEdit_current_temperature")
        self.lineEdit_current_temperature.setEnabled(False)

        self.gridLayout_5.addWidget(self.lineEdit_current_temperature, 2, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_5, 0, 0, 1, 1)

        self.frame = QFrame(andor_newton_config)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setFont(font)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.comboBox_shutter_mode = QComboBox(self.frame)
        self.comboBox_shutter_mode.addItem("")
        self.comboBox_shutter_mode.addItem("")
        self.comboBox_shutter_mode.addItem("")
        self.comboBox_shutter_mode.setObjectName(u"comboBox_shutter_mode")

        self.gridLayout_2.addWidget(self.comboBox_shutter_mode, 2, 0, 1, 1)

        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 3, 0, 1, 1)

        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 1, 0, 1, 1)

        self.exposure_time = QDoubleSpinBox(self.frame)
        self.exposure_time.setObjectName(u"exposure_time")
        self.exposure_time.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.exposure_time.setDecimals(3)
        self.exposure_time.setSingleStep(0.100000000000000)

        self.gridLayout_2.addWidget(self.exposure_time, 4, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 1, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 2, 0, 1, 1)

        self.frame_3 = QFrame(andor_newton_config)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.preamp_gain = QSpinBox(self.frame_3)
        self.preamp_gain.setObjectName(u"preamp_gain")
        self.preamp_gain.setValue(4)

        self.gridLayout_4.addWidget(self.preamp_gain, 4, 0, 1, 1)

        self.label_8 = QLabel(self.frame_3)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_4.addWidget(self.label_8, 1, 0, 1, 1)

        self.comboBox_readout_mode = QComboBox(self.frame_3)
        self.comboBox_readout_mode.addItem("")
        self.comboBox_readout_mode.addItem("")
        self.comboBox_readout_mode.addItem("")
        self.comboBox_readout_mode.addItem("")
        self.comboBox_readout_mode.setObjectName(u"comboBox_readout_mode")

        self.gridLayout_4.addWidget(self.comboBox_readout_mode, 2, 0, 1, 1)

        self.label_9 = QLabel(self.frame_3)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_4.addWidget(self.label_9, 3, 0, 1, 1)

        self.label_3 = QLabel(self.frame_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.gridLayout_4.addWidget(self.label_3, 0, 0, 1, 1)

        self.horizontal_binning = QSpinBox(self.frame_3)
        self.horizontal_binning.setObjectName(u"horizontal_binning")
        self.horizontal_binning.setSingleStep(2)
        self.horizontal_binning.setValue(4)

        self.gridLayout_4.addWidget(self.horizontal_binning, 6, 0, 1, 1)

        self.hs_speed = QDoubleSpinBox(self.frame_3)
        self.hs_speed.setObjectName(u"hs_speed")
        self.hs_speed.setValue(0.050000000000000)

        self.gridLayout_4.addWidget(self.hs_speed, 8, 0, 1, 1)

        self.label_11 = QLabel(self.frame_3)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_4.addWidget(self.label_11, 7, 0, 1, 1)

        self.vs_speed = QDoubleSpinBox(self.frame_3)
        self.vs_speed.setObjectName(u"vs_speed")
        self.vs_speed.setValue(25.699999999999999)

        self.gridLayout_4.addWidget(self.vs_speed, 10, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_2, 11, 0, 1, 1)

        self.label_12 = QLabel(self.frame_3)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_4.addWidget(self.label_12, 9, 0, 1, 1)

        self.label_10 = QLabel(self.frame_3)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_4.addWidget(self.label_10, 5, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_3, 0, 1, 3, 1)

        self.tracks_frame = QFrame(andor_newton_config)
        self.tracks_frame.setObjectName(u"tracks_frame")
        self.tracks_frame.setFrameShape(QFrame.StyledPanel)
        self.tracks_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.tracks_frame)
        self.gridLayout_3.setObjectName(u"gridLayout_3")

        self.gridLayout.addWidget(self.tracks_frame, 0, 2, 3, 1)

        QWidget.setTabOrder(self.set_temperature, self.exposure_time)
        QWidget.setTabOrder(self.exposure_time, self.preamp_gain)
        QWidget.setTabOrder(self.preamp_gain, self.horizontal_binning)
        QWidget.setTabOrder(self.horizontal_binning, self.hs_speed)
        QWidget.setTabOrder(self.hs_speed, self.vs_speed)
        QWidget.setTabOrder(self.vs_speed, self.comboBox_shutter_mode)
        QWidget.setTabOrder(self.comboBox_shutter_mode, self.comboBox_readout_mode)

        self.retranslateUi(andor_newton_config)

        QMetaObject.connectSlotsByName(andor_newton_config)
    # setupUi

    def retranslateUi(self, andor_newton_config):
        andor_newton_config.setWindowTitle(QCoreApplication.translate("andor_newton_config", u"Form", None))
        self.label_15.setText(QCoreApplication.translate("andor_newton_config", u"Temperature (\u00b0C)", None))
        self.label.setText(QCoreApplication.translate("andor_newton_config", u"Exposure", None))
        self.comboBox_shutter_mode.setItemText(0, QCoreApplication.translate("andor_newton_config", u"open", None))
        self.comboBox_shutter_mode.setItemText(1, QCoreApplication.translate("andor_newton_config", u"closed", None))
        self.comboBox_shutter_mode.setItemText(2, QCoreApplication.translate("andor_newton_config", u"auto", None))

        self.label_5.setText(QCoreApplication.translate("andor_newton_config", u"Exposure Time (s)", None))
        self.label_4.setText(QCoreApplication.translate("andor_newton_config", u"Shutter Mode", None))
        self.label_8.setText(QCoreApplication.translate("andor_newton_config", u"Readout Mode", None))
        self.comboBox_readout_mode.setItemText(0, QCoreApplication.translate("andor_newton_config", u"FVB - full vertical binning", None))
        self.comboBox_readout_mode.setItemText(1, QCoreApplication.translate("andor_newton_config", u"multi track", None))
        self.comboBox_readout_mode.setItemText(2, QCoreApplication.translate("andor_newton_config", u"image", None))
        self.comboBox_readout_mode.setItemText(3, QCoreApplication.translate("andor_newton_config", u"random track", None))

        self.label_9.setText(QCoreApplication.translate("andor_newton_config", u"Preamp Gain", None))
        self.label_3.setText(QCoreApplication.translate("andor_newton_config", u"Readout", None))
        self.label_11.setText(QCoreApplication.translate("andor_newton_config", u"HS Speed (MHz)", None))
        self.label_12.setText(QCoreApplication.translate("andor_newton_config", u"VS Speed (\u00b5s/shift)", None))
        self.label_10.setText(QCoreApplication.translate("andor_newton_config", u"Horizontal Binning", None))
    # retranslateUi

