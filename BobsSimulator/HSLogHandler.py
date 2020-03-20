import os
import logging
import hearthstone.enums as hsenums
from PySide2.QtCore import Signal, QObject
from hearthstone.enums import GameTag, CardType, Faction, Race, Rarity, Zone, Step


from BobsSimulator.Util import card_name_by_id
from BobsSimulator.HSType import Game, Board, Hero, Card, ENTITY_TYPES
from BobsSimulator.Regex import *
from BobsSimulator.HSLogging import hsloghandler_logger
from BobsSimulator.Main import version_number
import hearthstone_data





class HSLogHandler(QObject):
    # Signals
    game_start = Signal()
    game_info = Signal()
    battle_start = Signal()
    end_game = Signal()
    end_file = Signal()

    def __init__(self, log_file):
        super().__init__()
        self.log_file = log_file

        self.init_game()

        self.contexts = []
        self.recent_parsing_line = None

    def init_game(self):
        self.game = Game()

        self.entities = {}  # entity id -> tag/value dict -> value
        self.entity_names = {}  # entity name -> entity id

        self.game_entity = None
        self.baconshop8playerenchant = None
        self.player_name = None
        self.enemy_name = None

    def read_line(self):
        return self.log_file.readline()

    def line_reader(self):
        line = self.read_line()
        while line:
            self.line_parser(line)
            line = self.read_line()

        self.end_file.emit()

    def line_parser(self, line):
        if GAME_STATE_DEBUG_PRINT_POWER_RE.match(line):
            self.entity_parser(GAME_STATE_DEBUG_PRINT_POWER_RE.match(line).group("context"))
        elif GAME_STATE_DEBUG_PRINT_POWER_LIST_RE.match(line):
            pass
        elif GAME_STATE_DEBUG_PRINT_GAME_RE.match(line):
            self.print_game_parser(GAME_STATE_DEBUG_PRINT_GAME_RE.match(line).group("context"))
        elif POWER_TASK_LIST_DEBUG_DUMP_RE.match(line):
            pass
        elif POWER_TASK_LIST_DEBUG_PRINT_POWER_RE.match(line):
            pass
        elif POWER_PROCESSOR_PREPARE_HISTORY_FOR_CURRENT_TASK_LIST_RE.match(line):
            pass
        elif POWER_PROCESSOR_END_CURRENT_TASK_LIST_RE.match(line):
            pass
        elif POWER_PROCESSOR_DO_TASK_LIST_FOR_CARD_TASK_LIST_RE.match(line):
            pass
        elif GAME_STATE_DEBUG_PRINT_OPTIONS_RE.match(line):
            pass
        elif GAME_STATE_SEND_OPTION_RE.match(line):
            pass
        elif GAME_STATE_DEBUG_PRINT_ENTITY_CHOICES_RE.match(line):
            pass
        elif GAME_STATE_DEBUG_PRINT_ENTITY_CHOSEN_RE.match(line):
            pass
        elif GAME_STATE_SEND_CHOICES_RE.match(line):
            pass
        elif TRIGGER_SPELL_CONTROLLER_RE.match(line):
            pass
        elif POWER_SPELL_CONTROLLER_RE.match(line):
            pass
        elif CHOICE_CARD_MGR_HIDE_RE.match(line):
            pass
        elif CHOICE_CARD_MGR_SHOW_RE.match(line):
            pass
        else:
            short_len = min(len(self.recent_parsing_line), len(line))

            new_line = None
            for i in range(1, short_len - 1):
                recent_line_ends = self.recent_parsing_line[len(self.recent_parsing_line) - i:]
                now_line_starts = line[:i]
                if recent_line_ends == now_line_starts:
                    new_line = self.recent_parsing_line + self.recent_parsing_line[i:]
                    break
            if new_line:
                hsloghandler_logger.warning(f"line_parser() warning - line break - Line: {line.rstrip()}, New Line: {new_line.rstrip()}")
                self.line_parser(new_line)
            else:
                hsloghandler_logger.error(f"line_parser() error - Line: {line}")
        self.recent_parsing_line = line.rstrip()

    def print_game_parser(self, context):

        if BUILD_NUMBER_RE.match(context):
            self.build_number = int(BUILD_NUMBER_RE.match(context).group("BuildNumber"))
            if self.build_number != version_number:
                hsloghandler_logger.warning(f"Build number NOT correct, Program: {version_number}, Log File: {self.build_number}")
        elif GAME_TYPE_RE.match(context):
            self.game_type = str(GAME_TYPE_RE.match(context).group("GameType"))
        elif FORMAT_TYPE_RE.match(context):
            self.format_type = str(FORMAT_TYPE_RE.match(context).group("FormatType"))
        elif SCENARIO_ID_RE.match(context):
            self.scenarioID = int(SCENARIO_ID_RE.match(context).group("ScenarioID"))
        elif PLAYER_ID_NAME_RE.match(context):
            player_id = int(PLAYER_ID_NAME_RE.match(context).group("PlayerID"))
            player_name = str(PLAYER_ID_NAME_RE.match(context).group("PlayerName"))
            is_found = False
            for entity_id, entity_tags in self.entities.items():
                if "PlayerID" in entity_tags and self.entities[entity_id]["PlayerID"] == player_id:
                    self.entity_names[player_name] = entity_id
                    is_found = True
                    break
            if not is_found:
                logging.error(f"print_game_parser() error - PLAYER_ID not found: {context}")
        else:
            logging.error(f"print_game_parser() error: {context}")
            raise NotImplementedError



if __name__ == '__main__':
    HS_LOG_FILE_DIR = 'Test/logs'
    log_file_2020_03_06_20_31_28 = open(os.path.join(HS_LOG_FILE_DIR, "2020-03-06 20-31-28.log"), 'r', encoding="UTF8")
    log_file_2020_02_29_21_06_42 = open(os.path.join(HS_LOG_FILE_DIR, "2020-02-29 21-06-42.log"), 'r', encoding="UTF8")
    log_file_2020_03_01_21_19_18 = open(os.path.join(HS_LOG_FILE_DIR, "2020-03-01 21-19-18.log"), 'r', encoding="UTF8")

    log_handler = HSLogHandler(log_file_2020_03_01_21_19_18)
    log_handler.line_reader()


