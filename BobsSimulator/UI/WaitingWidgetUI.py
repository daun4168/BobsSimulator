# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'WaitingWidget.ui'
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


class Ui_LoadingWidget(object):
    def setupUi(self, LoadingWidget):
        if LoadingWidget.objectName():
            LoadingWidget.setObjectName(u"LoadingWidget")
        LoadingWidget.resize(800, 570)
        self.logoLabel = QLabel(LoadingWidget)
        self.logoLabel.setObjectName(u"logoLabel")
        self.logoLabel.setGeometry(QRect(10, 30, 781, 181))
        self.waitingImgLeft = QLabel(LoadingWidget)
        self.waitingImgLeft.setObjectName(u"waitingImgLeft")
        self.waitingImgLeft.setGeometry(QRect(-1, 220, 238, 341))
        self.waitingImgRight = QLabel(LoadingWidget)
        self.waitingImgRight.setObjectName(u"waitingImgRight")
        self.waitingImgRight.setGeometry(QRect(670, 220, 100, 309))
        self.waitingTextTop = QLabel(LoadingWidget)
        self.waitingTextTop.setObjectName(u"waitingTextTop")
        self.waitingTextTop.setGeometry(QRect(130, 190, 541, 191))
        self.waitingTextTop.setAlignment(Qt.AlignCenter)
        self.waitingTextBottom = QLabel(LoadingWidget)
        self.waitingTextBottom.setObjectName(u"waitingTextBottom")
        self.waitingTextBottom.setGeometry(QRect(180, 370, 461, 121))

        self.retranslateUi(LoadingWidget)

        QMetaObject.connectSlotsByName(LoadingWidget)
    # setupUi

    def retranslateUi(self, LoadingWidget):
        LoadingWidget.setWindowTitle(QCoreApplication.translate("LoadingWidget", u"Form", None))
        self.logoLabel.setText("")
        self.waitingImgLeft.setText("")
        self.waitingImgRight.setText("")
        self.waitingTextTop.setText("")
        self.waitingTextBottom.setText("")
    # retranslateUi

