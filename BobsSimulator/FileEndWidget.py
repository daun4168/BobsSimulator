import sys
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from BobsSimulator.UI.FileEndWidgetUI import Ui_fileEndWidget


class FileEndWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.ui = Ui_fileEndWidget()
        self.ui.setupUi(self)

        logo_img = QImage(r'res/img/logo.png')
        logo_pxm = QPixmap.fromImage(logo_img)
        logo_pxm = logo_pxm.scaled(self.ui.logoLabel.width(), self.ui.logoLabel.height())
        self.ui.logoLabel.setPixmap(logo_pxm)

        end_img = QImage(r'res/img/chen.png')
        end_img_pxm = QPixmap.fromImage(end_img)
        end_img_pxm = end_img_pxm.scaled(self.ui.endImg.width(), self.ui.endImg.height())
        self.ui.endImg.setPixmap(end_img_pxm)

        self.ui.endText1.setText("File End!")
        font = QFont("Times", 55, QFont.Bold)
        self.ui.endText1.setFont(font)
        self.ui.endText1.setStyleSheet(f"QLabel {{ color: white; }}")

        if parent:
            self.ui.homeButton.clicked.connect(parent.home)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileEndWidget()
    ex.show()
    sys.exit(app.exec_())
