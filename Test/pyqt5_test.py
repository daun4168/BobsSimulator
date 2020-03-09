import sys
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtCore import Qt, QSize, QRect, QPoint
from PyQt5.QtGui import QImage, QPalette, QBrush, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSizeGrip, QPushButton


class MyApp(QWidget):

    def __init__(self):
        super().__init__()

        self.title = 'Bobs Simulator'
        self.window_width = 800
        self.window_height = 480
        self.window_size = QSize(self.window_width, self.window_height)

        self.dragPos = 0
        self.is_window_move = False

        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setFixedSize(self.window_size)
        self.setWindowIcon(QIcon('res/bob.png'))
        # self.setAttribute(Qt.WA_TranslucentBackground)

        flags = QtCore.Qt.WindowFlags(int(QtCore.Qt.FramelessWindowHint) | int(QtCore.Qt.WindowStaysOnTopHint))
        self.setWindowFlags(flags)
        vboxlayout = QVBoxLayout()

        oimage = QImage("res/background.jpg")
        simage = oimage.scaled(self.window_size)

        palette = QPalette()
        palette.setBrush(10, QBrush(simage))
        self.setPalette(palette)

        x_button_loc = QPoint(int(self.window_width * 0.95), int(self.window_height * 0.03))
        x_button_size = QSize(int(self.window_height * 0.05), int(self.window_height * 0.05))

        self.button = QPushButton('', self)
        self.button.clicked.connect(self.close)
        self.button.setIcon(QtGui.QIcon('res/xbutton.svg'))
        self.button.setIconSize(QtCore.QSize(24, 24))
        self.button.resize(x_button_size)
        self.button.move(x_button_loc)
        self.button.setStyleSheet("background-color: rgba(255, 255, 255, 0);")

        self.show()

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
    ex = MyApp()
    sys.exit(app.exec_())
