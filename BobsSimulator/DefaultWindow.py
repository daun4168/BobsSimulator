import sys
import os
from enum import IntEnum
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from BobsSimulator.Main import VERSION_NUMBER, LOCALE
from BobsSimulator.HomeWidget import HomeWidget
from BobsSimulator.LoadingWidget import LoadingWidget
from BobsSimulator.WaitingWidget import WaitingGameWidget, WaitingBattleWidget
from BobsSimulator.BattleInfoWidget import BattleInfoWidget
from BobsSimulator.ErrorWIdget import ErrorWidget
from BobsSimulator.FileEndWidget import FileEndWidget
from BobsSimulator.GameEndWidget import GameEndWidget
from BobsSimulator.HSType import Game
from BobsSimulator.HSLogging import main_logger, hsbattle_logger


from BobsSimulator.UI.DefaultWindowUI import Ui_DefaultWindow


class SimulateType(IntEnum):
    REAL = 1
    FILE = 2
    TEXT = 3


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

        # Some Variables
        self.hs_dir = "C:/Program Files (x86)/Hearthstone"
        self.log_file_name = os.path.join(self.hs_dir, 'Logs/Power.log')
        self.log_file_dir = os.path.join(self.hs_dir, 'Logs')
        self.dirwatcher = None
        self.filewatcher = None
        self.simulate_type = None  # SimulateType
        self.log_file = None  # file pointer
        self.log_handler = None  # HSLogHandler

        # background setting
        bg_image = QImage("res/img/background.jpg").scaled(self.window_size)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(bg_image))
        self.setPalette(palette)

        self.create_menus()

        self.show()

    def init(self):
        self.dirwatcher = None
        self.filewatcher = None
        self.simulate_type = None
        self.log_file = None
        self.log_handler = None

    def home(self):
        self.init()

        main_logger.info("Bob's Simulator Home.")
        homeWidget = HomeWidget(self)

        self.setCentralWidget(homeWidget)
        self.show()

    def log_file_changed(self):
        if not self.log_handler:
            self.log_file = open(self.log_file_name, 'r', encoding="UTF8")
            from BobsSimulator.HSLogHandler import HSLogHandler
            self.log_handler = HSLogHandler(self.log_file)

            self.log_handler.sig_game_start.connect(self.game_start_handler)
            self.log_handler.sig_game_info.connect(self.game_info_handler)
            self.log_handler.sig_battle_start.connect(self.battle_start_handler)
            self.log_handler.sig_battle_end.connect(self.battle_end_handler)
            self.log_handler.sig_end_game.connect(self.end_game_handler)
            self.log_handler.sig_end_file.connect(self.end_file_handler)

        print("log file changed!!!")
        self.log_handler.line_reader_start()

    def log_dir_changed(self):
        print('log_dir_changed')
        if not self.filewatcher:
            self.filewatcher = QFileSystemWatcher([self.log_file_name])
        if len(self.filewatcher.files()) == 0:
            self.filewatcher.fileChanged.connect(self.log_file_changed)

    def real_time_simulate(self):
        self.init()
        self.simulate_type = SimulateType.REAL
        main_logger.info("Real Time Simulate Starts.")
        errorWidget = ErrorWidget(self, "It's not implemented..")

        if not os.path.isfile(os.path.join(self.hs_dir, 'Hearthstone.exe')):
            QMessageBox.information(self, "ERROR", "Please Set Correct Hearthstone Directory First")
            self.set_hs_dir()

        if not os.path.isfile(os.path.join(self.hs_dir, 'Hearthstone.exe')):
            return

        self.log_file_name = os.path.join(self.hs_dir, 'Logs/Power.log')
        self.log_file_dir = os.path.join(self.hs_dir, 'Logs')

        self.loading()

        if not os.path.isdir(self.log_file_dir):
            os.mkdir(self.log_file_dir)

        waitingGameWidget = WaitingGameWidget(self)
        self.setCentralWidget(waitingGameWidget)
        self.show()

        self.dirwatcher = QFileSystemWatcher([self.log_file_dir])
        self.dirwatcher.directoryChanged.connect(self.log_dir_changed)

        if os.path.isfile(self.log_file_name):
            self.log_file_changed()

    def log_file_simulate(self):
        self.init()
        self.simulate_type = SimulateType.FILE
        main_logger.info("Log File Simulate Start")
        fname = QFileDialog.getOpenFileName(self, "Select log file", filter='Log file(*.log)')
        self.log_file_name = fname[0]
        if not self.log_file_name:
            self.home()
            return

        self.loading()

        self.log_file = open(self.log_file_name, 'r', encoding="UTF8")
        from BobsSimulator.HSLogHandler import HSLogHandler
        self.log_handler = HSLogHandler(self.log_file)

        self.log_handler.sig_game_start.connect(self.game_start_handler)
        self.log_handler.sig_game_info.connect(self.game_info_handler)
        self.log_handler.sig_battle_start.connect(self.battle_start_handler)
        self.log_handler.sig_battle_end.connect(self.battle_end_handler)
        self.log_handler.sig_end_game.connect(self.end_game_handler)
        self.log_handler.sig_end_file.connect(self.end_file_handler)

        self.log_handler.line_reader_start()

    def text_simulate(self):
        self.init()
        self.simulate_type = SimulateType.TEXT
        main_logger.info("Text File Simulate Starts.")
        errorWidget = ErrorWidget(self, "It's not implemented..")

        self.setCentralWidget(errorWidget)
        self.show()

    def set_hs_dir(self):
        while True:
            fname = QFileDialog.getExistingDirectory(self, "Set HearthStone Directory", self.hs_dir)

            if fname:
                if os.path.isfile(os.path.join(fname, 'Hearthstone.exe')):
                    self.hs_dir = fname
                    main_logger.info(f"Set HS Directory: {self.hs_dir}")
                    return True
                else:
                    QMessageBox.information(self, "ERROR", "Can't find Hearthstone.exe!!")
                    main_logger.info(f"Failed to Set HS Directory: {self.hs_dir}")
                    continue
            else:
                return False

    def about(self):
        QMessageBox.about(self, "About Bob's Simulator",
                          "<h2>Bob's Simulator 0.1</h2>"
                          "<p>Copyright &copy; 2020 Daun Jeong</p>"
                          "<p>github: <a href='https://github.com/daun4168/BobsSimulator'>https://github.com/daun4168/BobsSimulator</a></p>"
                          "<p>e-mail: <a href='mailto:daun4168@naver.com'>daun4168@naver.com</a></p>")

    def help(self):
        QMessageBox.information(self, "Help",
                                "<h2>Hello</h2>"
                                "<p>I will help you :)</p>")

    def license(self):
        QMessageBox.aboutQt(self)

    def loading(self):
        loadingWidget = LoadingWidget(self)
        self.setCentralWidget(loadingWidget)
        self.show()

        QtCore.QCoreApplication.processEvents()
        import BobsSimulator.Util

    def create_menus(self):
        # Mode MENU
        # Go To Home
        self.HomeAction = QAction("&Home", self)
        self.HomeAction.setStatusTip("Go back to home")
        self.HomeAction.triggered.connect(self.home)
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
        mode_menu.addAction(self.HomeAction)
        mode_menu.addAction(self.RealTimeSimulateAction)
        mode_menu.addAction(self.LogFileSimulateAction)
        mode_menu.addAction(self.TextSimulateAction)

        mode_menu = self.menuBar().addMenu("&Setting")
        mode_menu.addAction(self.SetHSDirAction)

        help_menu = self.menuBar().addMenu("&Help")
        help_menu.addAction(self.helpAction)
        help_menu.addAction(self.aboutAction)
        help_menu.addAction(self.licenseAction)

    def game_start_handler(self):
        hsbattle_logger.info(f"# {'='*50}")
        hsbattle_logger.info(f"# Game Start")

        if self.simulate_type == SimulateType.REAL:
            waitingWidget = WaitingBattleWidget(self)
            self.setCentralWidget(waitingWidget)
            self.show()
            QtCore.QCoreApplication.processEvents()
        self.log_handler.line_reader_start()

    def game_info_handler(self):
        hsbattle_logger.info(f"# Build: {self.log_handler.game.build_number}")
        hsbattle_logger.info(f"# Game Type: {self.log_handler.game.game_type}")
        hsbattle_logger.info(f"# Format Type: {self.log_handler.game.format_type}")
        hsbattle_logger.info(f"# Scenario ID: {self.log_handler.game.scenarioID}")
        hsbattle_logger.info(f"# Battle tag: {self.log_handler.game.player_battle_tag}")
        hsbattle_logger.info(f"# {'-'*50}")
        self.log_handler.line_reader_start()

    def battle_start_log_handler(self):
        from BobsSimulator.Util import card_name_by_id

        def hero_log_print(hero, start_text):
            hero_cardid = hero.card_id
            hero_name = card_name_by_id(hero_cardid, locale=LOCALE)
            hero_hp = hero.health - hero.damage
            hero_tech = hero.tech_level
            hsbattle_logger.info(f"""* {start_text} -name "{hero_name} @{hero_cardid}" -hp {hero_hp} -tech {hero_tech} """)

        def hero_power_log_print(hero_power, start_text):
            hero_power_cardid = hero_power.card_id
            hero_power_name = card_name_by_id(hero_power_cardid, locale=LOCALE)
            hero_power_log_text = f"""* {start_text} -name "{hero_power_name} @{hero_power_cardid}" """
            if hero_power.exhausted:
                hero_power_log_text += "-exhausted "
            hsbattle_logger.info(hero_power_log_text)

        def secret_log_print(secrets, start_text):
            for secret in secrets:
                secret_cardid = secret.card_id
                secret_name = card_name_by_id(secret_cardid, locale=LOCALE)
                hsbattle_logger.info(f"""* {start_text} -name "{secret_name} @{secret_cardid}" """)

        def minion_log_print(board, start_text):
            for minion in board:
                if not minion:
                    continue
                minion_cardid = minion.card_id
                minion_name = card_name_by_id(minion_cardid, locale=LOCALE)
                minion_hp = minion.health - minion.damage

                minion_text = f"""* {start_text} -name "{minion_name} @{minion_cardid}" -atk {minion.attack} -hp {minion_hp} -pos {minion.pos} """
                if minion.golden:
                    minion_text += "-golden "
                if minion.taunt:
                    minion_text += "-taunt "
                if minion.divine_shield:
                    minion_text += "-divine_shield "
                if minion.poisonous:
                    minion_text += "-poisonous "
                if minion.windfury:
                    minion_text += "-windfury "
                if minion.reborn:
                    minion_text += "-reborn "

                for enchant in minion.enchantments:
                    enchant_cardid = enchant.card_id
                    enchant_name = card_name_by_id(enchant_cardid, locale=LOCALE)
                    minion_text += f"""-enchant "{enchant_name} @{enchant_cardid}" """

                hsbattle_logger.info(minion_text)

        # PLAYER
        hsbattle_logger.info(f"# Battle {self.log_handler.game.battle_num} Start")
        hero_log_print(self.log_handler.game.battle.me.hero, "PlayerHero")
        hero_power_log_print(self.log_handler.game.battle.me.hero_power, "PlayerHeroPower")
        secret_log_print(self.log_handler.game.battle.me.secrets, "PlayerHeroSecret")
        minion_log_print(self.log_handler.game.battle.me.board, "PlayerMinion")

        # ENEMY
        hsbattle_logger.info(f"# versus")
        hero_log_print(self.log_handler.game.battle.enemy.hero, "EnemyHero")
        hero_power_log_print(self.log_handler.game.battle.enemy.hero_power, "EnemyHeroPower")
        secret_log_print(self.log_handler.game.battle.enemy.secrets, "EnemyHeroSecret")
        minion_log_print(self.log_handler.game.battle.enemy.board, "EnemyMinion")

    def battle_start_handler(self):
        self.battle_start_log_handler()

        battle_info_widget = BattleInfoWidget(self.log_handler.game.battle, self)
        self.setCentralWidget(battle_info_widget)
        self.show()
        QtCore.QCoreApplication.processEvents()

    def battle_end_log_handler(self):
        hsbattle_logger.info(f"# Battle {self.log_handler.game.battle_num} End")
        player_hp = self.log_handler.game.battle.me.hero.health - self.log_handler.game.battle.me.hero.damage
        enemy_hp = self.log_handler.game.battle.enemy.hero.health - self.log_handler.game.battle.enemy.hero.damage

        if self.log_handler.game.battle.me.hero.taken_damage == 0 and self.log_handler.game.battle.enemy.hero.taken_damage == 0:
            hsbattle_logger.info(f"# DRAW")
        elif self.log_handler.game.battle.me.hero.taken_damage == 0:
            hsbattle_logger.info(f"# Player Win")
            hsbattle_logger.info(f"# Player Give Damage: {self.log_handler.game.battle.enemy.hero.taken_damage}")
        else:
            hsbattle_logger.info(f"# Enemy Win")
            hsbattle_logger.info(f"# Player Take Damage: {self.log_handler.game.battle.me.hero.taken_damage}")

        hsbattle_logger.info(f"# PlayerHP: {player_hp}, EnemyHP: {enemy_hp}")
        hsbattle_logger.info(f"# PlayerRank: {self.log_handler.game.leaderboard_place}")

        hsbattle_logger.info(f"# {'-'*50}")

    def battle_end_handler(self):
        self.battle_end_log_handler()

        if self.simulate_type == SimulateType.REAL:
            battle_num = self.log_handler.game.battle_num
            waitingWidget = WaitingBattleWidget(self, battle_num)
            self.setCentralWidget(waitingWidget)
            self.show()
            QtCore.QCoreApplication.processEvents()

        self.log_handler.line_reader_start()

    def end_game_handler(self):
        hsbattle_logger.info(f"# Game End")
        hsbattle_logger.info(f"# Player Rank: {self.log_handler.game.leaderboard_place}")
        hsbattle_logger.info(f"# {'='*50}")


        hero_cardid = self.log_handler.game.battle.me.hero.card_id
        rank_num = self.log_handler.game.leaderboard_place
        gameEndWidget = GameEndWidget(hero_cardid, rank_num, self)
        self.setCentralWidget(gameEndWidget)
        self.show()

        QtCore.QCoreApplication.processEvents()

    def end_file_handler(self):
        if self.simulate_type == SimulateType.FILE:
            main_logger.info("Log File Simulate End")
            fileEndWidget = FileEndWidget(self)
            self.setCentralWidget(fileEndWidget)
            self.show()
            return

        self.log_handler.line_reader_start()

    def simulate(self):
        from BobsSimulator.Simulator import Simulator
        simulator = Simulator()
        result = simulator.simulate(self.log_handler.game.battle)

        simulate_num = len(result)
        if not simulate_num:
            return
        win_num = sum(x > 0 for x in result)
        lose_num = sum(x < 0 for x in result)
        draw_num = sum(x == 0 for x in result)
        average_damage = sum(result) / simulate_num

        print("------simulation result-------")
        print(f'Simulate Number: {simulate_num}')
        print(result)
        print(f'Win Number: {win_num}, ratio: {win_num/simulate_num * 100}%')
        print(f'Lose Number: {lose_num}, ratio: {lose_num/simulate_num * 100}%')
        print(f'Draw Number: {draw_num}, ratio: {draw_num/simulate_num * 100}%')
        print(f'Average Damage: {average_damage}')



    def next_battle(self):
        if self.simulate_type == SimulateType.REAL:
            waitingWidget = WaitingGameWidget(self)
            self.setCentralWidget(waitingWidget)
            self.show()
            QtCore.QCoreApplication.processEvents()

        self.log_handler.line_reader_start()


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        ex = DefaultWindow()
        sys.exit(app.exec_())

    except Exception as e:
        print(f"Exception!: {e}")
