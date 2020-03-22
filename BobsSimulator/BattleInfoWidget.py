import sys
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from BobsSimulator.UI.BattleInfoWidgetUI import Ui_BattleInfoWidget
from BobsSimulator.HSType import Battle, Minion
from PySide2.QtCore import Qt, QSize, QRect, QPoint


class BattleInfoWidget(QWidget):
    def __init__(self, battle, parent=None):
        QWidget.__init__(self, parent)

        self.ui = Ui_BattleInfoWidget()
        self.ui.setupUi(self)

        player_minion_num = len(battle.player_board) - battle.player_board.count(None)
        enemy_minion_num = len(battle.enemy_board) - battle.enemy_board.count(None)

        for minion in battle.player_board:
            if minion is None:
                continue
            widget = QWidget(self)
            widget.setGeometry(QRect(-150 + minion.pos * 115 + (7 - player_minion_num) * 57.5, 220, 178, 178))
            self.draw_minion(widget, minion.card_id, minion.attack, minion.health - minion.damage, minion.elite, minion.golden)

        for minion in battle.enemy_board:
            if minion is None:
                continue
            widget = QWidget(self)
            widget.setGeometry(QRect(-150 + minion.pos * 115 + (7 - enemy_minion_num) * 57.5, -20, 178, 178))
            self.draw_minion(widget, minion.card_id, minion.attack, minion.health - minion.damage, minion.elite, minion.golden)

        if parent:
            self.ui.homeButton.clicked.connect(parent.home)
            self.ui.simulateButton.clicked.connect(parent.simulate)
            self.ui.nextButton.clicked.connect(parent.next_battle)

    @staticmethod
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

        BattleInfoWidget.draw_outlined_text(painter, str(attack), 110, 405)
        BattleInfoWidget.draw_outlined_text(painter, str(health), 380, 405)

        painter.end()

        pixmap = pixmap.scaled(widget.size(), mode=Qt.SmoothTransformation)
        pic.resize(widget.size())
        pic.setPixmap(pixmap)
        pic.show()

    @staticmethod
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



if __name__ == '__main__':
    app = QApplication(sys.argv)
    battle = Battle()

    for i in range(1, 6):
        minion = Minion()
        battle.player_board[i] = minion
        minion.card_id = "EX1_062"
        minion.attack = 103
        minion.health = 7
        minion.golden = True
        minion.elite = True
        minion.pos = i

    for i in range(1, 5):
        minion = Minion()
        battle.enemy_board[i] = minion
        minion.card_id = "EX1_507"
        minion.attack = 55
        minion.health = 330
        minion.pos = i

    ex = BattleInfoWidget(battle)
    ex.show()
    sys.exit(app.exec_())
