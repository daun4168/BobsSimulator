import sys
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from BobsSimulator.DefaultWindow import DefaultWindow


class HomeWindow(DefaultWindow):
    def __init__(self, parent=None):
        # Load from UI
        DefaultWindow.__init__(self, parent)

        self.home()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HomeWindow()
    sys.exit(app.exec_())


