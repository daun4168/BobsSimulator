# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'HomeWidget.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *


class Ui_HomeWidget(object):
    def setupUi(self, HomeWidget):
        if HomeWidget.objectName():
            HomeWidget.setObjectName(u"HomeWidget")
        HomeWidget.resize(800, 570)
        self.logoLabel = QLabel(HomeWidget)
        self.logoLabel.setObjectName(u"logoLabel")
        self.logoLabel.setGeometry(QRect(10, 30, 781, 181))
        self.widget = QWidget(HomeWidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(230, 230, 381, 311))
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.realtimeButton = QPushButton(self.widget)
        self.realtimeButton.setObjectName(u"realtimeButton")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.realtimeButton.sizePolicy().hasHeightForWidth())
        self.realtimeButton.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamily(u"Yu Gothic")
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.realtimeButton.setFont(font)

        self.gridLayout.addWidget(self.realtimeButton, 0, 0, 1, 1)

        self.logfileButton = QPushButton(self.widget)
        self.logfileButton.setObjectName(u"logfileButton")
        sizePolicy.setHeightForWidth(self.logfileButton.sizePolicy().hasHeightForWidth())
        self.logfileButton.setSizePolicy(sizePolicy)
        self.logfileButton.setFont(font)

        self.gridLayout.addWidget(self.logfileButton, 1, 0, 1, 1)

        self.textButton = QPushButton(self.widget)
        self.textButton.setObjectName(u"textButton")
        sizePolicy.setHeightForWidth(self.textButton.sizePolicy().hasHeightForWidth())
        self.textButton.setSizePolicy(sizePolicy)
        self.textButton.setFont(font)

        self.gridLayout.addWidget(self.textButton, 2, 0, 1, 1)


        self.retranslateUi(HomeWidget)

        QMetaObject.connectSlotsByName(HomeWidget)
    # setupUi

    def retranslateUi(self, HomeWidget):
        HomeWidget.setWindowTitle(QCoreApplication.translate("HomeWidget", u"Form", None))
        self.logoLabel.setText("")
        self.realtimeButton.setText(QCoreApplication.translate("HomeWidget", u"&Real Time", None))
        self.logfileButton.setText(QCoreApplication.translate("HomeWidget", u"&Log File", None))
        self.textButton.setText(QCoreApplication.translate("HomeWidget", u"&Text", None))
    # retranslateUi

