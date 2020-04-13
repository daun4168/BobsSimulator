import sys

from PySide2.QtGui import QImage, QPixmap, QFont
from PySide2.QtCore import QRect
from PySide2.QtWidgets import QWidget, QApplication

from BobsSimulator.Draw import draw_minion, draw_minions, draw_hero
from BobsSimulator.HSType import Battle, Minion
from BobsSimulator.UI.BattleInfoWidgetUI import Ui_BattleInfoWidget


class BattleInfoWidget(QWidget):
    def __init__(self, battle: Battle, parent=None):
        QWidget.__init__(self, parent)

        self.ui = Ui_BattleInfoWidget()
        self.ui.setupUi(self)

        draw_minions(battle.me, self, -150, 320)
        draw_minions(battle.enemy, self, -150, -20)

        hero_widget = QWidget(self)
        hero_widget.setGeometry(QRect(600, 190, 170, 170))
        draw_hero(hero_widget, battle.me.hero.card_id, hp=battle.me.hero.hp())

        hero_widget = QWidget(self)
        hero_widget.setGeometry(QRect(30, 130, 170, 170))
        draw_hero(hero_widget, battle.enemy.hero.card_id, hp=battle.enemy.hero.hp())


        self.ui.battle_num.setText(f"BATTLE {battle.battle_num}")
        font = QFont("Times", 50)
        font.setBold(True)
        self.ui.battle_num.setFont(font)
        self.ui.battle_num.setStyleSheet(f"QLabel {{ color: white; }}")

        if parent:
            self.ui.homeButton.clicked.connect(parent.home)
            self.ui.simulateButton.clicked.connect(parent.simulate)
            self.ui.nextButton.clicked.connect(parent.next_battle)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    new_battle = Battle()

    new_minion = Minion()
    new_minion.card_id = "EX1_062"
    new_minion.attack = 3
    new_minion.health = 7
    new_minion.golden = True
    new_minion.elite = True
    new_minion.divine_shield = True
    new_battle.me.append_minion(new_minion)

    new_minion = Minion()
    new_minion.card_id = "EX1_062"
    new_minion.attack = 3
    new_minion.health = 7
    new_minion.damage = 4
    new_minion.golden = True
    new_minion.elite = True
    new_minion.poisonous = True
    new_battle.me.append_minion(new_minion)

    new_minion = Minion()
    new_minion.card_id = "EX1_062"
    new_minion.attack = 3
    new_minion.health = 7
    new_minion.damage = 4
    new_minion.golden = True
    new_minion.elite = True
    new_minion.taunt = True
    new_battle.me.append_minion(new_minion)

    new_minion = Minion()
    new_minion.card_id = "EX1_062"
    new_minion.attack = 3
    new_minion.health = 7
    new_minion.damage = 4
    new_minion.golden = True
    new_minion.elite = True
    new_battle.me.append_minion(new_minion)

    new_minion = Minion()
    new_minion.card_id = "EX1_507"
    new_minion.attack = 77
    new_minion.health = 6
    new_battle.enemy.append_minion(new_minion)

    new_minion = Minion()
    new_minion.card_id = "EX1_507"
    new_minion.attack = 77
    new_minion.health = 6
    new_battle.enemy.append_minion(new_minion)

    new_minion = Minion()
    new_minion.card_id = "EX1_507"
    new_minion.attack = 77
    new_minion.health = 6
    new_minion.damage = 3
    new_minion.deathrattle = True
    new_battle.enemy.append_minion(new_minion)

    new_minion = Minion()
    new_minion.card_id = "EX1_507"
    new_minion.attack = 77
    new_minion.health = 6
    new_minion.damage = 3
    new_minion.taunt = True
    new_minion.deathrattle = True
    new_minion.poisonous = True
    new_battle.enemy.append_minion(new_minion)

    new_minion = Minion()
    new_minion.card_id = "EX1_507"
    new_minion.attack = 77
    new_minion.health = 6
    new_minion.damage = 3
    new_minion.divine_shield = True
    new_minion.poisonous = True
    new_battle.enemy.append_minion(new_minion)

    ex = BattleInfoWidget(new_battle)
    ex.show()
    sys.exit(app.exec_())
