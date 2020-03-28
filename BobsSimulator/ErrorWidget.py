import sys
from PySide2.QtGui import QImage, QPixmap, QFont
from PySide2.QtWidgets import QWidget, QApplication

from BobsSimulator.UI.ErrorWidgetUI import Ui_ErrorWidget


class ErrorWidget(QWidget):
    def __init__(self, parent=None, error_msg=None):
        QWidget.__init__(self, parent)

        self.ui = Ui_ErrorWidget()
        self.ui.setupUi(self)

        logo_img = QImage(r'res/img/logo.png')
        logo_pxm = QPixmap.fromImage(logo_img)
        logo_pxm = logo_pxm.scaled(self.ui.logoLabel.width(), self.ui.logoLabel.height())
        self.ui.logoLabel.setPixmap(logo_pxm)

        error_img = QImage(r'res/img/crying_murloc.png')
        error_img_pxm = QPixmap.fromImage(error_img)
        error_img_pxm = error_img_pxm.scaled(self.ui.errorImg.width(), self.ui.errorImg.height())
        self.ui.errorImg.setPixmap(error_img_pxm)

        self.ui.oopsText.setText("Oops!!!")
        font = QFont("Times", 60, QFont.Bold)
        self.ui.oopsText.setFont(font)
        self.ui.oopsText.setStyleSheet(f"QLabel {{ color: white; }}")


        if error_msg is None:
            error_msg = "Maybe file is broken."

        self.ui.errorText.setText(f"Something went wrong. {error_msg}")
        font = QFont("Times", 30)
        self.ui.errorText.setFont(font)
        self.ui.errorText.setStyleSheet(f"QLabel {{ color: white; }}")
        self.ui.errorText.setWordWrap(True)

        self.ui.homeButton.clicked.connect(parent.home)


if __name__ == '__main__':
    app = QApplication()
    ex = ErrorWidget()
    ex.show()
    sys.exit(app.exec_())
