import sys
import os

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt, QSize, QRect, QPoint
from PySide2.QtGui import *
from PySide2.QtWidgets import *

def path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class MyApp(QWidget):

    def __init__(self):
        super().__init__()

        self.title = 'Bobs Simulator'
        self.window_width = 1200
        self.window_height = 800
        self.window_size = QSize(self.window_width, self.window_height)
        self.move(50, 50)
        self.dragPos = 0
        self.is_window_move = False

        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setFixedSize(self.window_size)
        self.setWindowIcon(QIcon(path('res/img/icon_bob.png')))
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)

        flags = QtCore.Qt.WindowFlags(int(QtCore.Qt.FramelessWindowHint) | int(QtCore.Qt.WindowStaysOnTopHint))
        self.setWindowFlags(flags)

        oimage = QImage(path("res/img/background.jpg"))
        simage = oimage.scaled(self.window_size)

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

        self.draw_minion("BOT_606", is_golden=True, attack=4)
        self.show()

    def draw_minion(self, card_id, attack=0, health=0, is_legendary=False, is_golden=False, size=None, point=None):
        if not size:
            size = QSize(int(self.window_width * 0.2), int(self.window_width * 0.2))
            size = QSize(712, 712)
        if not point:
            point = QPoint(int(self.window_width * 0), int(self.window_height * 0))
        pic = QLabel(self)
        pixmap = QPixmap(712, 712)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.drawPixmap(100, 100, 512, 512, QPixmap(path(f"res/img/cards/512x/{card_id}.jpg")))

        painter.setCompositionMode(QPainter.CompositionMode_DestinationIn)
        painter.drawPixmap(0, 0, 712, 712, QPixmap(path("res/img/minion_mask.png")))
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)

        if not is_legendary and not is_golden:
            painter.drawPixmap(166, 100, 390, 512, QPixmap(path(f"res/img/minion_common.png")))
        elif not is_legendary and is_golden:
            painter.drawPixmap(135, 95, 450, 522, QPixmap(path(f"res/img/minion_golden_common.png")))
        elif is_legendary and not is_golden:
            painter.drawPixmap(166, 50, 508, 562, QPixmap(path(f"res/img/minion_legendary.png")))
        elif is_legendary and is_golden:
            painter.drawPixmap(135, 40, 570, 576, QPixmap(path(f"res/img/minion_golden_legendary.png")))

        painter.drawPixmap(150, 410, 154, 173, QPixmap(path(f"res/img/attack_minion.png")))
        painter.drawPixmap(430, 390, 143, 210, QPixmap(path(f"res/img/cost_health.png")))



        QFontDatabase.addApplicationFont(path('res/font/Franklin_Gothic_Book_Regular.ttf'))
        number_font = QFont()
        number_font.setFamily("Franklin Gothic Book Regular")
        number_font.setPointSize(76)
        painter.setFont(number_font)

        pen = QPen()
        pen.setColor(Qt.black)
        pen.setWidth(10)
        painter.setPen(pen)

        # painter.setFont(QFont('Arial Bold', 76))
        painter.drawText(QRect(140, 410, 200, 200), int(Qt.AlignCenter), str(attack))

        # pen = QPen()
        # pen.setColor(Qt.white)
        # pen.setWidth(2)
        # painter.setPen(pen)
        #
        # painter.setFont(QFont('Arial Bold', 70))
        # painter.drawText(QRect(140, 410, 200, 200), int(Qt.AlignCenter), str(attack))





        # pic.setAlignment(Qt.AlignCenter)
        # painter.drawText(200, 500, 'Default')
        #painter.drawText(QRect(200, 200, 200, 200), int(Qt.AlignCenter), 'Default')


        painter.end()


        pixmap = pixmap.scaled(size)
        pic.setPixmap(pixmap)
        pic.resize(size)
        pic.move(point)
        pic.show()  # You were missing this.
        return pic

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
    try:
        app = QApplication(sys.argv)
        ex = MyApp()
        sys.exit(app.exec_())

    except Exception as e:
        print("Exception!!!!!!!!!!")
        print(e)
        input()
