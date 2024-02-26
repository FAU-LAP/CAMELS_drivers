# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'andor_shamrock_500_config.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFrame,
    QGridLayout,
    QLabel,
    QLineEdit,
    QSizePolicy,
    QSpacerItem,
    QSpinBox,
    QWidget,
)


class Ui_andor_shamrock500_config(object):
    def setupUi(self, andor_shamrock500_config):
        if not andor_shamrock500_config.objectName():
            andor_shamrock500_config.setObjectName("andor_shamrock500_config")
        andor_shamrock500_config.resize(318, 310)
        self.gridLayout = QGridLayout(andor_shamrock500_config)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_2 = QFrame(andor_shamrock500_config)
        self.frame_2.setObjectName("frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.lineEdit_wl_start = QLineEdit(self.frame_2)
        self.lineEdit_wl_start.setObjectName("lineEdit_wl_start")
        self.lineEdit_wl_start.setEnabled(False)

        self.gridLayout_3.addWidget(self.lineEdit_wl_start, 7, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.gridLayout_3.addItem(self.verticalSpacer, 8, 0, 1, 1)

        self.label_11 = QLabel(self.frame_2)
        self.label_11.setObjectName("label_11")

        self.gridLayout_3.addWidget(self.label_11, 7, 1, 1, 1)

        self.lineEdit_wl_end = QLineEdit(self.frame_2)
        self.lineEdit_wl_end.setObjectName("lineEdit_wl_end")
        self.lineEdit_wl_end.setEnabled(False)

        self.gridLayout_3.addWidget(self.lineEdit_wl_end, 7, 2, 1, 1)

        self.initial_wavelength = QSpinBox(self.frame_2)
        self.initial_wavelength.setObjectName("initial_wavelength")
        self.initial_wavelength.setMaximum(9999)
        self.initial_wavelength.setValue(800)

        self.gridLayout_3.addWidget(self.initial_wavelength, 6, 0, 1, 3)

        self.label_3 = QLabel(self.frame_2)
        self.label_3.setObjectName("label_3")

        self.gridLayout_3.addWidget(self.label_3, 5, 0, 1, 3)

        self.set_grating_number = QSpinBox(self.frame_2)
        self.set_grating_number.setObjectName("set_grating_number")
        self.set_grating_number.setValue(1)

        self.gridLayout_3.addWidget(self.set_grating_number, 4, 0, 1, 3)

        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName("label_2")

        self.gridLayout_3.addWidget(self.label_2, 3, 0, 1, 3)

        self.label = QLabel(self.frame_2)
        self.label.setObjectName("label")
        font = QFont()
        font.setPointSize(9)
        font.setBold(True)
        self.label.setFont(font)

        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 3)

        self.gridLayout.addWidget(self.frame_2, 0, 0, 1, 1)

        self.frame_4 = QFrame(andor_shamrock500_config)
        self.frame_4.setObjectName("frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_4)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_5 = QLabel(self.frame_4)
        self.label_5.setObjectName("label_5")
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(True)
        self.label_5.setFont(font1)

        self.gridLayout_5.addWidget(self.label_5, 0, 0, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.gridLayout_5.addItem(self.verticalSpacer_4, 3, 0, 1, 1)

        self.comboBox_camera = QComboBox(self.frame_4)
        self.comboBox_camera.setObjectName("comboBox_camera")

        self.gridLayout_5.addWidget(self.comboBox_camera, 1, 0, 1, 1)

        self.checkBox_horizontal_flip = QCheckBox(self.frame_4)
        self.checkBox_horizontal_flip.setObjectName("checkBox_horizontal_flip")

        self.gridLayout_5.addWidget(self.checkBox_horizontal_flip, 2, 0, 1, 1)

        self.gridLayout.addWidget(self.frame_4, 0, 1, 1, 1)

        self.frame = QFrame(andor_shamrock500_config)
        self.frame.setObjectName("frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName("label_4")

        self.gridLayout_2.addWidget(self.label_4, 3, 0, 1, 1)

        self.label_7 = QLabel(self.frame)
        self.label_7.setObjectName("label_7")

        self.gridLayout_2.addWidget(self.label_7, 1, 0, 1, 1)

        self.input_port = QComboBox(self.frame)
        self.input_port.addItem("")
        self.input_port.addItem("")
        self.input_port.setObjectName("input_port")

        self.gridLayout_2.addWidget(self.input_port, 2, 0, 1, 1)

        self.label_6 = QLabel(self.frame)
        self.label_6.setObjectName("label_6")
        self.label_6.setFont(font)

        self.gridLayout_2.addWidget(self.label_6, 0, 0, 1, 1)

        self.input_slit_size = QSpinBox(self.frame)
        self.input_slit_size.setObjectName("input_slit_size")
        self.input_slit_size.setMaximum(2500)
        self.input_slit_size.setValue(10)

        self.gridLayout_2.addWidget(self.input_slit_size, 4, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.gridLayout_2.addItem(self.verticalSpacer_2, 7, 0, 1, 1)

        self.gridLayout.addWidget(self.frame, 1, 1, 1, 1)

        self.frame_3 = QFrame(andor_shamrock500_config)
        self.frame_3.setObjectName("frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_3)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.output_port = QComboBox(self.frame_3)
        self.output_port.addItem("")
        self.output_port.addItem("")
        self.output_port.setObjectName("output_port")

        self.gridLayout_4.addWidget(self.output_port, 2, 0, 1, 1)

        self.label_8 = QLabel(self.frame_3)
        self.label_8.setObjectName("label_8")
        self.label_8.setFont(font)

        self.gridLayout_4.addWidget(self.label_8, 0, 0, 1, 1)

        self.label_9 = QLabel(self.frame_3)
        self.label_9.setObjectName("label_9")

        self.gridLayout_4.addWidget(self.label_9, 1, 0, 1, 1)

        self.output_slit_size = QSpinBox(self.frame_3)
        self.output_slit_size.setObjectName("output_slit_size")
        self.output_slit_size.setMaximum(9999)

        self.gridLayout_4.addWidget(self.output_slit_size, 4, 0, 1, 1)

        self.label_10 = QLabel(self.frame_3)
        self.label_10.setObjectName("label_10")

        self.gridLayout_4.addWidget(self.label_10, 3, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.gridLayout_4.addItem(self.verticalSpacer_3, 5, 0, 1, 1)

        self.gridLayout.addWidget(self.frame_3, 1, 0, 1, 1)

        QWidget.setTabOrder(self.set_grating_number, self.initial_wavelength)
        QWidget.setTabOrder(self.initial_wavelength, self.input_slit_size)
        QWidget.setTabOrder(self.input_slit_size, self.output_slit_size)
        QWidget.setTabOrder(self.output_slit_size, self.input_port)
        QWidget.setTabOrder(self.input_port, self.output_port)

        self.retranslateUi(andor_shamrock500_config)

        QMetaObject.connectSlotsByName(andor_shamrock500_config)

    # setupUi

    def retranslateUi(self, andor_shamrock500_config):
        andor_shamrock500_config.setWindowTitle(
            QCoreApplication.translate("andor_shamrock500_config", "Form", None)
        )
        self.label_11.setText(
            QCoreApplication.translate("andor_shamrock500_config", "...", None)
        )
        self.label_3.setText(
            QCoreApplication.translate(
                "andor_shamrock500_config", "center wavelength (nm)", None
            )
        )
        self.label_2.setText(
            QCoreApplication.translate(
                "andor_shamrock500_config", "grating number", None
            )
        )
        self.label.setText(
            QCoreApplication.translate(
                "andor_shamrock500_config", "Grating Settings", None
            )
        )
        self.label_5.setText(
            QCoreApplication.translate("andor_shamrock500_config", "Camera", None)
        )
        self.checkBox_horizontal_flip.setText(
            QCoreApplication.translate(
                "andor_shamrock500_config", "horizontal flip", None
            )
        )
        self.label_4.setText(
            QCoreApplication.translate(
                "andor_shamrock500_config", "Input Slit Size (\u00b5m)", None
            )
        )
        self.label_7.setText(
            QCoreApplication.translate("andor_shamrock500_config", "Input Port", None)
        )
        self.input_port.setItemText(
            0, QCoreApplication.translate("andor_shamrock500_config", "side", None)
        )
        self.input_port.setItemText(
            1, QCoreApplication.translate("andor_shamrock500_config", "direct", None)
        )

        self.label_6.setText(
            QCoreApplication.translate(
                "andor_shamrock500_config", "Input Port Settings", None
            )
        )
        self.output_port.setItemText(
            0, QCoreApplication.translate("andor_shamrock500_config", "direct", None)
        )
        self.output_port.setItemText(
            1, QCoreApplication.translate("andor_shamrock500_config", "side", None)
        )

        self.label_8.setText(
            QCoreApplication.translate(
                "andor_shamrock500_config", "Output Port Settings", None
            )
        )
        self.label_9.setText(
            QCoreApplication.translate("andor_shamrock500_config", "Output Port", None)
        )
        self.label_10.setText(
            QCoreApplication.translate(
                "andor_shamrock500_config", "Output Slite Size", None
            )
        )

    # retranslateUi
