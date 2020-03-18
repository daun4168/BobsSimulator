# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ErrorWidget.ui'
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


class Ui_ErrorWidget(object):
    def setupUi(self, ErrorWidget):
        if ErrorWidget.objectName():
            ErrorWidget.setObjectName(u"ErrorWidget")
        ErrorWidget.resize(800, 570)
        self.logoLabel = QLabel(ErrorWidget)
        self.logoLabel.setObjectName(u"logoLabel")
        self.logoLabel.setGeometry(QRect(10, 30, 781, 181))
        self.errorImg = QLabel(ErrorWidget)
        self.errorImg.setObjectName(u"errorImg")
        self.errorImg.setGeometry(QRect(500, 180, 300, 282))
        self.errorText = QLabel(ErrorWidget)
        self.errorText.setObjectName(u"errorText")
        self.errorText.setGeometry(QRect(30, 300, 451, 181))
        self.errorText.setAlignment(Qt.AlignCenter)
        self.homeButton = QPushButton(ErrorWidget)
        self.homeButton.setObjectName(u"homeButton")
        self.homeButton.setGeometry(QRect(290, 490, 241, 61))
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.homeButton.sizePolicy().hasHeightForWidth())
        self.homeButton.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamily(u"Yu Gothic")
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.homeButton.setFont(font)
        self.oopsText = QLabel(ErrorWidget)
        self.oopsText.setObjectName(u"oopsText")
        self.oopsText.setGeometry(QRect(110, 170, 291, 161))
        self.oopsText.setAlignment(Qt.AlignCenter)

        self.retranslateUi(ErrorWidget)

        QMetaObject.connectSlotsByName(ErrorWidget)
    # setupUi

    def retranslateUi(self, ErrorWidget):
        ErrorWidget.setWindowTitle(QCoreApplication.translate("ErrorWidget", u"Form", None))
        self.logoLabel.setText("")
        self.errorImg.setText("")
        self.errorText.setText("")
        self.homeButton.setText(QCoreApplication.translate("ErrorWidget", u"GO HOME", None))
        self.oopsText.setText("")
    # retranslateUi

