import sys
from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QFontDatabase, QFont
import BobsSimulator.Config


class Font:
    @classmethod
    def init_font(cls):
        QFontDatabase.addApplicationFont('res/font/BelweMediumBT.ttf')
        QFontDatabase.addApplicationFont('res/font/BelweBdBTBold.ttf')
        QFontDatabase.addApplicationFont('res/font/Franklin_Gothic_Book_Regular.ttf')
        QFontDatabase.addApplicationFont('res/font/LHF_Uncial_Caps.ttf')
        QFontDatabase.addApplicationFont('res/font/BMJUA_ttf.ttf')
        QFontDatabase.addApplicationFont('res/font/Showlove-Regular.ttf')
        QFontDatabase.addApplicationFont('res/font/Show-Regular.ttf')
        QFontDatabase.addApplicationFont('res/font/Dr.Ziemboz.ttf')
        QFontDatabase.addApplicationFont('res/font/HambuRadul-Regular.ttf')




if __name__ == '__main__':
    from BobsSimulator.HomeWindow import HomeWindow
    from BobsSimulator.HSLogging import main_logger

    app = QApplication(sys.argv)
    Font.init_font()

    ex = HomeWindow()
    sys.exit(app.exec_())
