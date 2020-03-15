import sys
import os
from PySide2.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QGridLayout,
                               QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox)
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt, Signal
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt, QSize, QRect, QPoint
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from DesignerTest.ui_logon import Ui_Logon

def path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Logon(QWidget):
    ok = Signal()

    def __init__(self,ids,pws):
        QWidget.__init__(self)

        self.listIds = ids
        self.listPWs = pws

        self.ui = Ui_Logon()
        self.ui.setupUi(self)

        self.window_width = self.width()
        self.window_height = self.height()
        self.window_size = QSize(self.window_width, self.window_height)

        print(self.width())

        # self.setFixedSize(self.window_size)

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        flags = QtCore.Qt.WindowFlags(int(QtCore.Qt.FramelessWindowHint) | int(QtCore.Qt.WindowStaysOnTopHint))
        self.setWindowFlags(flags)

        oimage = QImage(path("res/img/background.jpg"))
        simage = oimage.scaled(self.window_size)

        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(simage))
        self.setPalette(palette)

        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(simage))
        self.setPalette(palette)

        x_button_loc = QPoint(int(self.window_width * 0.95), int(self.window_height * 0.03))
        x_button_size = QSize(int(self.window_height * 0.05), int(self.window_height * 0.05))

        self.button = QPushButton('', self)
        self.button.clicked.connect(self.close)
        self.button.setIcon(QtGui.QIcon(path('res/img/x_icon_2.png')))
        self.button.setIconSize(QtCore.QSize(24, 24))
        self.button.resize(x_button_size)
        self.button.move(x_button_loc)
        self.button.setStyleSheet("background-color: rgba(255, 255, 255, 0);")

        self.ui.ButtonOk.clicked.connect(self.onOk)

    def onOk(self):
        if (self.ui.lineEditId.text() not in self.listIds):
            QMessageBox.critical(self,"Logon error","Unregistered user")
            self.ui.lineEditId.setFocus()
        else:
            idx = self.listIds.index(self.ui.lineEditId.text())
            if self.ui.lineEditPW.text() != self.listPWs[idx] :
                QMessageBox.critical(self,"Logon error","Incroreect password")
                self.ui.lineEditPW.setFocus()
            else:
                self.ok.emit()

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton and event.y() < self.window_height * 0.1:
            self.is_window_move = True
            self.dragPos = event.globalPos()
            event.accept()
        else:
            self.is_window_move = False

    def mouseMoveEvent(self, event):

        if self.is_window_move and event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    ids = ['James','John','Jane']
    pws = ['123','456','789']

    logon = Logon(ids,pws)
    logon.ok.connect(app.exit)

    logon.show()
    app.exec_()