import sys
from PySide2.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QGridLayout,
                               QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox)
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt, Signal

class Logon(QWidget):
    ok = Signal()

    def __init__(self,ids,pws,parent=None):
        QWidget.__init__(self,parent)

        self.listIds = ids
        self.listPWs = pws

        self.labelId = QLabel('&Id :')
        self.labelId.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.labelPW = QLabel('&Password:')

        self.lineEditId = QLineEdit()
        self.lineEditPW = QLineEdit()
        self.lineEditPW.setEchoMode(QLineEdit.Password)

        self.labelId.setBuddy(self.lineEditId)
        self.labelPW.setBuddy(self.lineEditPW)

        self.buttonOk = QPushButton("&Ok")
        self.buttonOk.setIcon(QIcon(":/images/ok.png"))

        layout1 = QGridLayout()
        layout1.addWidget(self.labelId,0,0)
        layout1.addWidget(self.lineEditId,0,1);
        layout1.addWidget(self.labelPW,1,0)
        layout1.addWidget(self.lineEditPW,1,1)

        layout2 = QHBoxLayout()
        layout2.addStretch()
        layout2.addWidget(self.buttonOk)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(layout1)
        mainLayout.addLayout(layout2)

        self.setLayout(mainLayout)
        self.setWindowTitle('Log on')
        self.setWindowIcon(QIcon(":/images/ok.png"))

        self.buttonOk.clicked.connect(self.onOk)

    def onOk(self):
        if self.lineEditId.text() not in self.listIds:
            QMessageBox.critical(self,"Logon error","Unregistered user")
            self.lineEditId.setFocus()
        else:
            idx = self.listIds.index(self.lineEditId.text())
            if self.lineEditPW.text() != self.listPWs[idx] :
                QMessageBox.critical(self,"Logon error","Incroreect password")
                self.lineEditPW.setFocus()
            else:
                self.ok.emit()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    ids = ['James','John','Jane']
    pws = ['123','456','789']

    logon = Logon(ids,pws)

    logon.ok.connect(app.exit)

    logon.show()
    app.exec_()