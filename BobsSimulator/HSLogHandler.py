import os
import logging
import hearthstone.enums as hsenums
from PySide2.QtCore import Signal, QObject
from hearthstone.enums import GameTag, CardType, Faction, Race, Rarity, Zone, Step


from BobsSimulator.Util import card_name_by_id
from BobsSimulator.HSType import Game, Board, Hero, Card, ENTITY_TYPES
from BobsSimulator.Regex import *


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


