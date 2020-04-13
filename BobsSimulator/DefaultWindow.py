import sys
import os
from enum import IntEnum
from typing import Optional
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from BobsSimulator.Config import VERSION_NUMBER, LOCALE, HS_DIR, set_hs_dir_config
from BobsSimulator.HomeWidget import HomeWidget
from BobsSimulator.LoadingWidget import LoadingWidget
from BobsSimulator.WaitingWidget import WaitingGameWidget, WaitingBattleWidget
from BobsSimulator.BattleInfoWidget import BattleInfoWidget
from BobsSimulator.ErrorWidget import ErrorWidget
from BobsSimulator.FileEndWidget import FileEndWidget
from BobsSimulator.GameEndWidget import GameEndWidget
from BobsSimulator.ResultWidget import ResultWidget
from BobsSimulator.HSType import Game
from BobsSimulator.HSLogging import main_logger, hsbattle_logger, simulator_logger
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
        self.hs_dir = HS_DIR
        self.log_file_name = os.path.join(self.hs_dir, 'Logs/Power.log')
        self.log_file_dir = os.path.join(self.hs_dir, 'Logs')
        self.dirwatcher = None
        self.filewatcher = None
        self.simulate_type = None  # SimulateType
        self.log_file = None  # file pointer
        self.before_log_file_tell = 0  # file byte
        self.log_handler = None  # type: Optional["HSLogHandler"]

        self.ignore_battle_handler = False
        self.real_time_simulate_starting = False
        self.is_waiting_next_battle = False

        self.simulator = None

        # background setting
        bg_image = QImage("res/img/background.jpg").scaled(self.window_size)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(bg_image))
        self.setPalette(palette)

        self.loading_widget = None  # type: Optional[LoadingWidget]

        self.create_menus()

        self.show()

    def init(self):
        self.dirwatcher = None
        self.filewatcher = None
        self.simulate_type = None
        self.log_file = None
        self.log_handler = None
        self.simulator = None

        self.ignore_battle_handler = False
        self.real_time_simulate_starting = False
        self.is_waiting_next_battle = False
        self.before_log_file_tell = 0

    def home(self):
        self.init()
        self.setWindowTitle(f'Bobs Simulator')

        main_logger.info("Bob's Simulator Home.")
        homeWidget = HomeWidget(self)

        self.setCentralWidget(homeWidget)
        self.show()

    def log_file_changed(self):
        from BobsSimulator.HSLogHandler import HSLogHandler

        if not self.log_handler:
            self.log_file = open(self.log_file_name, 'r', encoding="UTF8")

            self.log_handler = HSLogHandler(self.log_file)

            self.log_handler.sig_game_start.connect(self.game_start_handler)
            self.log_handler.sig_game_info.connect(self.game_info_handler)
            self.log_handler.sig_battle_start.connect(self.battle_start_handler)
            self.log_handler.sig_battle_end.connect(self.battle_end_handler)
            self.log_handler.sig_end_game.connect(self.end_game_handler)
            self.log_handler.sig_end_file.connect(self.end_file_handler)
        else:
            print("log file changed!!!")
            if self.log_file is None or self.log_file.closed:
                self.log_file = open(self.log_file_name, 'r', encoding="UTF8")

                self.log_file.seek(0, os.SEEK_END)
                log_file_size = self.log_file.tell()

                if self.before_log_file_tell < log_file_size:
                    self.log_file.seek(self.before_log_file_tell)
                else:
                    self.log_file.seek(0)

                self.log_handler.log_file = self.log_file

        self.log_handler.line_reader_start()

    def log_dir_changed(self):
        print('log_dir_changed')
        if not self.filewatcher:
            print('new filewatcher!')
            self.filewatcher = QFileSystemWatcher()
            self.filewatcher.addPath(self.log_file_name)
            self.filewatcher.fileChanged.connect(self.log_file_changed)
        print("len filewatcher", len(self.filewatcher.files()))
        if len(self.filewatcher.files()) == 0:
            print("ADD PATH")
            self.filewatcher.addPath(self.log_file_name)
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

        self.real_time_simulate_starting = True
        self.ignore_battle_handler = True

        self.dirwatcher = QFileSystemWatcher([self.log_file_dir])
        self.dirwatcher.directoryChanged.connect(self.log_dir_changed)

        self.log_dir_changed()

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
        self.setWindowTitle(f'Bobs Simulator    Log File Simulate: {os.path.basename(self.log_file_name)}')

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
                    set_hs_dir_config(fname)
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
        self.loading_widget = LoadingWidget(self)
        self.setCentralWidget(self.loading_widget)
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
        print("game_start_handler")
        if self.ignore_battle_handler:
            self.log_handler.line_reader_start()
            return

        hsbattle_logger.info(f"# {'='*50}")
        hsbattle_logger.info(f"# Game Start")

        if self.simulate_type == SimulateType.REAL:
            waitingWidget = WaitingBattleWidget(self)
            self.setCentralWidget(waitingWidget)
            self.show()
            QtCore.QCoreApplication.processEvents()
        self.log_handler.line_reader_start()

    def game_info_handler(self):
        print("game_info_handler")
        if self.ignore_battle_handler:
            self.log_handler.line_reader_start()
            return

        hsbattle_logger.info(f"# Build: {self.log_handler.game.build_number}")
        hsbattle_logger.info(f"# Game Type: {self.log_handler.game.game_type}")
        hsbattle_logger.info(f"# Format Type: {self.log_handler.game.format_type}")
        hsbattle_logger.info(f"# Scenario ID: {self.log_handler.game.scenarioID}")
        hsbattle_logger.info(f"# Battle tag: {self.log_handler.game.player_battle_tag}")
        hsbattle_logger.info(f"# {'-'*50}")

        if self.log_handler.game.game_type != "GT_BATTLEGROUNDS":
            self.ignore_battle_handler = True

        self.log_handler.line_reader_start()

    def battle_start_log_handler(self):
        hsbattle_logger.info(f"# Battle {self.log_handler.game.battle_num}")
        self.log_handler.game.battle.print_log(hsbattle_logger)

    def battle_start_handler(self):
        print("battle_start_handler")
        if self.ignore_battle_handler:
            self.log_handler.line_reader_start()
            return

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
        print("battle_end_handler")
        if self.ignore_battle_handler:
            self.log_handler.line_reader_start()
            return

        self.battle_end_log_handler()

        if self.simulate_type == SimulateType.REAL:
            battle_num = self.log_handler.game.battle_num
            waitingWidget = WaitingBattleWidget(self, battle_num)
            self.setCentralWidget(waitingWidget)
            self.show()
            QtCore.QCoreApplication.processEvents()

        self.log_handler.line_reader_start()

    def end_game_handler(self):
        print("end_game_handler")
        if self.simulate_type == SimulateType.REAL and self.real_time_simulate_starting:
            self.next_battle()
            return

        if self.ignore_battle_handler:
            self.ignore_battle_handler = False
            self.next_battle()
            return

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
        print("End Of File")
        if self.simulate_type == SimulateType.FILE:
            main_logger.info("Log File Simulate End")
            fileEndWidget = FileEndWidget(self)
            self.setCentralWidget(fileEndWidget)
            self.show()
            return

        if self.simulate_type == SimulateType.REAL and self.real_time_simulate_starting:
            self.ignore_battle_handler = False
            self.real_time_simulate_starting = False

            if not self.log_handler.is_game_end:
                self.battle_start_handler()

        self.before_log_file_tell = self.log_file.tell()
        self.log_file.close()

        # self.log_handler.line_reader_start()

    def process_npercent_handler(self):
        self.loading_widget.set_progress(self.simulator.simulation_ratio * 100)
        QtCore.QCoreApplication.processEvents()

    def simulate(self):
        from BobsSimulator.HSSimulator import Simulator
        self.simulator = Simulator()

        self.simulator.sig_process_npercent.connect(self.process_npercent_handler)

        self.loading_widget = LoadingWidget(parent=self)
        self.setCentralWidget(self.loading_widget)
        self.show()

        QtCore.QCoreApplication.processEvents()

        best_score_battle, best_simulation_result, my_simulation_result = self.simulator.find_best_arrangement(self.log_handler.game.battle)

        simulator_logger.info("<Your Arrangement Simulation>")
        self.simulator.simulate(self.log_handler.game.battle, simulate_num=1, print_info=simulator_logger.info)
        simulator_logger.info("<Best Arrangement Simulation>")
        self.simulator.simulate(best_score_battle, simulate_num=1, print_info=simulator_logger.info)

        result_widget = ResultWidget(self.log_handler.game.battle, my_simulation_result, best_score_battle, best_simulation_result, parent=self)
        self.setCentralWidget(result_widget)
        self.show()

    def next_battle(self):
        if self.simulate_type == SimulateType.REAL:
            waitingWidget = WaitingGameWidget(self)
            self.setCentralWidget(waitingWidget)
            self.show()
            QtCore.QCoreApplication.processEvents()

        self.log_handler.line_reader_start()


if __name__ == '__main__':
    try:
        app = QApplication()
        ex = DefaultWindow()
        sys.exit(app.exec_())

    except Exception as e:
        print(f"Exception!: {e}")
