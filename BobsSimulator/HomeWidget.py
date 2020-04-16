import sys
from PySide2.QtGui import QImage, QPixmap, QFont
from PySide2.QtWidgets import QWidget, QApplication

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

        self.ui.realtimeButton.setFont(QFont("배달의민족 주아", 40, QFont.Bold))
        self.ui.logfileButton.setFont(QFont("배달의민족 주아", 40, QFont.Bold))
        self.ui.textButton.setFont(QFont("배달의민족 주아", 40, QFont.Bold))

        self.ui.realtimeButton.clicked.connect(parent.real_time_simulate)
        self.ui.logfileButton.clicked.connect(parent.log_file_simulate)
        self.ui.textButton.clicked.connect(parent.text_simulate)


if __name__ == '__main__':
    app = QApplication()
    ex = HomeWidget()
    ex.show()
    sys.exit(app.exec_())

