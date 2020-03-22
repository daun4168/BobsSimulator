# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FileEndWidget.ui'
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


class Ui_fileEndWidget(object):
    def setupUi(self, fileEndWidget):
        if fileEndWidget.objectName():
            fileEndWidget.setObjectName(u"fileEndWidget")
        fileEndWidget.resize(800, 570)
        self.logoLabel = QLabel(fileEndWidget)
        self.logoLabel.setObjectName(u"logoLabel")
        self.logoLabel.setGeometry(QRect(10, 30, 781, 181))
        self.endImg = QLabel(fileEndWidget)
        self.endImg.setObjectName(u"endImg")
        self.endImg.setGeometry(QRect(400, 170, 391, 301))
        self.endText2 = QLabel(fileEndWidget)
        self.endText2.setObjectName(u"endText2")
        self.endText2.setGeometry(QRect(30, 300, 451, 181))
        self.endText2.setAlignment(Qt.AlignCenter)
        self.homeButton = QPushButton(fileEndWidget)
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
        self.endText1 = QLabel(fileEndWidget)
        self.endText1.setObjectName(u"endText1")
        self.endText1.setGeometry(QRect(110, 170, 291, 161))
        self.endText1.setAlignment(Qt.AlignCenter)

        self.retranslateUi(fileEndWidget)

        QMetaObject.connectSlotsByName(fileEndWidget)
    # setupUi

    def retranslateUi(self, fileEndWidget):
        fileEndWidget.setWindowTitle(QCoreApplication.translate("fileEndWidget", u"Form", None))
        self.logoLabel.setText("")
        self.endImg.setText("")
        self.endText2.setText("")
        self.homeButton.setText(QCoreApplication.translate("fileEndWidget", u"GO HOME", None))
        self.endText1.setText("")
    # retranslateUi

