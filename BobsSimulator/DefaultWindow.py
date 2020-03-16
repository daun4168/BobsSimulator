import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt, QSize, QRect, QPoint
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from BobsSimulator.UI.DefaultWindowUI import Ui_DefaultWindow


class DefaultWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        # Load from UI
        self.ui = Ui_DefaultWindow()
        self.ui.setupUi(self)

        # Default setting
        self.setWindowTitle('Bobs Simulator')
        self.setWindowIcon(QIcon('res/img/icon_bob.png'))
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.window_size = QSize(self.width(), self.height())
        self.setFixedSize(self.window_size)
        self.statusBar().setSizeGripEnabled(False)

        # background setting
        bg_image = QImage("res/img/background.jpg").scaled(self.window_size)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(bg_image))
        self.setPalette(palette)

        self.createMenus()

        self.show()

    def real_time_simulate(self):
        pass

    def log_file_simulate(self):
        pass

    def text_simulate(self):
        pass

    def set_hs_dir(self):
        pass

    def about(self):
        QMessageBox.about(self, "About Bob's Simulator",
                          "<h2>Bob's Simulator 0.1</h2>"
                          "<p>Copyright &copy; 2020 Daun Jeong</p>"
                          "<p>github: <a href='https://github.com/daun4168/BobsSimulator'>https://github.com/daun4168/BobsSimulator</a></p></p>"
                          "<p>e-mail: <a href='mailto:daun4168@naver.com'>daun4168@naver.com</a></p>")

    def help(self):
        QMessageBox.about(self, "HELP! Shape",
                          "<h2>Shape 1.0</h2>"
                          "<p>Copyright &copy; 2014 Q5Programming Inc."
                          "<p>Shape is a small application that "
                          "demonstrates QAction, QMainWindow, QMenuBar, "
                          "QStatusBar, QToolBar, and many other "
                          "Qt classes.")

    def license(self):
        QMessageBox.aboutQt(self)

    def createMenus(self):
        # Mode MENU
        # Go To Home
        # Real time simulate action
        self.RealTimeSimulateAction = QAction("&Real Time", self)
        self.RealTimeSimulateAction.setStatusTip("Real Time Simulate")
        self.RealTimeSimulateAction.triggered.connect(self.real_time_simulate)

        # Log File simulate action
        self.LogFileSimulateAction = QAction("&Log File", self)
        self.LogFileSimulateAction.setStatusTip("Simulate with log file")
        self.LogFileSimulateAction.triggered.connect(self.log_file_simulate)

        # Text simulate action
        self.TextSimulateAction = QAction("&Text", self)
        self.TextSimulateAction.setStatusTip("Simulate with Text")
        self.TextSimulateAction.triggered.connect(self.text_simulate)

        # Setting MENU
        # Set Hearthstone Directory action
        self.SetHSDirAction = QAction("&Set HS Directory", self)
        self.SetHSDirAction.setStatusTip("Set Hearthstone Directory")
        self.SetHSDirAction.triggered.connect(self.set_hs_dir)

        # Help MENU
        # help action
        self.helpAction = QAction("&Help", self)
        self.helpAction.setStatusTip("Show the application's Help box")
        self.helpAction.triggered.connect(self.help)

        # about action
        self.aboutAction = QAction("&About", self)
        self.aboutAction.setStatusTip("Show the application's About box")
        self.aboutAction.triggered.connect(self.about)

        # about license
        self.licenseAction = QAction("&License", self)
        self.licenseAction.setStatusTip("Show the application's License box")
        self.licenseAction.triggered.connect(self.license)

        mode_menu = self.menuBar().addMenu("&Mode")
        mode_menu.addAction(self.RealTimeSimulateAction)
        mode_menu.addAction(self.LogFileSimulateAction)
        mode_menu.addAction(self.TextSimulateAction)

        mode_menu = self.menuBar().addMenu("&Setting")
        mode_menu.addAction(self.SetHSDirAction)

        help_menu = self.menuBar().addMenu("&Help")
        help_menu.addAction(self.helpAction)
        help_menu.addAction(self.aboutAction)
        help_menu.addAction(self.licenseAction)




if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        ex = DefaultWindow()
        sys.exit(app.exec_())

    except Exception as e:
        print(f"Exception!: {e}")
