import os
import logging
import hearthstone.enums as hsenums
from PySide2.QtCore import Signal, QObject
from hearthstone.enums import GameTag, CardType, Faction, Race, Rarity, Zone, Step, State


from BobsSimulator.Util import card_name_by_id, tag_value_to_int, qsleep
from BobsSimulator.HSType import Game, Battle, Hero, Minion, Secret, \
    ENTITY_TYPES, DEATHRATTLE_BUFF_CARDIDS, BOB_NAMES, Enchantment
from BobsSimulator.Regex import *
from BobsSimulator.HSLogging import hsloghandler_logger
from BobsSimulator.Main import VERSION_NUMBER
import hearthstone_data


class HSLogHandler(QObject):
    # Signals
    sig_game_start = Signal()
    sig_game_info = Signal()
    sig_battle_start = Signal()
    sig_battle_end = Signal()
    sig_end_game = Signal()
    sig_end_file = Signal()

    def __init__(self, log_file, is_print_console=False):
        super().__init__()
        self.log_file = log_file
        self.is_print_console = is_print_console

        hsloghandler_logger.info(f"HSLogHandler Start: {log_file.name}")

        self.init_game()

        self.contexts = []
        self.recent_parsing_line = None
        self.do_line_reader = False
        self.is_line_reader = False

    def init_game(self):
        self.game = Game()

        self.entities = {}  # entity id -> tag/value dict -> value
        self.entity_names = {}  # entity name -> entity id
        self.is_hero_contain = {}  # key: level, value: bool

        self.game_entity = None
        self.baconshop8playerenchant = None
        self.player_entity_id = None
        self.player_player_id = None
        self.enemy_entity_id = None
        self.enemy_player_id = None

    def read_line(self):
        return self.log_file.readline()

    def line_reader_start(self):
        self.do_line_reader = True
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
        entity_id = None
        if ENTITY_DESCRIPTION_RE.match(entity):
            entity_id = int(ENTITY_DESCRIPTION_RE.match(entity).group("id"))
        elif entity.isdigit():
            entity_id = int(entity)
        elif entity in self.entity_names:
            entity_id = self.entity_names[entity]
        else:
            entity_id = self.enemy_entity_id
        return entity_id

    def print_entity_pretty(self, entity_id):
        card_name = ""
        zone = ""
        cardtype = ""
        card_id = ""

        if 'CardID' in self.entities[entity_id]:
            card_id = self.entities[entity_id]['CardID']
            card_name = card_name_by_id(card_id)

        if GameTag.ZONE.value in self.entities[entity_id]:
            zone = self.entities[entity_id][GameTag.ZONE.value]

        if GameTag.CARDTYPE.value in self.entities[entity_id]:
            cardtype = self.entities[entity_id][GameTag.CARDTYPE.value]


        if card_name and \
                zone == Zone.PLAY.value and \
                (cardtype in [CardType.HERO.value, CardType.HERO_POWER.value, CardType.MINION.value] or
                 card_id in DEATHRATTLE_BUFF_CARDIDS):
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


        if card_name and \
                zone == Zone.SECRET.value:
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
        self.sig_game_start.emit()

    def game_info(self):
        self.do_line_reader = False
        self.sig_game_info.emit()

    def battle_start(self):
        self.game.turn_num = int(self.entities[self.game_entity][GameTag.TURN.value])
        self.game.battle_num = self.game.turn_num // 2

        battle = Battle()

        entity_id_to_minion_dict = {}
        key_list = list(self.entities.keys())
        key_list.sort()
        for entity_id in key_list:
            card_name = ""
            zone = ""
            cardtype = ""
            card_id = ""

            if 'CardID' in self.entities[entity_id]:
                card_id = self.entities[entity_id]['CardID']
                card_name = card_name_by_id(card_id)
            if GameTag.ZONE.value in self.entities[entity_id]:
                zone = self.entities[entity_id][GameTag.ZONE.value]
            if GameTag.CARDTYPE.value in self.entities[entity_id]:
                cardtype = self.entities[entity_id][GameTag.CARDTYPE.value]



            if card_name and zone == Zone.PLAY.value:
                if cardtype == CardType.HERO.value:
                    if int(self.entities[entity_id][GameTag["CONTROLLER"].value]) == self.player_player_id:  # player hero
                        battle.me.hero.entity_id = entity_id
                        battle.me.hero.card_id = card_id
                        if GameTag["HEALTH"].value in self.entities[entity_id]:
                            battle.me.hero.health = self.entities[entity_id][GameTag["HEALTH"].value]
                        if GameTag["DAMAGE"].value in self.entities[entity_id]:
                            battle.me.hero.damage = self.entities[entity_id][GameTag["DAMAGE"].value]
                        if GameTag["PLAYER_TECH_LEVEL"].value in self.entities[entity_id]:
                            battle.me.hero.tech_level = self.entities[entity_id][GameTag["PLAYER_TECH_LEVEL"].value]
                        if GameTag["PLAYER_LEADERBOARD_PLACE"].value in self.entities[entity_id]:
                            self.game.leaderboard_place = self.entities[entity_id][GameTag.PLAYER_LEADERBOARD_PLACE.value]
                    elif int(self.entities[entity_id][GameTag["CONTROLLER"].value]) == self.enemy_player_id:  # enemy hero
                        battle.enemy.hero.entity_id = entity_id
                        battle.enemy.hero.card_id = card_id
                        if GameTag["HEALTH"].value in self.entities[entity_id]:
                            battle.enemy.hero.health = self.entities[entity_id][GameTag["HEALTH"].value]
                        if GameTag["DAMAGE"].value in self.entities[entity_id]:
                            battle.enemy.hero.damage = self.entities[entity_id][GameTag["DAMAGE"].value]

                        if GameTag["PLAYER_TECH_LEVEL"].value in self.entities[entity_id]:
                            battle.enemy.hero.tech_level = self.entities[entity_id][GameTag["PLAYER_TECH_LEVEL"].value]

                elif cardtype == CardType.HERO_POWER.value:
                    if GameTag["CONTROLLER"].value not in self.entities[entity_id]:
                        hsloghandler_logger.error(f"gametag controller not exist, battle: {self.game.battle_num}, entity_id: {entity_id}")
                    if int(self.entities[entity_id][GameTag["CONTROLLER"].value]) == self.player_player_id:  # player hero
                        battle.me.hero_power.entity_id = entity_id
                        battle.me.hero_power.card_id = card_id
                        if GameTag["EXHAUSTED"].value in self.entities[entity_id]:
                            battle.me.hero_power.exhausted = self.entities[entity_id][GameTag["EXHAUSTED"].value]
                    elif int(self.entities[entity_id][GameTag["CONTROLLER"].value]) == self.enemy_player_id:  # enemy hero
                        battle.enemy.hero_power.entity_id = entity_id
                        battle.enemy.hero_power.card_id = card_id
                        if GameTag["EXHAUSTED"].value in self.entities[entity_id]:
                            battle.enemy.hero_power.exhausted = self.entities[entity_id][GameTag["EXHAUSTED"].value]

                elif cardtype == CardType.MINION.value:
                    minion = Minion()
                    entity_id_to_minion_dict[entity_id] = minion
                    minion.entity_id = entity_id
                    minion.card_id = card_id
                    if GameTag["PREMIUM"].value in self.entities[entity_id]:
                        minion.golden = bool(self.entities[entity_id][GameTag["PREMIUM"].value])
                    if GameTag["BACON_MINION_IS_LEVEL_TWO"].value in self.entities[entity_id]:
                        minion.level2 = bool(self.entities[entity_id][GameTag["BACON_MINION_IS_LEVEL_TWO"].value])
                    if GameTag["ELITE"].value in self.entities[entity_id]:
                        minion.elite = bool(self.entities[entity_id][GameTag["ELITE"].value])
                    if GameTag["TECH_LEVEL"].value in self.entities[entity_id]:
                        minion.tech_level = self.entities[entity_id][GameTag["TECH_LEVEL"].value]
                    if GameTag["EXHAUSTED"].value in self.entities[entity_id]:
                        minion.exhausted = bool(self.entities[entity_id][GameTag["EXHAUSTED"].value])
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
                    if GameTag["CHARGE"].value in self.entities[entity_id]:
                        minion.charge = bool(self.entities[entity_id][GameTag["CHARGE"].value])
                    if GameTag["MODULAR"].value in self.entities[entity_id]:
                        minion.modular = bool(self.entities[entity_id][GameTag["MODULAR"].value])
                    if GameTag["DEATHRATTLE"].value in self.entities[entity_id]:
                        minion.deathrattle = bool(self.entities[entity_id][GameTag["DEATHRATTLE"].value])
                    if GameTag["BATTLECRY"].value in self.entities[entity_id]:
                        minion.battlecry = bool(self.entities[entity_id][GameTag["BATTLECRY"].value])
                    if GameTag["DISCOVER"].value in self.entities[entity_id]:
                        minion.discover = bool(self.entities[entity_id][GameTag["DISCOVER"].value])
                    if GameTag["AURA"].value in self.entities[entity_id]:
                        minion.aura = bool(self.entities[entity_id][GameTag["AURA"].value])
                    if GameTag["START_OF_COMBAT"].value in self.entities[entity_id]:
                        minion.start_of_combat = bool(self.entities[entity_id][GameTag["START_OF_COMBAT"].value])
                    if GameTag["OVERKILL"].value in self.entities[entity_id]:
                        minion.overkill = bool(self.entities[entity_id][GameTag["OVERKILL"].value])
                    if GameTag["TAG_SCRIPT_DATA_NUM_1"].value in self.entities[entity_id]:
                        minion.TAG_SCRIPT_DATA_NUM_1 = self.entities[entity_id][GameTag["TAG_SCRIPT_DATA_NUM_1"].value]
                    if GameTag["TAG_SCRIPT_DATA_NUM_2"].value in self.entities[entity_id]:
                        minion.TAG_SCRIPT_DATA_NUM_2 = self.entities[entity_id][GameTag["TAG_SCRIPT_DATA_NUM_2"].value]

                    minion.zone = zone
                    minion.pos = self.entities[entity_id][GameTag["ZONE_POSITION"].value]
                    if int(self.entities[entity_id][GameTag["CONTROLLER"].value]) == self.player_player_id:
                        minion.is_mine = True
                        battle.me.board[minion.pos] = minion
                    elif int(self.entities[entity_id][GameTag["CONTROLLER"].value]) == self.enemy_player_id:
                        minion.is_mine = False
                        battle.enemy.board[minion.pos] = minion
                elif cardtype == CardType.ENCHANTMENT.value:
                    if not GameTag["ATTACHED"].value in self.entities[entity_id]:
                        continue
                    enchantment = Enchantment()
                    enchantment.entity_id = entity_id
                    enchantment.card_id = card_id
                    enchantment.attached_id = self.entities[entity_id][GameTag["ATTACHED"].value]

                    if enchantment.attached_id in entity_id_to_minion_dict:
                        entity_id_to_minion_dict[enchantment.attached_id].enchantments.append(enchantment)

            elif zone == Zone.SECRET.value:
                secret = Secret()
                secret.entity_id = entity_id
                secret.card_id = card_id
                if int(self.entities[entity_id][GameTag["CONTROLLER"].value]) == self.player_player_id:  # player hero
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
        self.sig_battle_start.emit()

    def battle_end(self):
        key_list = list(self.entities.keys())
        key_list.sort()
        for entity_id in key_list:
            card_name = ""
            zone = ""
            cardtype = ""
            card_id = ""

            if 'CardID' in self.entities[entity_id]:
                card_id = self.entities[entity_id]['CardID']
                card_name = card_name_by_id(card_id)
            if GameTag.ZONE.value in self.entities[entity_id]:
                zone = self.entities[entity_id][GameTag.ZONE.value]
            if GameTag.CARDTYPE.value in self.entities[entity_id]:
                cardtype = self.entities[entity_id][GameTag.CARDTYPE.value]

            if cardtype == CardType.HERO.value and (zone == Zone.PLAY.value or zone == Zone.GRAVEYARD.value):
                if int(self.entities[entity_id][GameTag["CONTROLLER"].value]) == self.player_player_id:
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
                        self.game.battle.enemy.hero.damage = damage

        if self.is_print_console:
            print(f"{' '*20}BATTLE END{' '*20}")
            print(f"Damage taken: {self.game.battle.me.hero.taken_damage}")
            print(f"My HP: {self.game.battle.me.hero.health - self.game.battle.me.hero.damage}")
            print(f"Damage give: {self.game.battle.enemy.hero.taken_damage}")
            print(f"Enemy HP: {self.game.battle.enemy.hero.health - self.game.battle.enemy.hero.damage}")
            print('=' * 50)

        self.do_line_reader = False
        self.sig_battle_end.emit()

    def end_game(self):

        key_list = list(self.entities.keys())
        key_list.sort()
        for entity_id in key_list:
            card_name = ""
            zone = ""
            cardtype = ""
            card_id = ""

            if 'CardID' in self.entities[entity_id]:
                card_id = self.entities[entity_id]['CardID']
                card_name = card_name_by_id(card_id)
            if GameTag.ZONE.value in self.entities[entity_id]:
                zone = self.entities[entity_id][GameTag.ZONE.value]
            if GameTag.CARDTYPE.value in self.entities[entity_id]:
                cardtype = self.entities[entity_id][GameTag.CARDTYPE.value]

            if cardtype == CardType.HERO.value:
                if int(self.entities[entity_id][GameTag["CONTROLLER"].value]) == self.player_player_id:
                    if GameTag["PLAYER_LEADERBOARD_PLACE"].value in self.entities[entity_id]:
                        self.game.leaderboard_place = int(self.entities[entity_id][GameTag.PLAYER_LEADERBOARD_PLACE.value])
        if self.is_print_console:
            print(f"---------GAME END!!!----------")
            self.print_entities_pretty()

        self.do_line_reader = False
        self.sig_end_game.emit()

    def end_file(self):
        self.do_line_reader = False
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
            is_found = False
            for entity_id, entity_tags in self.entities.items():
                if "PlayerID" in entity_tags and self.entities[entity_id]["PlayerID"] == player_id:
                    self.entity_names[player_name] = entity_id
                    is_found = True
                    break
            if not is_found:
                hsloghandler_logger.error(f"print_game_parser() error - PLAYER_ID not found: {context}")

            if not self.game.player_battle_tag:
                self.game.player_battle_tag = player_name
            else:  # print game parser end
                self.game_info()
        else:
            hsloghandler_logger.error(f"print_game_parser() error: {context}")

    def entity_parser(self, context, level=0):
        context_level = (len(context) - len(context.lstrip())) // 4
        if context_level > level:
            self.contexts[level].append(context)
            return
        words = context.split()
        if words[0] in ENTITY_TYPES:
            if words[0] == "BLOCK_END" or words[0] == "SUB_SPELL_END":
                if level < len(self.contexts):
                    self.contexts[level].append(context)
                    self.call_handler(level)
            elif words[0] == "CREATE_GAME" or words[0] == "BLOCK_START" or words[0] == "FULL_ENTITY" or words[0] == "CHANGE_ENTITY" \
                    or words[0] == "SHOW_ENTITY" or words[0] == "META_DATA" or words[0] == "SUB_SPELL_START":
                self.call_handler(context_level)
                if len(self.contexts) != level:
                    hsloghandler_logger.error(f"entity_parser() error: level not correct, context: {context}, level: {level}")
                self.contexts.append(list())
                self.contexts[level].append(context)
            elif words[0] == "TAG_CHANGE" or words[0] == "HIDE_ENTITY":
                self.call_handler(level)
                self.contexts.append(list())
                self.contexts[level].append(context)
                self.call_handler(level)
        else:
            hsloghandler_logger.error(f"entity_parser() error: unknown entity type: {words[0]}")

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
                account_id_hi = int(match_data.group("hi"))
                account_id_lo = int(match_data.group("lo"))
                self.entities[entity_id] = {}
                self.entities[entity_id]["PlayerID"] = player_id
                self.entities[entity_id]["hi"] = account_id_hi
                self.entities[entity_id]["lo"] = account_id_lo
                if not self.player_entity_id:
                    self.player_entity_id = entity_id
                    self.player_player_id = player_id
                else:
                    self.enemy_entity_id = entity_id
                    self.enemy_player_id = player_id
            elif TAG_VALUE_RE.match(text):
                tag, value = TAG_VALUE_RE.match(text).group("tag", "value")
                tag, value = tag_value_to_int(tag, value)
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

    def full_entity_handler(self, level):
        text = self.contexts[level][0].strip()

        if not FULL_ENTITY_CREATING_RE.match(text):
            hsloghandler_logger.error(f"full_entity_handler Error - FULL_ENTITY: {text}")
            return
        entity_id, card_id = FULL_ENTITY_CREATING_RE.match(text).group("ID", "CardID")
        entity_id = int(entity_id)
        self.entities[entity_id] = {}
        self.entities[entity_id]["CardID"] = card_id

        if card_id == "TB_BaconShopBob":
            for bob_name in BOB_NAMES:
                self.entity_names[bob_name] = entity_id

        if card_id == "TB_BaconShop_8P_PlayerE":
            self.baconshop8playerenchant = entity_id

        for text in self.contexts[level][1:]:
            text = text.lstrip()
            if TAG_VALUE_RE.match(text):
                tag, value = TAG_VALUE_RE.match(text).group("tag", "value")
                tag, value = tag_value_to_int(tag, value)
                self.entities[entity_id][tag] = value
            else:
                hsloghandler_logger.error(f"full_entity_handler Error - tag/value: {text}")

        if self.entities[entity_id]["CardID"].upper().find('HERO') != -1:
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

        tag, value = tag_value_to_int(tag, value)
        self.entities[entity_id][tag] = value

        if entity_id == self.game_entity and GameTag.STATE.value in self.entities[self.game_entity]:
            if self.entities[self.game_entity][GameTag.STATE.value] == State.COMPLETE:
                self.end_game()

        if entity_id == self.player_entity_id and tag == 1481 and value == 0:
            self.battle_end()

    def show_entity_handler(self, level):
        text = self.contexts[level][0].strip()

        if not SHOW_ENTITY_RE.match(text):
            hsloghandler_logger.error(f"show_entity_handler Error - SHOW_ENTITY: {text}")
            return
        entity, card_id = SHOW_ENTITY_RE.match(text).group("Entity", "CardID")

        entity_id = self.get_entity_id_by_entity(entity)
        if card_id:
            self.entities[entity_id]['CardID'] = card_id

        for text in self.contexts[level][1:]:
            text = text.lstrip()
            if TAG_VALUE_RE.match(text):
                tag, value = TAG_VALUE_RE.match(text).group("tag", "value")
                tag, value = tag_value_to_int(tag, value)
                self.entities[entity_id][tag] = value
            else:
                hsloghandler_logger.error(f"show_entity_handler Error - tag/value: {text}")

    def hide_entity_handler(self, level):
        text = self.contexts[level][0].strip()

        if not HIDE_ENTITY_RE.match(text):
            hsloghandler_logger.error(f"hide_entity_handler Error - HIDE_ENTITY: {text}")
            return
        entity, tag, value = HIDE_ENTITY_RE.match(text).group("Entity", "tag", "value")

        entity_id = self.get_entity_id_by_entity(entity)
        tag, value = tag_value_to_int(tag, value)
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
            text = text.lstrip()
            if TAG_VALUE_RE.match(text):
                tag, value = TAG_VALUE_RE.match(text).group("tag", "value")
                tag, value = tag_value_to_int(tag, value)
                self.entities[entity_id][tag] = value
            else:
                hsloghandler_logger.error(f"change_entity_handler Error - tag/value: {text}")

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


