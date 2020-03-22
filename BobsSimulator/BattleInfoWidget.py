import sys
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from BobsSimulator.UI.BattleInfoWidgetUI import Ui_BattleInfoWidget
from BobsSimulator.HSType import Battle, Minion
from BobsSimulator.Draw import draw_minion
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
            draw_minion(widget, minion.card_id, minion.attack, minion.health - minion.damage, minion.elite, minion.golden)

        for minion in battle.enemy_board:
            if minion is None:
                continue
            widget = QWidget(self)
            widget.setGeometry(QRect(-150 + minion.pos * 115 + (7 - enemy_minion_num) * 57.5, -20, 178, 178))
            draw_minion(widget, minion.card_id, minion.attack, minion.health - minion.damage, minion.elite, minion.golden)

        if parent:
            self.ui.homeButton.clicked.connect(parent.home)
            self.ui.simulateButton.clicked.connect(parent.simulate)
            self.ui.nextButton.clicked.connect(parent.next_battle)


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
