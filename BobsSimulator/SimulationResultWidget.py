import sys
from PySide2.QtGui import QImage, QPixmap, QFont
from PySide2.QtCore import QRect, Qt
from PySide2.QtWidgets import QWidget, QApplication, QLabel

from BobsSimulator.UI.SimulationResultWidgetUI import Ui_SimulationResultWidget
from BobsSimulator.HSType import Battle
from BobsSimulator.Draw import draw_minions


class SimulationResultWidget(QWidget):
    def __init__(self, my_battle: Battle, my_result: list, parent=None):
        QWidget.__init__(self, parent)

        self.ui = Ui_SimulationResultWidget()
        self.ui.setupUi(self)

        self.ui.title.setText(f"Simulation Result")
        font = QFont("배달의민족 주아", 35, QFont.Bold)
        self.ui.title.setFont(font)
        self.ui.title.setStyleSheet(f"QLabel {{ color: white; }}")

        self.my_battle = my_battle

        draw_minions(my_battle.enemy, self, -150, 50)
        draw_minions(my_battle.me, self, -150, 250)

        score = sum(my_result) / len(my_result)
        win_ratio = sum(x > 0 for x in my_result) / len(my_result)
        draw_ratio = sum(x == 0 for x in my_result) / len(my_result)
        lose_ratio = sum(x < 0 for x in my_result) / len(my_result)

        self.ui.your_arr.setText(f"Your Damage: {score:2.1f}, Win: {win_ratio:2.1%}, Draw: {draw_ratio:2.1%}, Lose: {lose_ratio:2.1%}")
        font = QFont("배달의민족 주아", 18)
        self.ui.your_arr.setFont(font)
        self.ui.your_arr.setStyleSheet(f"QLabel {{ color: white; }}")

        self.ui.homeButton.setFont(QFont("배달의민족 주아", 15, QFont.Bold))
        self.ui.nextButton.setFont(QFont("배달의민족 주아", 15, QFont.Bold))
        self.ui.actualResult.setFont(QFont("배달의민족 주아", 15, QFont.Bold))

        self.ui.actualResult.clicked.connect(self.show_actual_result)

        if parent:
            self.ui.homeButton.clicked.connect(parent.home)
            self.ui.nextButton.clicked.connect(parent.next_battle)

    def show_actual_result(self):
        geo = self.ui.actualResult.geometry()
        self.ui.actualResult.setParent(None)
        self.ui.actualResult = QLabel(self)
        self.ui.actualResult.setAlignment(Qt.AlignCenter)
        self.ui.actualResult.setFont(QFont("배달의민족 주아", 22, QFont.Bold))
        self.ui.actualResult.setGeometry(geo)
        self.ui.actualResult.setStyleSheet(f"QLabel {{ color: white; }}")

        taken_damage = self.my_battle.me.hero.taken_damage
        give_damage = self.my_battle.enemy.hero.taken_damage

        text = ""

        if taken_damage == 0 and give_damage == 0:
            text += "Draw"
        elif taken_damage > 0:
            text += f"Lose: {taken_damage} Damage"
        elif give_damage > 0:
            text += f"Win: {give_damage} Damage"

        self.ui.actualResult.setText(text)

        self.ui.actualResult.show()
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pass


