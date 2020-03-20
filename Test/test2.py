import sys
from PySide2.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QGridLayout,
                               QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox)
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt, Signal

import hearthstone_data
carddefs_path = hearthstone_data.get_carddefs_path()

print(int(float(hearthstone_data.__version__)))
