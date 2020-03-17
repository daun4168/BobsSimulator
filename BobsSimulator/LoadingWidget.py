import sys
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from BobsSimulator.UI.LoadingWidgetUI import Ui_LoadingWidget


PROGRESS_STYLE = """
QProgressBar{
    border: 2px solid grey;
    border-radius: 5px;
    text-align: center;
    background-color: grey;

}

QProgressBar::chunk{
    background: qlineargradient(x1: 0,
                                y1: 0.5,
                                x2: 1,
                                y2: 0.5,
                                stop: 0 orange,
                                stop: 1 yellow);
    margin-right: 2px;
}

"""




class LoadingWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.ui = Ui_LoadingWidget()
        self.ui.setupUi(self)

        logo_img = QImage(r'res/img/logo.png')
        logo_pxm = QPixmap.fromImage(logo_img)
        logo_pxm = logo_pxm.scaled(self.ui.logoLabel.width(), self.ui.logoLabel.height())
        self.ui.logoLabel.setPixmap(logo_pxm)

        loading_text_img = QImage(r'res/img/loading_img.png')
        loading_text_pxm = QPixmap.fromImage(loading_text_img)
        loading_text_pxm = loading_text_pxm.scaled(self.ui.loadingTextLabel.width(), self.ui.loadingTextLabel.height())

        self.ui.loadingTextLabel.setPixmap(loading_text_pxm)

        self.ui.progressBar.setStyleSheet(PROGRESS_STYLE)
        self.ui.progressBar.setValue(0)

    def set_progress(self, value):
        self.ui.progressBar.setValue(value)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LoadingWidget()
    ex.show()
    sys.exit(app.exec_())

