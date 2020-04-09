from PySide2.QtCore import Qt, QRect
from PySide2.QtGui import QPixmap, QFont, QPainter, QFontDatabase, QPen
from PySide2.QtWidgets import QWidget, QApplication, QLabel

from BobsSimulator.HSType import Minion
from BobsSimulator.Main import CARD_RES


def draw_hero(widget, card_id):
    pic = QLabel(widget)
    pixmap = QPixmap(712, 712)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.drawPixmap(100, 100, 512, 512, QPixmap(f"res/img/cards/{CARD_RES}/{card_id}.jpg"))

    painter.setCompositionMode(QPainter.CompositionMode_DestinationIn)
    painter.drawPixmap(100, 100, 512, 512, QPixmap("res/img/hero_mask.png"))
    painter.setCompositionMode(QPainter.CompositionMode_SourceOver)

    painter.drawPixmap(81, 25, 550, 637, QPixmap(f"res/img/hero_frame.png"))

    painter.end()
    pixmap = pixmap.scaled(widget.size(), mode=Qt.SmoothTransformation)
    pic.resize(widget.size())
    pic.setPixmap(pixmap)
    pic.show()


def draw_minion(widget, minion: Minion):
    pic = QLabel(widget)
    pixmap = QPixmap(712, 712)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)

    painter.drawPixmap(100, 100, 512, 512, QPixmap(f"res/img/cards/{CARD_RES}/{minion.card_id}.jpg"))
    painter.setCompositionMode(QPainter.CompositionMode_DestinationIn)
    painter.drawPixmap(0, 0, 712, 712, QPixmap("res/img/minion_mask.png"))
    painter.setCompositionMode(QPainter.CompositionMode_SourceOver)

    painter.setCompositionMode(QPainter.CompositionMode_DestinationAtop)
    if minion.taunt:
        if minion.golden:
            painter.drawPixmap(60, 30, 600, 700, QPixmap(f"res/img/images/inplay_minion_taunt_premium.png"))
        else:
            painter.drawPixmap(60, 30, 600, 700, QPixmap(f"res/img/images/inplay_minion_taunt.png"))
    painter.setCompositionMode(QPainter.CompositionMode_SourceOver)

    if not minion.elite and not minion.golden:
        painter.drawPixmap(166, 100, 390, 512, QPixmap(f"res/img/minion_common.png"))
    elif not minion.elite and minion.golden:
        painter.drawPixmap(135, 95, 450, 522, QPixmap(f"res/img/minion_golden_common.png"))
    elif minion.elite and not minion.golden:
        painter.drawPixmap(166, 50, 508, 562, QPixmap(f"res/img/minion_legendary.png"))
    elif minion.elite and minion.golden:
        painter.drawPixmap(135, 40, 570, 576, QPixmap(f"res/img/minion_golden_legendary.png"))

    painter.drawPixmap(150, 410, 154, 173, QPixmap(f"res/img/attack_minion.png"))
    painter.drawPixmap(435, 405, 130, 191, QPixmap(f"res/img/cost_health2.png"))

    QFontDatabase.addApplicationFont('res/font/BelweMediumBT.ttf')
    number_font = QFont()
    number_font.setFamily("Belwe Medium BT")
    number_font.setPointSize(80)
    painter.setFont(number_font)

    draw_outlined_text(painter, str(minion.attack), 110, 405)
    if minion.damage == 0:
        draw_outlined_text(painter, str(minion.health), 380, 405)
    else:
        draw_outlined_text(painter, str(minion.health - minion.damage), 380, 405, text_color=Qt.red)

    if minion.poisonous and minion.deathrattle:
        painter.drawPixmap(120, 30, 600, 700, QPixmap(f"res/img/images/icon_deathrattle.png"))
        painter.drawPixmap(0, 30, 600, 700, QPixmap(f"res/img/images/icon_poisonous.png"))
    elif minion.poisonous:
        painter.drawPixmap(60, 30, 600, 700, QPixmap(f"res/img/images/icon_poisonous.png"))
    elif minion.deathrattle:
        painter.drawPixmap(60, 30, 600, 700, QPixmap(f"res/img/images/icon_deathrattle.png"))

    if minion.divine_shield:
        painter.drawPixmap(60, 30, 600, 700, QPixmap(f"res/img/images/inplay_minion_divine_shield.png"))

    painter.end()
    pixmap = pixmap.scaled(widget.size(), mode=Qt.SmoothTransformation)
    pic.resize(widget.size())
    pic.setPixmap(pixmap)
    pic.show()


def draw_outlined_text(painter, text, x, y, outline_size=5, width=250, height=200, text_color=Qt.white, outline_color=Qt.black):
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


if __name__ == "__main__":
    import sys

    class App(QWidget):
        def __init__(self):
            super().__init__()
            self.title = 'TEST'
            self.left = 100
            self.top = 100
            self.width = 712
            self.height = 712
            self.init_ui()

        def init_ui(self):
            self.setWindowTitle(self.title)
            self.setGeometry(self.left, self.top, self.width, self.height)

            # Create widget
            widget = QWidget(self)
            widget.setGeometry(QRect(0, 0, 712, 712))
            draw_hero(widget, "TB_BaconShop_HERO_49")
            self.show()


    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
