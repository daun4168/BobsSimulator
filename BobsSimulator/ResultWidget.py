import sys
from PySide2.QtGui import QImage, QPixmap, QFont
from PySide2.QtCore import QRect
from PySide2.QtWidgets import QWidget, QApplication

from BobsSimulator.UI.ResultWidgetUI import Ui_ResultWidget
from BobsSimulator.HSType import Battle
from BobsSimulator.Draw import draw_minions


class ResultWidget(QWidget):
    def __init__(self, my_battle: Battle, my_result: list, best_battle: Battle, best_result: list, parent=None):
        QWidget.__init__(self, parent)

        self.ui = Ui_ResultWidget()
        self.ui.setupUi(self)

        self.ui.title.setText(f"Simulation Result")
        font = QFont("Times", 35)
        self.ui.title.setFont(font)
        self.ui.title.setStyleSheet(f"QLabel {{ color: white; }}")



        draw_minions(my_battle.me, self, -150, 50)

        score = sum(my_result) / len(my_result)
        win_ratio = sum(x > 0 for x in my_result) / len(my_result)
        draw_ratio = sum(x == 0 for x in my_result) / len(my_result)
        lose_ratio = sum(x < 0 for x in my_result) / len(my_result)

        self.ui.your_arr.setText(f"Your Damage: {score:2.1f}, Win: {win_ratio:2.1%}, Draw: {draw_ratio:2.1%}, Lose: {lose_ratio:2.1%}")
        font = QFont("Times", 22)
        self.ui.your_arr.setFont(font)
        self.ui.your_arr.setStyleSheet(f"QLabel {{ color: white; }}")



        draw_minions(best_battle.me, self, -150, 270)

        score = sum(best_result) / len(best_result)
        win_ratio = sum(x > 0 for x in best_result) / len(best_result)
        draw_ratio = sum(x == 0 for x in best_result) / len(best_result)
        lose_ratio = sum(x < 0 for x in best_result) / len(best_result)

        self.ui.best_arr.setText(f"Best Damage: {score:2.1f}, Win: {win_ratio:2.1%}, Draw: {draw_ratio:2.1%}, Lose: {lose_ratio:2.1%}")
        font = QFont("Times", 22)
        self.ui.best_arr.setFont(font)
        self.ui.best_arr.setStyleSheet(f"QLabel {{ color: white; }}")




        if parent:
            self.ui.homeButton.clicked.connect(parent.home)
            self.ui.nextButton.clicked.connect(parent.next_battle)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pass


