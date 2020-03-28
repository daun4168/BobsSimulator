import sys
from PySide2.QtGui import QImage, QPixmap, QFont
from PySide2.QtWidgets import QWidget, QApplication

from BobsSimulator.UI.WaitingWidgetUI import Ui_LoadingWidget


class WaitingWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.ui = Ui_LoadingWidget()
        self.ui.setupUi(self)

        logo_img = QImage(r'res/img/logo.png')
        logo_pxm = QPixmap.fromImage(logo_img)
        logo_pxm = logo_pxm.scaled(self.ui.logoLabel.width(), self.ui.logoLabel.height())
        self.ui.logoLabel.setPixmap(logo_pxm)

        waiting_img_left = QImage(r'res/img/sylvanas.png')
        waiting_img_left_pxm = QPixmap.fromImage(waiting_img_left)
        waiting_img_left_pxm = waiting_img_left_pxm.scaled(self.ui.waitingImgLeft.width(), self.ui.waitingImgLeft.height())
        self.ui.waitingImgLeft.setPixmap(waiting_img_left_pxm)

        waiting_img_right = QImage(r'res/img/tyrande.png')
        waiting_img_right_pxm = QPixmap.fromImage(waiting_img_right)
        waiting_img_right_pxm = waiting_img_right_pxm.scaled(self.ui.waitingImgRight.width(), self.ui.waitingImgRight.height())
        self.ui.waitingImgRight.setPixmap(waiting_img_right_pxm)


class WaitingGameWidget(WaitingWidget):
    def __init__(self, parent):
        WaitingWidget.__init__(self, parent)

        self.ui.waitingTextTop.setText("Waiting For\nGame Starts...")
        font = QFont("Times", 50, QFont.Bold)
        self.ui.waitingTextTop.setFont(font)
        self.ui.waitingTextTop.setStyleSheet(f"QLabel {{ color: orange; }}")


class WaitingBattleWidget(WaitingWidget):
    def __init__(self, parent, battle_num=0):
        WaitingWidget.__init__(self, parent)

        self.ui.waitingTextTop.setText("Waiting For\nNext Battle...")
        font = QFont("Times", 50, QFont.Bold)
        self.ui.waitingTextTop.setFont(font)
        self.ui.waitingTextTop.setStyleSheet(f"QLabel {{ color: orange; }}")

        if battle_num > 0:
            self.ui.waitingTextBottom.setText(f"Previous Battle: {battle_num}")
            font = QFont("Times", 40, QFont.Bold)
            self.ui.waitingTextBottom.setFont(font)
            self.ui.waitingTextBottom.setStyleSheet(f"QLabel {{ color: orange; }}")


if __name__ == '__main__':
    app = QApplication()
    ex = WaitingWidget()
    ex.show()
    sys.exit(app.exec_())
