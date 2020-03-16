import sys
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from BobsSimulator.DefaultWindow import DefaultWindow
from BobsSimulator.UI.HomeWidgetUI import Ui_HomeWidget


class HomeWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.ui = Ui_HomeWidget()
        self.ui.setupUi(self)

        logo_img = QImage(r'res/img/logo.png')
        log_pxm = QPixmap.fromImage(logo_img)
        log_pxm = log_pxm.scaled(self.ui.logoLabel.width(), self.ui.logoLabel.height())
        self.ui.logoLabel.setPixmap(log_pxm)


class HomeWindow(DefaultWindow):
    def __init__(self, parent=None):
        # Load from UI
        DefaultWindow.__init__(self, parent)

        self.homeWidget = HomeWidget()

        self.setCentralWidget(self.homeWidget)
        self.show()
    pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HomeWindow()
    sys.exit(app.exec_())


