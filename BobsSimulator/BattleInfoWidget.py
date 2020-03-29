import sys

from PySide2.QtCore import QRect
from PySide2.QtWidgets import QWidget, QApplication

from BobsSimulator.Draw import draw_minion
from BobsSimulator.HSType import Battle, Minion
from BobsSimulator.UI.BattleInfoWidgetUI import Ui_BattleInfoWidget


class BattleInfoWidget(QWidget):
    def __init__(self, battle: Battle, parent=None):
        QWidget.__init__(self, parent)

        self.ui = Ui_BattleInfoWidget()
        self.ui.setupUi(self)

        for minion in battle.me.minions():
            widget = QWidget(self)
            widget.setGeometry(QRect(-150 + minion.pos * 115 + (7 - battle.me.minion_num()) * 57.5, 220, 178, 178))
            draw_minion(widget, minion.card_id, minion.attack, minion.health - minion.damage, minion.elite, minion.golden)

        for minion in battle.enemy.minions():
            if minion is None:
                continue
            widget = QWidget(self)
            widget.setGeometry(QRect(-150 + minion.pos * 115 + (7 - battle.enemy.minion_num()) * 57.5, -20, 178, 178))
            draw_minion(widget, minion.card_id, minion.attack, minion.health - minion.damage, minion.elite, minion.golden)

        if parent:
            self.ui.homeButton.clicked.connect(parent.home)
            self.ui.simulateButton.clicked.connect(parent.simulate)
            self.ui.nextButton.clicked.connect(parent.next_battle)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    new_battle = Battle()

    for i in range(5):
        new_minion = Minion()
        new_minion.card_id = "EX1_062"
        new_minion.attack = i * 3
        new_minion.health = 7
        new_minion.golden = True
        new_minion.elite = True
        new_battle.me.append_minion(new_minion)

    for i in range(4):
        new_minion = Minion()
        new_minion.card_id = "EX1_507"
        new_minion.attack = 77
        new_minion.health = i * 6
        new_battle.enemy.append_minion(new_minion)

    ex = BattleInfoWidget(new_battle)
    ex.show()
    sys.exit(app.exec_())
