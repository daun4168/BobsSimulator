import sys
import os

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt, QSize, QRect, QPoint
from PySide2.QtGui import *
from PySide2.QtWidgets import *


from Test import LogHandler




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
        self.move(QPoint(50, 50))
        self.dragPos = 0
        self.is_window_move = False

        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setFixedSize(self.window_size)
        self.setWindowIcon(QIcon(path('res/img/icon_bob.png')))
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)

        # flags = QtCore.Qt.WindowFlags(int(QtCore.Qt.FramelessWindowHint) | int(QtCore.Qt.WindowStaysOnTopHint))
        flags = QtCore.Qt.WindowFlags(int(QtCore.Qt.WindowStaysOnTopHint))
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

        self.draw_minion("BOT_606", is_golden=True, attack=2345, health=878)
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

        QFontDatabase.addApplicationFont(path('res/font/BelweMediumBT.ttf'))
        number_font = QFont()
        number_font.setFamily("Belwe Medium BT")
        number_font.setPointSize(80)
        painter.setFont(number_font)

        self.drawOutlinedText(painter, str(attack), 115, 405)
        self.drawOutlinedText(painter, str(health), 380, 405)

        painter.end()

        pixmap = pixmap.scaled(size)
        pic.setPixmap(pixmap)
        pic.resize(size)
        pic.move(point)
        pic.show()  # You were missing this.
        return pic

    def drawOutlinedText(self, painter, text, x, y, outline_size=3, width=250, height=200, text_color=Qt.white, outline_color=Qt.black):
        pen = QPen()
        pen.setColor(outline_color)
        painter.setPen(pen)

        painter.drawText(QRect(x + outline_size, y + outline_size, width, height), int(Qt.AlignCenter), text)
        painter.drawText(QRect(x + outline_size, y - outline_size, width, height), int(Qt.AlignCenter), text)
        painter.drawText(QRect(x - outline_size, y + outline_size, width, height), int(Qt.AlignCenter), text)
        painter.drawText(QRect(x - outline_size, y - outline_size, width, height), int(Qt.AlignCenter), text)
        painter.drawText(QRect(x, y + outline_size, width, height), int(Qt.AlignCenter), text)
        painter.drawText(QRect(x, y - outline_size, width, height), int(Qt.AlignCenter), text)
        painter.drawText(QRect(x + outline_size, y, width, height), int(Qt.AlignCenter), text)
        painter.drawText(QRect(x - outline_size, y, width, height), int(Qt.AlignCenter), text)

        pen = QPen()
        pen.setColor(text_color)
        painter.setPen(pen)

        painter.drawText(QRect(x, y, width, height), int(Qt.AlignCenter), text)

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


def battle_start_handler(battle_num):
    print(f"{battle_num}, START BATTLE!!!!")

if __name__ == '__main__':
    HS_LOG_FILE_DIR= os.path.join(os.getcwd(), "Test/logs")
    log_file_2020_03_06_20_31_28 = open(os.path.join(HS_LOG_FILE_DIR, "2020-03-06 20-31-28.log"), 'r', encoding="UTF8")
    game = LogHandler.HSGame(log_file_2020_03_06_20_31_28)

    game.battle_start.connect(battle_start_handler)

    game.line_reader()



    try:
        app = QApplication(sys.argv)
        ex = MyApp()
        sys.exit(app.exec_())

    except Exception as e:
        print("Exception!!!!!!!!!!")
        print(e)
        input()
