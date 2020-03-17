import sys
from PySide2.QtGui import *
from PySide2.QtWidgets import *

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




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WaitingWidget()
    ex.show()
    sys.exit(app.exec_())

