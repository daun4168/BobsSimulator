# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SimulationResultWidget.ui'
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


class Ui_SimulationResultWidget(object):
    def setupUi(self, SimulationResultWidget):
        if SimulationResultWidget.objectName():
            SimulationResultWidget.setObjectName(u"SimulationResultWidget")
        SimulationResultWidget.resize(800, 570)
        font = QFont()
        font.setFamily(u"Arial")
        font.setPointSize(15)
        SimulationResultWidget.setFont(font)
        self.homeButton = QPushButton(SimulationResultWidget)
        self.homeButton.setObjectName(u"homeButton")
        self.homeButton.setGeometry(QRect(20, 490, 151, 61))
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.homeButton.sizePolicy().hasHeightForWidth())
        self.homeButton.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setFamily(u"Yu Gothic")
        font1.setPointSize(15)
        font1.setBold(True)
        font1.setWeight(75)
        self.homeButton.setFont(font1)
        self.nextButton = QPushButton(SimulationResultWidget)
        self.nextButton.setObjectName(u"nextButton")
        self.nextButton.setGeometry(QRect(630, 490, 161, 61))
        sizePolicy.setHeightForWidth(self.nextButton.sizePolicy().hasHeightForWidth())
        self.nextButton.setSizePolicy(sizePolicy)
        self.nextButton.setFont(font1)
        self.title = QLabel(SimulationResultWidget)
        self.title.setObjectName(u"title")
        self.title.setGeometry(QRect(80, -10, 621, 71))
        self.title.setAlignment(Qt.AlignCenter)
        self.your_arr = QLabel(SimulationResultWidget)
        self.your_arr.setObjectName(u"your_arr")
        self.your_arr.setGeometry(QRect(0, 420, 791, 61))
        self.your_arr.setAlignment(Qt.AlignCenter)
        self.actualResult = QPushButton(SimulationResultWidget)
        self.actualResult.setObjectName(u"actualResult")
        self.actualResult.setGeometry(QRect(210, 490, 381, 61))
        sizePolicy.setHeightForWidth(self.actualResult.sizePolicy().hasHeightForWidth())
        self.actualResult.setSizePolicy(sizePolicy)
        self.actualResult.setFont(font1)

        self.retranslateUi(SimulationResultWidget)

        QMetaObject.connectSlotsByName(SimulationResultWidget)
    # setupUi

    def retranslateUi(self, SimulationResultWidget):
        SimulationResultWidget.setWindowTitle(QCoreApplication.translate("SimulationResultWidget", u"Form", None))
        self.homeButton.setText(QCoreApplication.translate("SimulationResultWidget", u"GO HOME", None))
        self.nextButton.setText(QCoreApplication.translate("SimulationResultWidget", u"NEXT BATTLE", None))
        self.title.setText(QCoreApplication.translate("SimulationResultWidget", u"TextLabel", None))
        self.your_arr.setText(QCoreApplication.translate("SimulationResultWidget", u"TextLabel", None))
        self.actualResult.setText(QCoreApplication.translate("SimulationResultWidget", u"Show Actual Result", None))
    # retranslateUi

