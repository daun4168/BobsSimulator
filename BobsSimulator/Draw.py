from PySide2.QtCore import Qt, QSize, QRect, QPoint
from PySide2.QtGui import *
from PySide2.QtWidgets import *


def draw_hero(widget, card_id):
    pic = QLabel(widget)
    pixmap = QPixmap(712, 712)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.drawPixmap(100, 100, 512, 512, QPixmap(f"res/img/cards/512x/{card_id}.jpg"))

    painter.setCompositionMode(QPainter.CompositionMode_DestinationIn)
    painter.drawPixmap(100, 100, 512, 512, QPixmap("res/img/hero_mask.png"))
    painter.setCompositionMode(QPainter.CompositionMode_SourceOver)

    painter.drawPixmap(81, 25, 550, 637, QPixmap(f"res/img/hero_frame.png"))

    painter.end()
    pixmap = pixmap.scaled(widget.size(), mode=Qt.SmoothTransformation)
    pic.resize(widget.size())
    pic.setPixmap(pixmap)
    pic.show()

def draw_minion(widget, card_id, attack=0, health=0, is_legendary=False, is_golden=False):
    pic = QLabel(widget)
    pixmap = QPixmap(712, 712)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.drawPixmap(100, 100, 512, 512, QPixmap(f"res/img/cards/512x/{card_id}.jpg"))

    painter.setCompositionMode(QPainter.CompositionMode_DestinationIn)
    painter.drawPixmap(0, 0, 712, 712, QPixmap("res/img/minion_mask.png"))
    painter.setCompositionMode(QPainter.CompositionMode_SourceOver)

    if not is_legendary and not is_golden:
        painter.drawPixmap(166, 100, 390, 512, QPixmap(f"res/img/minion_common.png"))
    elif not is_legendary and is_golden:
        painter.drawPixmap(135, 95, 450, 522, QPixmap(f"res/img/minion_golden_common.png"))
    elif is_legendary and not is_golden:
        painter.drawPixmap(166, 50, 508, 562, QPixmap(f"res/img/minion_legendary.png"))
    elif is_legendary and is_golden:
        painter.drawPixmap(135, 40, 570, 576, QPixmap(f"res/img/minion_golden_legendary.png"))

    painter.drawPixmap(150, 410, 154, 173, QPixmap(f"res/img/attack_minion.png"))
    painter.drawPixmap(435, 405, 130, 191, QPixmap(f"res/img/cost_health.png"))

    QFontDatabase.addApplicationFont('res/font/BelweMediumBT.ttf')
    number_font = QFont()
    number_font.setFamily("Belwe Medium BT")
    number_font.setPointSize(80)
    painter.setFont(number_font)

    draw_outlined_text(painter, str(attack), 110, 405)
    draw_outlined_text(painter, str(health), 380, 405)

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
            self.initUI()

        def initUI(self):
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


