import sys
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtCore import Qt, QSize, QRect, QPoint
from PyQt5.QtGui import QImage, QPalette, QBrush, QIcon, QPixmap, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSizeGrip, QPushButton, QLabel


class MyApp(QWidget):

    def __init__(self):
        super().__init__()

        self.title = 'Bobs Simulator'
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())