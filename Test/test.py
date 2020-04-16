from PySide2.QtCore import QFileSystemWatcher
import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from time import time
import datetime




class FileWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        log_file_name = r"C:\Program Files (x86)\Hearthstone\Logs\Power.log"

        self.filewatcher = QFileSystemWatcher()
        is_add = self.filewatcher.addPath(log_file_name)
        print("ADD: ", is_add)
        self.filewatcher.fileChanged.connect(self.log_file_changed)

        self.show()

    def log_file_changed(self):
        print(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} log_file_changed")



if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = FileWindow()
    sys.exit(app.exec_())
