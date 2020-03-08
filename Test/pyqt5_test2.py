from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSizeGrip
from PyQt5 import QtCore
import sys


class Marker(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.title = "PyQt5 Size Grip"
        self.top = 200
        self.left = 500
        self.width = 640
        self.height = 480
        self.setWindowTitle(self.title)
        self.setWindowFlags(QtCore.Qt.Widget | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.clicked = False

    def paintEvent(self, ev):
        p = QtGui.QPainter(self)
        p.fillRect(self.rect(), QtGui.QColor(128, 128, 128, 128))

    def mousePressEvent(self, ev):
        self.old_pos = ev.screenPos()

    def mouseMoveEvent(self, ev):
        if self.clicked:
            dx = self.old_pos.x() - ev.screenPos().x()
            dy = self.old_pos.y() - ev.screenPos().y()
            self.move(self.pos().x() - dx, self.pos().y() - dy)
        self.old_pos = ev.screenPos()
        self.clicked = True
        return QWidget.mouseMoveEvent(self, ev)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "PyQt5 Size Grip"
        self.top = 200
        self.left = 500
        self.width = 640
        self.height = 480
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setGeometry(self.left, self.top, self.width, self.height)
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(flags)
        vboxlayout = QVBoxLayout()
        sizegrip = QSizeGrip(self)
        #sizegrip.setVisible(True)
        vboxlayout.addWidget(sizegrip)
        self.setLayout(vboxlayout)
        self.show()



if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Marker()
    sys.exit(App.exec())