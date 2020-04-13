# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ResultWidget.ui'
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


class Ui_ResultWidget(object):
    def setupUi(self, ResultWidget):
        if ResultWidget.objectName():
            ResultWidget.setObjectName(u"ResultWidget")
        ResultWidget.resize(800, 570)
        font = QFont()
        font.setFamily(u"Arial")
        font.setPointSize(15)
        ResultWidget.setFont(font)
        self.homeButton = QPushButton(ResultWidget)
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
        self.nextButton = QPushButton(ResultWidget)
        self.nextButton.setObjectName(u"nextButton")
        self.nextButton.setGeometry(QRect(630, 490, 161, 61))
        sizePolicy.setHeightForWidth(self.nextButton.sizePolicy().hasHeightForWidth())
        self.nextButton.setSizePolicy(sizePolicy)
        self.nextButton.setFont(font1)
        self.title = QLabel(ResultWidget)
        self.title.setObjectName(u"title")
        self.title.setGeometry(QRect(80, -10, 621, 71))
        self.title.setAlignment(Qt.AlignCenter)
        self.your_arr = QLabel(ResultWidget)
        self.your_arr.setObjectName(u"your_arr")
        self.your_arr.setGeometry(QRect(40, 200, 731, 61))
        self.your_arr.setAlignment(Qt.AlignCenter)
        self.best_arr = QLabel(ResultWidget)
        self.best_arr.setObjectName(u"best_arr")
        self.best_arr.setGeometry(QRect(30, 420, 741, 61))
        self.best_arr.setAlignment(Qt.AlignCenter)

        self.retranslateUi(ResultWidget)

        QMetaObject.connectSlotsByName(ResultWidget)
    # setupUi

    def retranslateUi(self, ResultWidget):
        ResultWidget.setWindowTitle(QCoreApplication.translate("ResultWidget", u"Form", None))
        self.homeButton.setText(QCoreApplication.translate("ResultWidget", u"GO HOME", None))
        self.nextButton.setText(QCoreApplication.translate("ResultWidget", u"NEXT BATTLE", None))
        self.title.setText(QCoreApplication.translate("ResultWidget", u"TextLabel", None))
        self.your_arr.setText(QCoreApplication.translate("ResultWidget", u"TextLabel", None))
        self.best_arr.setText(QCoreApplication.translate("ResultWidget", u"TextLabel", None))
    # retranslateUi

