import sys
from PySide2.QtWidgets import *

from BobsSimulator.HomeWindow import HomeWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HomeWindow()
    sys.exit(app.exec_())
