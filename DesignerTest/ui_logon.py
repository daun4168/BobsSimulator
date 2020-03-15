# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Logon.ui'
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


class Ui_Logon(object):
    def setupUi(self, Logon):
        if Logon.objectName():
            Logon.setObjectName(u"Logon")
        Logon.resize(1200, 800)
        icon = QIcon()
        icon.addFile(u"../res/app.ico", QSize(), QIcon.Normal, QIcon.Off)
        Logon.setWindowIcon(icon)
        self.widget = QWidget(Logon)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(30, 20, 251, 81))
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.lineEditId = QLineEdit(self.widget)
        self.lineEditId.setObjectName(u"lineEditId")

        self.gridLayout.addWidget(self.lineEditId, 0, 1, 1, 1)

        self.labelPW = QLabel(self.widget)
        self.labelPW.setObjectName(u"labelPW")
        font = QFont()
        font.setFamily(u"Agency FB")
        font.setPointSize(14)
        self.labelPW.setFont(font)

        self.gridLayout.addWidget(self.labelPW, 1, 0, 1, 1)

        self.lineEditPW = QLineEdit(self.widget)
        self.lineEditPW.setObjectName(u"lineEditPW")
        self.lineEditPW.setEchoMode(QLineEdit.Password)

        self.gridLayout.addWidget(self.lineEditPW, 1, 1, 1, 1)

        self.labelId = QLabel(self.widget)
        self.labelId.setObjectName(u"labelId")
        self.labelId.setFont(font)

        self.gridLayout.addWidget(self.labelId, 0, 0, 1, 1)

        self.widget1 = QWidget(Logon)
        self.widget1.setObjectName(u"widget1")
        self.widget1.setGeometry(QRect(30, 110, 251, 26))
        self.horizontalLayout = QHBoxLayout(self.widget1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(88, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.ButtonOk = QPushButton(self.widget1)
        self.ButtonOk.setObjectName(u"ButtonOk")
        icon1 = QIcon()
        icon1.addFile(u"../res/img/attack_minion.png", QSize(), QIcon.Normal, QIcon.Off)
        self.ButtonOk.setIcon(icon1)

        self.horizontalLayout.addWidget(self.ButtonOk)

#if QT_CONFIG(shortcut)
        self.labelPW.setBuddy(self.lineEditPW)
        self.labelId.setBuddy(self.lineEditId)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.lineEditId, self.lineEditPW)
        QWidget.setTabOrder(self.lineEditPW, self.ButtonOk)

        self.retranslateUi(Logon)

        QMetaObject.connectSlotsByName(Logon)
    # setupUi

    def retranslateUi(self, Logon):
        Logon.setWindowTitle(QCoreApplication.translate("Logon", u"Logon", None))
        self.labelPW.setText(QCoreApplication.translate("Logon", u"&Password:", None))
        self.labelId.setText(QCoreApplication.translate("Logon", u"&id:", None))
        self.ButtonOk.setText(QCoreApplication.translate("Logon", u"Ok", None))
    # retranslateUi

