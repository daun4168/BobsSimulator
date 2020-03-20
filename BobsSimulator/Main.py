import sys
from PySide2.QtWidgets import QApplication


version_number = 43246

if __name__ == '__main__':
    from BobsSimulator.HomeWindow import HomeWindow
    from BobsSimulator.HSLogging import main_logger

    app = QApplication(sys.argv)
    ex = HomeWindow()
    sys.exit(app.exec_())
