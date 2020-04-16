# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'OptimizeResultWidget.ui'
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


class Ui_OptimizeResultWidget(object):
    def setupUi(self, OptimizeResultWidget):
        if OptimizeResultWidget.objectName():
            OptimizeResultWidget.setObjectName(u"OptimizeResultWidget")
        OptimizeResultWidget.resize(800, 570)
        font = QFont()
        font.setFamily(u"Arial")
        font.setPointSize(15)
        OptimizeResultWidget.setFont(font)
        self.homeButton = QPushButton(OptimizeResultWidget)
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
        self.nextButton = QPushButton(OptimizeResultWidget)
        self.nextButton.setObjectName(u"nextButton")
        self.nextButton.setGeometry(QRect(630, 490, 161, 61))
        sizePolicy.setHeightForWidth(self.nextButton.sizePolicy().hasHeightForWidth())
        self.nextButton.setSizePolicy(sizePolicy)
        self.nextButton.setFont(font1)
        self.title = QLabel(OptimizeResultWidget)
        self.title.setObjectName(u"title")
        self.title.setGeometry(QRect(80, -10, 621, 71))
        self.title.setAlignment(Qt.AlignCenter)
        self.your_arr = QLabel(OptimizeResultWidget)
        self.your_arr.setObjectName(u"your_arr")
        self.your_arr.setGeometry(QRect(0, 200, 791, 61))
        self.your_arr.setAlignment(Qt.AlignCenter)
        self.best_arr = QLabel(OptimizeResultWidget)
        self.best_arr.setObjectName(u"best_arr")
        self.best_arr.setGeometry(QRect(0, 420, 791, 61))
        self.best_arr.setAlignment(Qt.AlignCenter)
        self.actualResult = QPushButton(OptimizeResultWidget)
        self.actualResult.setObjectName(u"actualResult")
        self.actualResult.setGeometry(QRect(210, 490, 381, 61))
        sizePolicy.setHeightForWidth(self.actualResult.sizePolicy().hasHeightForWidth())
        self.actualResult.setSizePolicy(sizePolicy)
        self.actualResult.setFont(font1)

        self.retranslateUi(OptimizeResultWidget)

        QMetaObject.connectSlotsByName(OptimizeResultWidget)
    # setupUi

    def retranslateUi(self, OptimizeResultWidget):
        OptimizeResultWidget.setWindowTitle(QCoreApplication.translate("OptimizeResultWidget", u"Form", None))
        self.homeButton.setText(QCoreApplication.translate("OptimizeResultWidget", u"GO HOME", None))
        self.nextButton.setText(QCoreApplication.translate("OptimizeResultWidget", u"NEXT BATTLE", None))
        self.title.setText(QCoreApplication.translate("OptimizeResultWidget", u"TextLabel", None))
        self.your_arr.setText(QCoreApplication.translate("OptimizeResultWidget", u"TextLabel", None))
        self.best_arr.setText(QCoreApplication.translate("OptimizeResultWidget", u"TextLabel", None))
        self.actualResult.setText(QCoreApplication.translate("OptimizeResultWidget", u"Show Actual Result", None))
    # retranslateUi

