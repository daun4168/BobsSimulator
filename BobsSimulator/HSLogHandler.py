import os
from typing import Dict, Optional
from PySide2.QtCore import QObject, Signal

from BobsSimulator.HSLogging import hsloghandler_logger
from BobsSimulator.HSType import Battle, CardType, Enchantment, Faction, Game, \
    GameTag, Minion, PowerType, Race, Secret, State, Zone, Hero, HeroPower, \
    DEATHRATTLE_ENCHANT_CARD_IDS
from BobsSimulator.Config import LOCALE, VERSION_NUMBER
from BobsSimulator.Regex import *
from BobsSimulator.Util import Util


class HSLogHandler(QObject):
    # Signals
    sig_game_start = Signal()
    sig_game_info = Signal()
    sig_battle_start = Signal()
    sig_battle_end = Signal()
    sig_end_game = Signal()
    sig_end_file = Signal()

    # initialize in init_game()
    game: Game
    entities: Dict[int, Dict[int, int]]  # entity id -> tag/value dict
    card_ids: Dict[int, str]
    entity_names: Dict[str, int]  # entity name -> entity id
    is_hero_contain: Dict[int, bool]

    game_entity: Optional[int]
    baconshop8playerenchant: Optional[int]
    me_entity_id: Optional[int]
    me_player_id: Optional[int]
    enemy_entity_id: Optional[int]
    enemy_player_id: Optional[int]

    def __init__(self, log_file_name: str, is_print_console=False):
        super().__init__()
        self.log_file_name = log_file_name
        self.log_file = open(log_file_name, 'r', encoding="UTF8")
        self.before_log_file_tell = 0  # file byte
        self.is_print_console = is_print_console

        hsloghandler_logger.info(f"HSLogHandler Start: {log_file_name}")

        self.init_game()

        self.contexts = []
        self.recent_parsing_line = None
        self.do_line_reader = False
        self.is_line_reader = False
        self.is_game_end = False

    def init_game(self):
        self.game = Game()
        self.entities = {}
        self.card_ids = {}
        self.entity_names = {}
        self.is_hero_contain = {}

        self.game_entity = None
        self.baconshop8playerenchant = None
        self.me_entity_id = None
        self.me_player_id = None
        self.enemy_entity_id = None
        self.enemy_player_id = None

        self.is_game_end = False

    def read_line(self):
        return self.log_file.readline()

    def line_reader_start(self):
        self.do_line_reader = True

        if self.log_file is None or self.log_file.closed:
            self.log_file = open(self.log_file_name, 'r', encoding="UTF8")

            self.log_file.seek(0, os.SEEK_END)
            log_file_size = self.log_file.tell()

            if self.before_log_file_tell <= log_file_size:
                self.log_file.seek(self.before_log_file_tell)
            else:
                self.log_file.seek(0)

            self.log_file = self.log_file

        if self.is_line_reader:
            return
        else:
            self.line_reader()

    def line_reader(self):
        self.is_line_reader = True
        while True:
            if not self.do_line_reader:
                self.is_line_reader = False
                return
            line = self.read_line()
            if not line:
                break
            self.line_parser(line)
        self.end_file()
        self.is_line_reader = False

    def get_entity_id_by_entity(self, entity):
        entity_id: int
        if ENTITY_DESCRIPTION_RE.match(entity):
            entity_id = int(ENTITY_DESCRIPTION_RE.match(entity).group("id"))
        elif entity.isdigit():
            entity_id = int(entity)
        elif entity in self.entity_names:
            entity_id = self.entity_names[entity]
        else:
            entity_id = self.enemy_entity_id
            self.entity_names[entity] = self.enemy_entity_id
        return entity_id

    def get_default_values(self, entity_id):
        cardtype = ""
        zone = ""

        card_id = self.card_ids.get(entity_id, "")
        card_name = Util.card_name_by_id(card_id)

        if GameTag.CARDTYPE.value in self.entities[entity_id]:
            cardtype = self.entities[entity_id][GameTag.CARDTYPE.value]
        if GameTag.ZONE.value in self.entities[entity_id]:
            zone = self.entities[entity_id][GameTag.ZONE.value]

        return card_id, card_name, cardtype, zone

    def print_entity_pretty(self, entity_id):
        card_id, card_name, cardtype, zone = self.get_default_values(entity_id)

        if card_name and \
                (zone == Zone.PLAY.value and
                 (cardtype in [CardType.HERO.value, CardType.HERO_POWER.value, CardType.MINION.value])) or \
                (zone == Zone.SECRET.value):
            print(f"{entity_id} - Name: {card_name}, CardID: {card_id} Zone: {Zone(zone).name}, CardType: {CardType(cardtype).name}")

            gametags = ["CONTROLLER", "ZONE_POSITION", "PLAYER_TECH_LEVEL", "ATK", "HEALTH", "COST", "TAG_LAST_KNOWN_COST_IN_HAND",
                        "CARDRACE", "RARITY",
                        "TECH_LEVEL", "DIVINE_SHIELD", "TAUNT", "POISONOUS", "WINDFURY",
                        "REBORN", "ELITE", "FROZEN", "LINKED_ENTITY", "CREATOR", "STEALTH", "EXHAUSTED",
                        "DEATHRATTLE", "ATTACHED", "PLAYER_LEADERBOARD_PLACE", "DAMAGE"]
            # GameTag
            for gametag in gametags:
                if GameTag[gametag].value in self.entities[entity_id]:
                    print(f"{gametag}:{self.entities[entity_id][GameTag[gametag].value]}", end=" | ")
            print()

    def print_entities_pretty(self):
        for entity_id in self.entities.keys():
            self.print_entity_pretty(entity_id)

    def game_start(self):
        self.do_line_reader = False
        # noinspection PyUnresolvedReferences
        self.sig_game_start.emit()

    def game_info(self):
        self.do_line_reader = False
        # noinspection PyUnresolvedReferences
        self.sig_game_info.emit()

    def battle_start(self):
        self.game.turn_num = int(self.entities[self.game_entity][GameTag.TURN.value])
        self.game.battle_num = self.game.turn_num // 2

        battle = Battle()

        battle.battle_num = self.game.battle_num

        me_player_id = self.entities[self.me_entity_id][GameTag.PLAYER_ID.value]
        enemy_player_id = self.entities[self.me_entity_id][GameTag.NEXT_OPPONENT_PLAYER_ID.value]

        if me_player_id < enemy_player_id:
            battle.is_me_trigger_first = True
        else:
            battle.is_me_trigger_first = False

        entity_id_to_hsobject_dict = {}
        key_list = list(self.entities.keys())
        key_list.sort()
        for entity_id in key_list:
            card_id, card_name, cardtype, zone = self.get_default_values(entity_id)

            if card_name and zone == Zone.PLAY.value:
                if cardtype == CardType.HERO.value:
                    hero = None  # type: Optional[Hero]
                    if int(self.entities[entity_id][GameTag["CONTROLLER"].value]) == self.me_player_id:  # player hero
                        hero = battle.me.hero
                        if GameTag["PLAYER_LEADERBOARD_PLACE"].value in self.entities[entity_id]:
                            self.game.leaderboard_place = self.entities[entity_id][GameTag.PLAYER_LEADERBOARD_PLACE.value]
                    elif int(self.entities[entity_id][GameTag["CONTROLLER"].value]) == self.enemy_player_id:  # enemy hero
                        hero = battle.enemy.hero
                    hero.card_id = card_id
                    entity_id_to_hsobject_dict[entity_id] = hero
                    hero.zone = Zone(self.entities[entity_id][GameTag["ZONE"].value])

                    if int(self.entities[entity_id][GameTag["CONTROLLER"].value]) == self.me_player_id:  # player hero
                        hero.player = battle.me

                    elif int(self.entities[entity_id][GameTag["CONTROLLER"].value]) == self.enemy_player_id:  # enemy hero
                        hero.player = battle.enemy

                    if GameTag["HEALTH"].value in self.entities[entity_id]:
                        hero.health = self.entities[entity_id][GameTag["HEALTH"].value]
                    if GameTag["DAMAGE"].value in self.entities[entity_id]:
                        hero.damage = self.entities[entity_id][GameTag["DAMAGE"].value]
                    if GameTag["PLAYER_TECH_LEVEL"].value in self.entities[entity_id]:
                        hero.tech_level = self.entities[entity_id][GameTag["PLAYER_TECH_LEVEL"].value]

                elif cardtype == CardType.HERO_POWER.value:
                    if GameTag["CONTROLLER"].value not in self.entities[entity_id]:
                        hsloghandler_logger.error(f"gametag controller not exist, battle: {self.game.battle_num}, entity_id: {entity_id}")

                    hero_power = None  # type: Optional[HeroPower]

                    if int(self.entities[entity_id][GameTag["CONTROLLER"].value]) == self.me_player_id:  # player hero
                        hero_power = battle.me.hero_power
                        hero_power.player = battle.me

                    elif int(self.entities[entity_id][GameTag["CONTROLLER"].value]) == self.enemy_player_id:  # enemy hero
                        hero_power = battle.enemy.hero_power
                        hero_power.player = battle.enemy

                    hero_power.card_id = card_id
                    entity_id_to_hsobject_dict[entity_id] = hero_power
                    hero_power.zone = Zone(self.entities[entity_id][GameTag["ZONE"].value])
                    if 1398 in self.entities[entity_id]:
                        hero_power.used = self.entities[entity_id][1398]


                elif cardtype == CardType.MINION.value:
                    if card_id in ['BGS_029', 'OG_123', 'TB_BaconUps_095']:  # if Shifter Zerus
                        if 1429 in self.entities[entity_id]:
                            card_id = Util.enum_id_to_card_id(self.entities[entity_id][1429])
                    minion = Minion()
                    entity_id_to_hsobject_dict[entity_id] = minion
                    minion.card_id = card_id
                    if GameTag["PREMIUM"].value in self.entities[entity_id]:
                        minion.golden = bool(self.entities[entity_id][GameTag["PREMIUM"].value])
                    if GameTag["BACON_MINION_IS_LEVEL_TWO"].value in self.entities[entity_id]:
                        minion.level2 = bool(self.entities[entity_id][GameTag["BACON_MINION_IS_LEVEL_TWO"].value])
                    if GameTag["ELITE"].value in self.entities[entity_id]:
                        minion.elite = bool(self.entities[entity_id][GameTag["ELITE"].value])
                    if GameTag["TECH_LEVEL"].value in self.entities[entity_id]:
                        minion.tech_level = self.entities[entity_id][GameTag["TECH_LEVEL"].value]
                    if GameTag["COST"].value in self.entities[entity_id]:
                        minion.cost = self.entities[entity_id][GameTag["COST"].value]
                    if GameTag["ATK"].value in self.entities[entity_id]:
                        minion.attack = self.entities[entity_id][GameTag["ATK"].value]
                    if GameTag["HEALTH"].value in self.entities[entity_id]:
                        minion.health = self.entities[entity_id][GameTag["HEALTH"].value]
                    if GameTag["DAMAGE"].value in self.entities[entity_id]:
                        minion.damage = self.entities[entity_id][GameTag["DAMAGE"].value]
                    if GameTag["TAUNT"].value in self.entities[entity_id]:
                        minion.taunt = bool(self.entities[entity_id][GameTag["TAUNT"].value])
                    if GameTag["DIVINE_SHIELD"].value in self.entities[entity_id]:
                        minion.divine_shield = bool(self.entities[entity_id][GameTag["DIVINE_SHIELD"].value])
                    if GameTag["POISONOUS"].value in self.entities[entity_id]:
                        minion.poisonous = bool(self.entities[entity_id][GameTag["POISONOUS"].value])
                    if GameTag["WINDFURY"].value in self.entities[entity_id]:
                        minion.windfury = int(self.entities[entity_id][GameTag["WINDFURY"].value])
                    if GameTag["REBORN"].value in self.entities[entity_id]:
                        minion.reborn = bool(self.entities[entity_id][GameTag["REBORN"].value])
                    if GameTag["DEATHRATTLE"].value in self.entities[entity_id]:
                        minion.deathrattle = bool(self.entities[entity_id][GameTag["DEATHRATTLE"].value])
                    if GameTag["AURA"].value in self.entities[entity_id]:
                        minion.aura = bool(self.entities[entity_id][GameTag["AURA"].value])
                    if GameTag["START_OF_COMBAT"].value in self.entities[entity_id]:
                        minion.start_of_combat = bool(self.entities[entity_id][GameTag["START_OF_COMBAT"].value])
                    if GameTag["OVERKILL"].value in self.entities[entity_id]:
                        minion.overkill = bool(self.entities[entity_id][GameTag["OVERKILL"].value])
                    if GameTag["CARDRACE"].value in self.entities[entity_id]:
                        minion.race = Race(self.entities[entity_id][GameTag["CARDRACE"].value])
                    minion.zone = Zone(self.entities[entity_id][GameTag["ZONE"].value])
                    minion.pos = self.entities[entity_id][GameTag["ZONE_POSITION"].value]
                    if int(self.entities[entity_id][GameTag["CONTROLLER"].value]) == self.me_player_id:
                        minion.player = battle.me
                        battle.me.board[minion.pos] = minion
                    elif int(self.entities[entity_id][GameTag["CONTROLLER"].value]) == self.enemy_player_id:
                        minion.player = battle.enemy
                        battle.enemy.board[minion.pos] = minion

                elif cardtype == CardType.ENCHANTMENT.value:
                    if (not GameTag["ATTACHED"].value in self.entities[entity_id]) or (not GameTag["CREATOR"].value in self.entities[entity_id]):
                        continue
                    attached_id = self.entities[entity_id][GameTag["ATTACHED"].value]
                    creator_id = self.entities[entity_id][GameTag["CREATOR"].value]

                    enchantment = Enchantment()
                    enchantment.card_id = card_id
                    entity_id_to_hsobject_dict[entity_id] = enchantment
                    enchantment.zone = Zone(self.entities[entity_id][GameTag["ZONE"].value])

                    if 323 in self.entities[entity_id] and 324 in self.entities[entity_id]:
                        if self.entities[entity_id][323] == 1 and self.entities[entity_id][324] == 1:
                            enchantment.is_aura = True

                    if int(self.entities[entity_id][GameTag["CONTROLLER"].value]) == self.me_player_id:
                        enchantment.player = battle.me
                    elif int(self.entities[entity_id][GameTag["CONTROLLER"].value]) == self.enemy_player_id:
                        enchantment.player = battle.enemy

                    if attached_id in entity_id_to_hsobject_dict:
                        enchantment.attached_minion = entity_id_to_hsobject_dict[attached_id]
                        entity_id_to_hsobject_dict[attached_id].enchants.append(enchantment)

                        if enchantment.is_aura:
                            entity_id_to_hsobject_dict[attached_id].auras.append(enchantment)
                        else:
                            if enchantment.card_id in DEATHRATTLE_ENCHANT_CARD_IDS:
                                entity_id_to_hsobject_dict[attached_id].enchants.append(enchantment)

                    if creator_id in entity_id_to_hsobject_dict:
                        # entity_id_to_hsobject_dict[creator_id].created_enchants.append(enchantment)
                        enchantment.creator = entity_id_to_hsobject_dict[creator_id]

            elif zone == Zone.SECRET.value:
                secret = Secret()
                secret.card_id = card_id
                if int(self.entities[entity_id][GameTag["CONTROLLER"].value]) == self.me_player_id:  # player hero
                    battle.me.secrets.append(secret)
                elif int(self.entities[entity_id][GameTag["CONTROLLER"].value]) == self.enemy_player_id:  # enemy hero
                    battle.enemy.secrets.append(secret)

        self.game.battle = battle
        self.game.battle_history[self.game.battle_num] = battle
        if self.is_print_console:
            print('='*50)
            print(f"{' '*20}BATTLE{self.game.battle_num}{' '*20}")
            self.print_entities_pretty()

        self.do_line_reader = False
        # noinspection PyUnresolvedReferences
        self.sig_battle_start.emit()

    def battle_end(self):
        key_list = list(self.entities.keys())
        key_list.sort()
        for entity_id in key_list:
            card_id, card_name, cardtype, zone = self.get_default_values(entity_id)

            if cardtype == CardType.HERO.value and zone == Zone.PLAY.value:
                if int(self.entities[entity_id][GameTag["CONTROLLER"].value]) == self.me_player_id:
                    if GameTag["DAMAGE"].value in self.entities[entity_id]:
                        damage = int(self.entities[entity_id][GameTag["DAMAGE"].value])
                        self.game.battle.me.hero.taken_damage = damage - self.game.battle.me.hero.damage
                        self.game.battle.me.hero.damage = damage
                    if GameTag["PLAYER_LEADERBOARD_PLACE"].value in self.entities[entity_id]:
                        self.game.leaderboard_place = int(self.entities[entity_id][GameTag.PLAYER_LEADERBOARD_PLACE.value])
                elif int(self.entities[entity_id][GameTag["CONTROLLER"].value]) == self.enemy_player_id:
                    if GameTag["DAMAGE"].value in self.entities[entity_id]:
                        damage = int(self.entities[entity_id][GameTag["DAMAGE"].value])
                        self.game.battle.enemy.hero.taken_damage = damage - self.game.battle.enemy.hero.damage
                        print("BATTLE", self.game.battle.battle_num," Enemy Damage: ", self.game.battle.enemy.hero.taken_damage)
                        self.game.battle.enemy.hero.damage = damage

        if self.is_print_console:
            print(f"{' '*20}BATTLE END{' '*20}")
            print(f"Damage taken: {self.game.battle.me.hero.taken_damage}")
            print(f"My HP: {self.game.battle.me.hero.health - self.game.battle.me.hero.damage}")
            print(f"Damage give: {self.game.battle.enemy.hero.taken_damage}")
            print(f"Enemy HP: {self.game.battle.enemy.hero.health - self.game.battle.enemy.hero.damage}")
            print('=' * 50)

        self.do_line_reader = False
        # noinspection PyUnresolvedReferences
        self.sig_battle_end.emit()

    def end_game(self):

        key_list = list(self.entities.keys())
        key_list.sort()
        for entity_id in key_list:
            card_id, card_name, cardtype, zone = self.get_default_values(entity_id)

            if cardtype == CardType.HERO.value:
                if int(self.entities[entity_id][GameTag["CONTROLLER"].value]) == self.me_player_id:
                    if GameTag["PLAYER_LEADERBOARD_PLACE"].value in self.entities[entity_id]:
                        self.game.leaderboard_place = int(self.entities[entity_id][GameTag.PLAYER_LEADERBOARD_PLACE.value])
        if self.is_print_console:
            print(f"---------GAME END!!!----------")
            self.print_entities_pretty()

        self.do_line_reader = False

        self.game.game_end = True

        self.sig_end_game.emit()

    def end_file(self):
        self.do_line_reader = False

        self.before_log_file_tell = self.log_file.tell()
        self.log_file.close()

        # noinspection PyUnresolvedReferences
        self.sig_end_file.emit()

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
            if not self.recent_parsing_line:
                return
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
            self.game.build_number = int(BUILD_NUMBER_RE.match(context).group("BuildNumber"))
            if self.game.build_number != VERSION_NUMBER:
                hsloghandler_logger.warning(f"Build number NOT correct, Program: {VERSION_NUMBER}, Log File: {self.game.build_number}")
        elif GAME_TYPE_RE.match(context):
            self.game.game_type = str(GAME_TYPE_RE.match(context).group("GameType"))
        elif FORMAT_TYPE_RE.match(context):
            self.game.format_type = str(FORMAT_TYPE_RE.match(context).group("FormatType"))
        elif SCENARIO_ID_RE.match(context):
            self.game.scenarioID = int(SCENARIO_ID_RE.match(context).group("ScenarioID"))
        elif PLAYER_ID_NAME_RE.match(context):
            player_id = int(PLAYER_ID_NAME_RE.match(context).group("PlayerID"))
            player_name = str(PLAYER_ID_NAME_RE.match(context).group("PlayerName"))
            if self.me_player_id == player_id:
                self.entity_names[player_name] = self.me_entity_id
            elif self.enemy_player_id == player_id:
                self.entity_names[player_name] = self.enemy_entity_id
                self.game_info()
        else:
            hsloghandler_logger.error(f"print_game_parser() error: {context}")

    def entity_parser(self, context, level=0):
        context_level = (len(context) - len(context.lstrip())) // 4
        if context_level > level:
            self.contexts[level].append(context)
            return
        words = context.split()

        try:
            power_type = PowerType[words[0]]
        except KeyError:
            hsloghandler_logger.exception(f"entity_parser() error: unknown entity type: {words[0]}")
            return

        if power_type in (PowerType.BLOCK_END, PowerType.SUB_SPELL_END):
            if level < len(self.contexts):
                self.contexts[level].append(context)
                self.call_handler(level)
        elif power_type in (PowerType.CREATE_GAME, PowerType.BLOCK_START, PowerType.FULL_ENTITY, PowerType.CHANGE_ENTITY,
                            PowerType.SHOW_ENTITY, PowerType.META_DATA, PowerType.SUB_SPELL_START):
            self.call_handler(context_level)
            if len(self.contexts) != level:
                hsloghandler_logger.error(f"entity_parser() error: level not correct, context: {context}, level: {level}")
            self.contexts.append(list())
            self.contexts[level].append(context)
        elif power_type in (PowerType.TAG_CHANGE, PowerType.HIDE_ENTITY):
            self.call_handler(level)
            self.contexts.append(list())
            self.contexts[level].append(context)
            self.call_handler(level)

    def call_handler(self, level):
        start_idx = len(self.contexts) - 1
        for i in range(start_idx, level - 1, -1):
            if not self.contexts[i]:
                del self.contexts[i]
                continue
            opcode = self.contexts[i][0].split()[0]
            if opcode == "CREATE_GAME":
                self.create_game_handler(level)
            elif opcode == "FULL_ENTITY":
                self.full_entity_handler(i)
            elif opcode == "TAG_CHANGE":
                self.tag_change_handler(i)
            elif opcode == "BLOCK_START":
                self.block_handler(i)
            elif opcode == "SHOW_ENTITY":
                self.show_entity_handler(i)
            elif opcode == "HIDE_ENTITY":
                self.hide_entity_handler(i)
            elif opcode == "META_DATA":
                self.meta_data_handler(i)
            elif opcode == "CHANGE_ENTITY":
                self.change_entity_handler(i)
            elif opcode == "SUB_SPELL_START":
                self.sub_spell_handler(i)
            else:
                HSLogHandler.error(f"call_handler() error, no opcode: {self.contexts[i]}")
            del self.contexts[i]

    def create_game_handler(self, level):
        self.init_game()

        entity_id = None
        for text in self.contexts[level]:
            text = text.lstrip()
            if CREATE_GAME_ENTITY_RE.match(text):
                continue
            elif GAME_ENTITY_RE.match(text):
                entity_id = int(GAME_ENTITY_RE.match(text).group("EntityID"))
                self.entities[entity_id] = {}
                self.entity_names["GameEntity"] = entity_id
                self.game_entity = entity_id
            elif PLAYER_ENTITY_RE.match(text):
                match_data = PLAYER_ENTITY_RE.match(text)
                entity_id = int(match_data.group("EntityID"))
                player_id = int(match_data.group("PlayerID"))
                self.entities[entity_id] = {}
                if not self.me_entity_id:
                    self.me_entity_id = entity_id
                    self.me_player_id = player_id
                else:
                    self.enemy_entity_id = entity_id
                    self.enemy_player_id = player_id
            elif TAG_VALUE_RE.match(text):
                tag, value = TAG_VALUE_RE.match(text).group("tag", "value")
                tag, value = Util.tag_value_to_int(tag, value)
                self.entities[entity_id][tag] = value

        self.game_start()

    def block_handler(self, level):
        text = self.contexts[level][0].strip()
        match_data = BLOCK_START_ENTITY_RE.match(text)

        blocktype = match_data.group("BlockType")
        entity_id = self.get_entity_id_by_entity(match_data.group("Entity"))
        self.is_hero_contain[level] = False

        line_num = len(self.contexts[level])
        for i in range(1, line_num-1):
            self.entity_parser(self.contexts[level][i], level + 1)
        if self.contexts[level][line_num-1].split()[0] != "BLOCK_END":
            self.entity_parser(self.contexts[level][line_num-1], level + 1)
        self.call_handler(level+1)

        if blocktype == "TRIGGER" and entity_id == self.baconshop8playerenchant:
            if self.is_hero_contain[level]:
                self.battle_start()

    def add_tag_values_entities(self, entity_id, text):
        text = text.lstrip()
        if TAG_VALUE_RE.match(text):
            tag, value = TAG_VALUE_RE.match(text).group("tag", "value")
            tag, value = Util.tag_value_to_int(tag, value)
            self.entities[entity_id][tag] = value
        else:
            hsloghandler_logger.error(f"add_tag_values_entities Error - tag/value: {text}")

    def full_entity_handler(self, level):
        text = self.contexts[level][0].strip()

        if not FULL_ENTITY_CREATING_RE.match(text):
            hsloghandler_logger.error(f"full_entity_handler Error - FULL_ENTITY: {text}")
            return
        entity_id, card_id = FULL_ENTITY_CREATING_RE.match(text).group("ID", "CardID")
        entity_id = int(entity_id)
        self.entities[entity_id] = {}
        self.card_ids[entity_id] = card_id

        if card_id == "TB_BaconShopBob":
            bob_name = Util.card_name_by_id(card_id, locale=LOCALE)
            self.entity_names[bob_name] = entity_id

        if card_id == "TB_BaconShop_8P_PlayerE":
            self.baconshop8playerenchant = entity_id

        for text in self.contexts[level][1:]:
            self.add_tag_values_entities(entity_id, text)

        if GameTag.CARDTYPE.value in self.entities[entity_id]:
            cardtype = self.entities[entity_id][GameTag.CARDTYPE.value]
            if cardtype == CardType.HERO.value:
                self.is_hero_contain[level - 1] = True

    def tag_change_handler(self, level):
        if len(self.contexts[level]) != 1:
            hsloghandler_logger.error(f"tag_change_handler Error - self.contexts too long: {self.contexts[level]}")
            return
        text = self.contexts[level][0].strip()
        match_data = TAG_CHANGE_RE.match(text)
        if not match_data:
            hsloghandler_logger.error(f"tag_change_handler Error - match error: {text}")
            return

        entity = match_data.group("Entity")
        tag = match_data.group("tag")
        value = match_data.group("value")
        entity_id = self.get_entity_id_by_entity(entity)

        tag, value = Util.tag_value_to_int(tag, value)
        self.entities[entity_id][tag] = value

        if entity_id == self.game_entity and GameTag.STATE.value in self.entities[self.game_entity]:
            if self.entities[self.game_entity][GameTag.STATE.value] == State.COMPLETE:
                self.is_game_end = True
                self.end_game()

        if ((entity_id == self.me_entity_id and tag == 1481 and value == 0) or tag == 479 and value == 0) and not self.game.battle.is_end:
            self.game.battle.is_end = True
            self.battle_end()

    def show_entity_handler(self, level):
        text = self.contexts[level][0].strip()

        if not SHOW_ENTITY_RE.match(text):
            hsloghandler_logger.error(f"show_entity_handler Error - SHOW_ENTITY: {text}")
            return
        entity, card_id = SHOW_ENTITY_RE.match(text).group("Entity", "CardID")

        entity_id = self.get_entity_id_by_entity(entity)
        if card_id:
            self.card_ids[entity_id] = card_id

        for text in self.contexts[level][1:]:
            self.add_tag_values_entities(entity_id, text)

    def hide_entity_handler(self, level):
        text = self.contexts[level][0].strip()

        if not HIDE_ENTITY_RE.match(text):
            hsloghandler_logger.error(f"hide_entity_handler Error - HIDE_ENTITY: {text}")
            return
        entity, tag, value = HIDE_ENTITY_RE.match(text).group("Entity", "tag", "value")

        entity_id = self.get_entity_id_by_entity(entity)
        tag, value = Util.tag_value_to_int(tag, value)
        self.entities[entity_id][tag] = value

    def meta_data_handler(self, level):
        pass

    def change_entity_handler(self, level):
        text = self.contexts[level][0].strip()

        if not CHANGE_ENTITY_RE.match(text):
            hsloghandler_logger.error(f"change_entity_handler Error - CHANGE_ENTITY: {text}")
            return
        entity, card_id = CHANGE_ENTITY_RE.match(text).group("Entity", "CardID")

        entity_id = self.get_entity_id_by_entity(entity)

        for text in self.contexts[level][1:]:
            self.add_tag_values_entities(entity_id, text)

    def sub_spell_handler(self, level):
        line_num = len(self.contexts[level])
        for i in range(1, line_num - 1):
            if self.contexts[level][i].lstrip().startswith("Source") \
                    or self.contexts[level][i].lstrip().startswith("Targets"):
                continue
            self.entity_parser(self.contexts[level][i], level + 1)
        if self.contexts[level][line_num-1].split()[0] != "SUB_SPELL_END" and \
                not(self.contexts[level][line_num-1].lstrip().startswith("Source")
                    or self.contexts[level][line_num-1].lstrip().startswith("Targets")):
            self.entity_parser(self.contexts[level][line_num-1], level + 1)
            # self.entity_parser((" "*4*level) + "SUB_SPELL_END", level + 1)
        self.call_handler(level+1)


if __name__ == '__main__':
    HS_LOG_FILE_DIR = 'Test/logs'
    log_file_2020_03_06_20_31_28 = open(os.path.join(HS_LOG_FILE_DIR, "2020-03-06 20-31-28.log"), 'r', encoding="UTF8")
    log_file_2020_02_29_21_06_42 = open(os.path.join(HS_LOG_FILE_DIR, "2020-02-29 21-06-42.log"), 'r', encoding="UTF8")
    log_file_2020_03_01_21_19_18 = open(os.path.join(HS_LOG_FILE_DIR, "2020-03-01 21-19-18.log"), 'r', encoding="UTF8")
    log_file_2020_03_21_23_33_29 = open(os.path.join(HS_LOG_FILE_DIR, "2020-03-21 23-33-29.log"), 'r', encoding="UTF8")
    power = open(os.path.join(HS_LOG_FILE_DIR, "Power.log"), 'r', encoding="UTF8")
    power_old = open(os.path.join(HS_LOG_FILE_DIR, "Power_old.log"), 'r', encoding="UTF8")

    log_handler = HSLogHandler(log_file_2020_03_06_20_31_28, is_print_console=True)
    log_handler.line_reader_start()
