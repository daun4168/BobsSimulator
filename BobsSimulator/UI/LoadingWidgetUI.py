# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'LoadingWidget.ui'
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
        self.progressBar = QProgressBar(LoadingWidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(30, 290, 731, 71))
        self.progressBar.setValue(24)
        self.progressBar.setTextVisible(False)
        self.progressBar.setInvertedAppearance(False)
        self.loadingTextLabel = QLabel(LoadingWidget)
        self.loadingTextLabel.setObjectName(u"loadingTextLabel")
        self.loadingTextLabel.setGeometry(QRect(510, 450, 261, 101))

        self.retranslateUi(LoadingWidget)

        QMetaObject.connectSlotsByName(LoadingWidget)
    # setupUi

    def retranslateUi(self, LoadingWidget):
        LoadingWidget.setWindowTitle(QCoreApplication.translate("LoadingWidget", u"Form", None))
        self.logoLabel.setText("")
        self.loadingTextLabel.setText("")
    # retranslateUi

