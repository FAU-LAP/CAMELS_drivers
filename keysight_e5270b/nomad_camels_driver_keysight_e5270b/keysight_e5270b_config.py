# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'keysight_e5270b_config.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QLabel, QLineEdit, QSizePolicy, QTabWidget,
    QWidget)

class Ui_keysight_e5270b_config(object):
    def setupUi(self, keysight_e5270b_config):
        if not keysight_e5270b_config.objectName():
            keysight_e5270b_config.setObjectName(u"keysight_e5270b_config")
        keysight_e5270b_config.resize(782, 431)
        self.gridLayout = QGridLayout(keysight_e5270b_config)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_10 = QLabel(keysight_e5270b_config)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMaximumSize(QSize(16777215, 30))
        font = QFont()
        font.setPointSize(9)
        font.setBold(True)
        self.label_10.setFont(font)

        self.gridLayout.addWidget(self.label_10, 1, 2, 1, 2)

        self.comboBox_highSpeedMode = QComboBox(keysight_e5270b_config)
        self.comboBox_highSpeedMode.setObjectName(u"comboBox_highSpeedMode")

        self.gridLayout.addWidget(self.comboBox_highSpeedMode, 2, 1, 1, 1)

        self.lineEdit_highSpeedPLC = QLineEdit(keysight_e5270b_config)
        self.lineEdit_highSpeedPLC.setObjectName(u"lineEdit_highSpeedPLC")

        self.gridLayout.addWidget(self.lineEdit_highSpeedPLC, 3, 1, 1, 1)

        self.label_speedMode = QLabel(keysight_e5270b_config)
        self.label_speedMode.setObjectName(u"label_speedMode")

        self.gridLayout.addWidget(self.label_speedMode, 2, 0, 1, 1)

        self.lineEdit_highResPLC = QLineEdit(keysight_e5270b_config)
        self.lineEdit_highResPLC.setObjectName(u"lineEdit_highResPLC")

        self.gridLayout.addWidget(self.lineEdit_highResPLC, 3, 3, 1, 1)

        self.label_speedPLC = QLabel(keysight_e5270b_config)
        self.label_speedPLC.setObjectName(u"label_speedPLC")
        self.label_speedPLC.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_speedPLC, 3, 0, 1, 1)

        self.label_resMode = QLabel(keysight_e5270b_config)
        self.label_resMode.setObjectName(u"label_resMode")

        self.gridLayout.addWidget(self.label_resMode, 2, 2, 1, 1)

        self.label_resPLC = QLabel(keysight_e5270b_config)
        self.label_resPLC.setObjectName(u"label_resPLC")
        self.label_resPLC.setLayoutDirection(Qt.LeftToRight)
        self.label_resPLC.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_resPLC, 3, 2, 1, 1)

        self.comboBox_highResMode = QComboBox(keysight_e5270b_config)
        self.comboBox_highResMode.setObjectName(u"comboBox_highResMode")

        self.gridLayout.addWidget(self.comboBox_highResMode, 2, 3, 1, 1)

        self.label_9 = QLabel(keysight_e5270b_config)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMaximumSize(QSize(16777215, 30))
        self.label_9.setFont(font)

        self.gridLayout.addWidget(self.label_9, 1, 0, 1, 2)

        self.line_2 = QFrame(keysight_e5270b_config)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_2, 4, 0, 1, 4)

        self.tabWidget = QTabWidget(keysight_e5270b_config)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setMaximumSize(QSize(16777215, 250))
        self.channel1 = QWidget()
        self.channel1.setObjectName(u"channel1")
        self.gridLayout_2 = QGridLayout(self.channel1)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.tabWidget.addTab(self.channel1, "")
        self.channel2 = QWidget()
        self.channel2.setObjectName(u"channel2")
        self.gridLayout_3 = QGridLayout(self.channel2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.tabWidget.addTab(self.channel2, "")
        self.channel3 = QWidget()
        self.channel3.setObjectName(u"channel3")
        self.gridLayout_4 = QGridLayout(self.channel3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.tabWidget.addTab(self.channel3, "")
        self.channel4 = QWidget()
        self.channel4.setObjectName(u"channel4")
        self.gridLayout_5 = QGridLayout(self.channel4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.tabWidget.addTab(self.channel4, "")
        self.channel5 = QWidget()
        self.channel5.setObjectName(u"channel5")
        self.gridLayout_6 = QGridLayout(self.channel5)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.tabWidget.addTab(self.channel5, "")
        self.channel6 = QWidget()
        self.channel6.setObjectName(u"channel6")
        self.gridLayout_7 = QGridLayout(self.channel6)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.tabWidget.addTab(self.channel6, "")
        self.channel7 = QWidget()
        self.channel7.setObjectName(u"channel7")
        self.gridLayout_8 = QGridLayout(self.channel7)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.tabWidget.addTab(self.channel7, "")
        self.channel8 = QWidget()
        self.channel8.setObjectName(u"channel8")
        self.gridLayout_9 = QGridLayout(self.channel8)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.tabWidget.addTab(self.channel8, "")

        self.gridLayout.addWidget(self.tabWidget, 5, 0, 1, 4)

        QWidget.setTabOrder(self.comboBox_highSpeedMode, self.lineEdit_highSpeedPLC)
        QWidget.setTabOrder(self.lineEdit_highSpeedPLC, self.comboBox_highResMode)
        QWidget.setTabOrder(self.comboBox_highResMode, self.lineEdit_highResPLC)

        self.retranslateUi(keysight_e5270b_config)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(keysight_e5270b_config)
    # setupUi

    def retranslateUi(self, keysight_e5270b_config):
        keysight_e5270b_config.setWindowTitle(QCoreApplication.translate("keysight_e5270b_config", u"Form", None))
        self.label_10.setText(QCoreApplication.translate("keysight_e5270b_config", u"High Resolution ADC", None))
        self.label_speedMode.setText(QCoreApplication.translate("keysight_e5270b_config", u"Mode", None))
        self.label_speedPLC.setText(QCoreApplication.translate("keysight_e5270b_config", u"N", None))
        self.label_resMode.setText(QCoreApplication.translate("keysight_e5270b_config", u"Mode", None))
        self.label_resPLC.setText(QCoreApplication.translate("keysight_e5270b_config", u"N", None))
        self.label_9.setText(QCoreApplication.translate("keysight_e5270b_config", u"High Speed ADC", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.channel1), QCoreApplication.translate("keysight_e5270b_config", u"Channel 1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.channel2), QCoreApplication.translate("keysight_e5270b_config", u"Channel 2", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.channel3), QCoreApplication.translate("keysight_e5270b_config", u"Channel 3", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.channel4), QCoreApplication.translate("keysight_e5270b_config", u"Channel 4", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.channel5), QCoreApplication.translate("keysight_e5270b_config", u"Channel 5", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.channel6), QCoreApplication.translate("keysight_e5270b_config", u"Channel 6", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.channel7), QCoreApplication.translate("keysight_e5270b_config", u"Channel 7", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.channel8), QCoreApplication.translate("keysight_e5270b_config", u"Channel 8", None))
    # retranslateUi

