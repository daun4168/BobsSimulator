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


class Ui_ErrorWidget(object):
    def setupUi(self, ErrorWidget):
        if ErrorWidget.objectName():
            ErrorWidget.setObjectName(u"ErrorWidget")
        ErrorWidget.resize(800, 570)
        self.homeButton = QPushButton(ErrorWidget)
        self.homeButton.setObjectName(u"homeButton")
        self.homeButton.setGeometry(QRect(140, 490, 261, 61))
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.homeButton.sizePolicy().hasHeightForWidth())
        self.homeButton.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamily(u"Yu Gothic")
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.homeButton.setFont(font)
        self.homeButton_2 = QPushButton(ErrorWidget)
        self.homeButton_2.setObjectName(u"homeButton_2")
        self.homeButton_2.setGeometry(QRect(440, 490, 251, 61))
        sizePolicy.setHeightForWidth(self.homeButton_2.sizePolicy().hasHeightForWidth())
        self.homeButton_2.setSizePolicy(sizePolicy)
        self.homeButton_2.setFont(font)
        self.layoutWidget = QWidget(ErrorWidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 230, 781, 121))
        self.pboard = QGridLayout(self.layoutWidget)
        self.pboard.setObjectName(u"pboard")
        self.pboard.setContentsMargins(0, 0, 0, 0)
        self.pcard4 = QWidget(self.layoutWidget)
        self.pcard4.setObjectName(u"pcard4")

        self.pboard.addWidget(self.pcard4, 0, 3, 1, 1)

        self.pcard1 = QWidget(self.layoutWidget)
        self.pcard1.setObjectName(u"pcard1")

        self.pboard.addWidget(self.pcard1, 0, 0, 1, 1)

        self.pcard5 = QWidget(self.layoutWidget)
        self.pcard5.setObjectName(u"pcard5")

        self.pboard.addWidget(self.pcard5, 0, 4, 1, 1)

        self.pcard7 = QWidget(self.layoutWidget)
        self.pcard7.setObjectName(u"pcard7")

        self.pboard.addWidget(self.pcard7, 0, 6, 1, 1)

        self.pcard3 = QWidget(self.layoutWidget)
        self.pcard3.setObjectName(u"pcard3")

        self.pboard.addWidget(self.pcard3, 0, 2, 1, 1)

        self.pcard6 = QWidget(self.layoutWidget)
        self.pcard6.setObjectName(u"pcard6")

        self.pboard.addWidget(self.pcard6, 0, 5, 1, 1)

        self.pcard2 = QWidget(self.layoutWidget)
        self.pcard2.setObjectName(u"pcard2")

        self.pboard.addWidget(self.pcard2, 0, 1, 1, 1)

        self.layoutWidget_2 = QWidget(ErrorWidget)
        self.layoutWidget_2.setObjectName(u"layoutWidget_2")
        self.layoutWidget_2.setGeometry(QRect(10, 350, 781, 81))
        self.pinfo = QGridLayout(self.layoutWidget_2)
        self.pinfo.setObjectName(u"pinfo")
        self.pinfo.setContentsMargins(0, 0, 0, 0)
        self.pinfo4 = QWidget(self.layoutWidget_2)
        self.pinfo4.setObjectName(u"pinfo4")

        self.pinfo.addWidget(self.pinfo4, 0, 3, 1, 1)

        self.pinfo1 = QWidget(self.layoutWidget_2)
        self.pinfo1.setObjectName(u"pinfo1")

        self.pinfo.addWidget(self.pinfo1, 0, 0, 1, 1)

        self.pinfo5 = QWidget(self.layoutWidget_2)
        self.pinfo5.setObjectName(u"pinfo5")

        self.pinfo.addWidget(self.pinfo5, 0, 4, 1, 1)

        self.pinfo7 = QWidget(self.layoutWidget_2)
        self.pinfo7.setObjectName(u"pinfo7")

        self.pinfo.addWidget(self.pinfo7, 0, 6, 1, 1)

        self.pinfo3 = QWidget(self.layoutWidget_2)
        self.pinfo3.setObjectName(u"pinfo3")

        self.pinfo.addWidget(self.pinfo3, 0, 2, 1, 1)

        self.pinfo6 = QWidget(self.layoutWidget_2)
        self.pinfo6.setObjectName(u"pinfo6")

        self.pinfo.addWidget(self.pinfo6, 0, 5, 1, 1)

        self.pinfo2 = QWidget(self.layoutWidget_2)
        self.pinfo2.setObjectName(u"pinfo2")

        self.pinfo.addWidget(self.pinfo2, 0, 1, 1, 1)

        self.layoutWidget_3 = QWidget(ErrorWidget)
        self.layoutWidget_3.setObjectName(u"layoutWidget_3")
        self.layoutWidget_3.setGeometry(QRect(9, 130, 781, 81))
        self.einfo = QGridLayout(self.layoutWidget_3)
        self.einfo.setObjectName(u"einfo")
        self.einfo.setContentsMargins(0, 0, 0, 0)
        self.einfo4 = QWidget(self.layoutWidget_3)
        self.einfo4.setObjectName(u"einfo4")

        self.einfo.addWidget(self.einfo4, 0, 3, 1, 1)

        self.einfo1 = QWidget(self.layoutWidget_3)
        self.einfo1.setObjectName(u"einfo1")

        self.einfo.addWidget(self.einfo1, 0, 0, 1, 1)

        self.einfo5 = QWidget(self.layoutWidget_3)
        self.einfo5.setObjectName(u"einfo5")

        self.einfo.addWidget(self.einfo5, 0, 4, 1, 1)

        self.einfo7 = QWidget(self.layoutWidget_3)
        self.einfo7.setObjectName(u"einfo7")

        self.einfo.addWidget(self.einfo7, 0, 6, 1, 1)

        self.einfo3 = QWidget(self.layoutWidget_3)
        self.einfo3.setObjectName(u"einfo3")

        self.einfo.addWidget(self.einfo3, 0, 2, 1, 1)

        self.einfo6 = QWidget(self.layoutWidget_3)
        self.einfo6.setObjectName(u"einfo6")

        self.einfo.addWidget(self.einfo6, 0, 5, 1, 1)

        self.einfo2 = QWidget(self.layoutWidget_3)
        self.einfo2.setObjectName(u"einfo2")

        self.einfo.addWidget(self.einfo2, 0, 1, 1, 1)

        self.widget = QWidget(ErrorWidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(9, 10, 781, 121))
        self.eboard = QGridLayout(self.widget)
        self.eboard.setObjectName(u"eboard")
        self.eboard.setContentsMargins(0, 0, 0, 0)
        self.ecard6 = QWidget(self.widget)
        self.ecard6.setObjectName(u"ecard6")

        self.eboard.addWidget(self.ecard6, 0, 5, 1, 1)

        self.ecard2 = QWidget(self.widget)
        self.ecard2.setObjectName(u"ecard2")

        self.eboard.addWidget(self.ecard2, 0, 1, 1, 1)

        self.ecard3 = QWidget(self.widget)
        self.ecard3.setObjectName(u"ecard3")

        self.eboard.addWidget(self.ecard3, 0, 2, 1, 1)

        self.ecard1 = QWidget(self.widget)
        self.ecard1.setObjectName(u"ecard1")

        self.eboard.addWidget(self.ecard1, 0, 0, 1, 1)

        self.ecard7 = QWidget(self.widget)
        self.ecard7.setObjectName(u"ecard7")

        self.eboard.addWidget(self.ecard7, 0, 6, 1, 1)

        self.ecard4 = QWidget(self.widget)
        self.ecard4.setObjectName(u"ecard4")

        self.eboard.addWidget(self.ecard4, 0, 3, 1, 1)

        self.ecard5 = QWidget(self.widget)
        self.ecard5.setObjectName(u"ecard5")

        self.eboard.addWidget(self.ecard5, 0, 4, 1, 1)


        self.retranslateUi(ErrorWidget)

        QMetaObject.connectSlotsByName(ErrorWidget)
    # setupUi

    def retranslateUi(self, ErrorWidget):
        ErrorWidget.setWindowTitle(QCoreApplication.translate("ErrorWidget", u"Form", None))
        self.homeButton.setText(QCoreApplication.translate("ErrorWidget", u"GO HOME", None))
        self.homeButton_2.setText(QCoreApplication.translate("ErrorWidget", u"SIMULATE", None))
    # retranslateUi

