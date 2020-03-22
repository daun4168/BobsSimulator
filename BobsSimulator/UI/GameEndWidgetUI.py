# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GameEndWidget.ui'
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


class Ui_GameEndWidget(object):
    def setupUi(self, GameEndWidget):
        if GameEndWidget.objectName():
            GameEndWidget.setObjectName(u"GameEndWidget")
        GameEndWidget.resize(800, 570)
        font = QFont()
        font.setPointSize(15)
        GameEndWidget.setFont(font)
        self.homeButton = QPushButton(GameEndWidget)
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
        self.nextButton = QPushButton(GameEndWidget)
        self.nextButton.setObjectName(u"nextButton")
        self.nextButton.setGeometry(QRect(630, 490, 161, 61))
        sizePolicy.setHeightForWidth(self.nextButton.sizePolicy().hasHeightForWidth())
        self.nextButton.setSizePolicy(sizePolicy)
        self.nextButton.setFont(font1)
        self.heroImg = QLabel(GameEndWidget)
        self.heroImg.setObjectName(u"heroImg")
        self.heroImg.setGeometry(QRect(300, 0, 221, 211))
        self.rankText = QLabel(GameEndWidget)
        self.rankText.setObjectName(u"rankText")
        self.rankText.setGeometry(QRect(110, 220, 571, 91))
        self.rankText.setAlignment(Qt.AlignCenter)
        self.rankNumber = QLabel(GameEndWidget)
        self.rankNumber.setObjectName(u"rankNumber")
        self.rankNumber.setGeometry(QRect(270, 290, 271, 241))
        self.rankNumber.setAlignment(Qt.AlignCenter)

        self.retranslateUi(GameEndWidget)

        QMetaObject.connectSlotsByName(GameEndWidget)
    # setupUi

    def retranslateUi(self, GameEndWidget):
        GameEndWidget.setWindowTitle(QCoreApplication.translate("GameEndWidget", u"Form", None))
        self.homeButton.setText(QCoreApplication.translate("GameEndWidget", u"GO HOME", None))
        self.nextButton.setText(QCoreApplication.translate("GameEndWidget", u"NEXT GAME", None))
        self.heroImg.setText("")
        self.rankText.setText(QCoreApplication.translate("GameEndWidget", u"YOUR FINAL RANK", None))
        self.rankNumber.setText("")
    # retranslateUi

