import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt, QSize, QRect, QPoint
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from BobsSimulator.UI.DefaultWindowUI import Ui_DefaultWindow


class DefaultWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.ui = Ui_DefaultWindow()
        self.ui.setupUi(self)

        self.setWindowTitle('Bobs Simulator')
        self.setWindowIcon(QIcon('res/img/icon_bob.png'))
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.window_size = QSize(self.width(), self.height())
        self.setFixedSize(self.window_size)

        bg_image = QImage("res/img/background.jpg").scaled(self.window_size)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(bg_image))
        self.setPalette(palette)


        self.statusBar().setSizeGripEnabled(False)
        # about
        self.aboutAction = QAction("&About",self)
        self.aboutAction.setStatusTip("Show the application's About box")
        self.aboutAction.triggered.connect(self.about)

        self.createMenus()

        self.show()

    @staticmethod
    def new_file():
        print("NEW_FILE")

    def createMenus(self):
        aboutMenu = self.menuBar().addMenu("&About")
        aboutMenu.addAction(self.aboutAction)

    def about(self):
        QMessageBox.about(self, "About Shape",
                          "<h2>Shape 1.0</h2>"
                          "<p>Copyright &copy; 2014 Q5Programming Inc."
                          "<p>Shape is a small application that "
                          "demonstrates QAction, QMainWindow, QMenuBar, "
                          "QStatusBar, QToolBar, and many other "
                          "Qt classes.")


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        ex = DefaultWindow()
        sys.exit(app.exec_())

    except Exception as e:
        print(f"Exception!: {e}")
