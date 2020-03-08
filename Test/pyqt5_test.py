import sys
from PyQt5.QtGui import QImage, QPalette, QBrush, QIcon
from PyQt5.QtCore import QSize, Qt
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSizeGrip






class MyApp(QWidget):

    def __init__(self):
        super().__init__()

        self.title = 'Bobs Simulator'
        self.window_width = 800
        self.window_height = 480
        self.window_size = QSize(self.window_width, self.window_height)

        self.dragPos = 0

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


        self.show()

    def mousePressEvent(self, event):
        pass
        if event.buttons() == Qt.LeftButton:
            self.dragPos = event.globalPos()
            event.accept()

    def mouseMoveEvent(self, event):

        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
