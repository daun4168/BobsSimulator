import sys
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QWidget, QApplication

from BobsSimulator.Draw import draw_hero
from BobsSimulator.UI.GameEndWidgetUI import Ui_GameEndWidget


class GameEndWidget(QWidget):
    def __init__(self, hero_card_id, rank_num, parent=None):
        QWidget.__init__(self, parent)

        self.ui = Ui_GameEndWidget()
        self.ui.setupUi(self)

        draw_hero(self.ui.heroImg, hero_card_id)

        self.ui.rankText.setText("YOUR FINAL RANK")
        font = QFont("Hambu Radul", 45, QFont.Bold)
        self.ui.rankText.setFont(font)
        self.ui.rankText.setStyleSheet(f"QLabel {{ color: orange; }}")

        font = QFont("Showlove", 120, QFont.Bold)
        self.ui.rankNumber.setFont(font)
        self.ui.rankNumber.setText(f"{rank_num}")
        self.ui.rankNumber.setStyleSheet(f"QLabel {{ color: orange; }}")

        self.ui.homeButton.setFont(QFont("배달의민족 주아", 15, QFont.Bold))
        self.ui.nextButton.setFont(QFont("배달의민족 주아", 15, QFont.Bold))

        if parent:
            self.ui.homeButton.clicked.connect(parent.home)
            self.ui.nextButton.clicked.connect(parent.next_game)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = GameEndWidget("TB_BaconShop_HERO_49", 4)
    ex.show()
    sys.exit(app.exec_())
