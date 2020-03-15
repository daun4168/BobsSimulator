# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DefaultWindow.ui'
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


class Ui_DefaultWindow(object):
    def setupUi(self, DefaultWindow):
        if DefaultWindow.objectName():
            DefaultWindow.setObjectName(u"DefaultWindow")
        DefaultWindow.resize(800, 600)
        self.centralwidget = QWidget(DefaultWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        DefaultWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(DefaultWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        DefaultWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(DefaultWindow)
        self.statusbar.setObjectName(u"statusbar")
        DefaultWindow.setStatusBar(self.statusbar)

        self.retranslateUi(DefaultWindow)

        QMetaObject.connectSlotsByName(DefaultWindow)
    # setupUi

    def retranslateUi(self, DefaultWindow):
        DefaultWindow.setWindowTitle(QCoreApplication.translate("DefaultWindow", u"MainWindow", None))
    # retranslateUi

