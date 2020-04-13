# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'BattleInfoWidget.ui'
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


class Ui_BattleInfoWidget(object):
    def setupUi(self, BattleInfoWidget):
        if BattleInfoWidget.objectName():
            BattleInfoWidget.setObjectName(u"BattleInfoWidget")
        BattleInfoWidget.resize(800, 570)
        font = QFont()
        font.setPointSize(15)
        BattleInfoWidget.setFont(font)
        self.homeButton = QPushButton(BattleInfoWidget)
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
        self.simulateButton = QPushButton(BattleInfoWidget)
        self.simulateButton.setObjectName(u"simulateButton")
        self.simulateButton.setGeometry(QRect(260, 490, 311, 61))
        sizePolicy.setHeightForWidth(self.simulateButton.sizePolicy().hasHeightForWidth())
        self.simulateButton.setSizePolicy(sizePolicy)
        font2 = QFont()
        font2.setFamily(u"Arial")
        font2.setPointSize(25)
        font2.setBold(True)
        font2.setWeight(75)
        self.simulateButton.setFont(font2)
        self.nextButton = QPushButton(BattleInfoWidget)
        self.nextButton.setObjectName(u"nextButton")
        self.nextButton.setGeometry(QRect(630, 490, 161, 61))
        sizePolicy.setHeightForWidth(self.nextButton.sizePolicy().hasHeightForWidth())
        self.nextButton.setSizePolicy(sizePolicy)
        self.nextButton.setFont(font1)
        self.battle_num = QLabel(BattleInfoWidget)
        self.battle_num.setObjectName(u"battle_num")
        self.battle_num.setGeometry(QRect(240, 210, 341, 101))
        self.battle_num.setAlignment(Qt.AlignCenter)

        self.retranslateUi(BattleInfoWidget)

        QMetaObject.connectSlotsByName(BattleInfoWidget)
    # setupUi

    def retranslateUi(self, BattleInfoWidget):
        BattleInfoWidget.setWindowTitle(QCoreApplication.translate("BattleInfoWidget", u"Form", None))
        self.homeButton.setText(QCoreApplication.translate("BattleInfoWidget", u"GO HOME", None))
        self.simulateButton.setText(QCoreApplication.translate("BattleInfoWidget", u"SIMULATE", None))
        self.nextButton.setText(QCoreApplication.translate("BattleInfoWidget", u"NEXT BATTLE", None))
        self.battle_num.setText(QCoreApplication.translate("BattleInfoWidget", u"TextLabel", None))
    # retranslateUi

