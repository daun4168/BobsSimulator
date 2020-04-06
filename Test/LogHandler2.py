import os
import logging
import hearthstone.enums as hsenums
from PySide2.QtCore import Signal, QObject
from hearthstone.enums import GameTag, CardType, Faction, Race, Rarity, Zone, Step, State

from BobsSimulator.Util import Util
from BobsSimulator.HSType import Hero, Minion, Battle
from BobsSimulator.Regex import *

HS_LOG_FILE_DIR = os.path.join(os.getcwd(), "Test/logs")
HS_LOG_FILE_NAME = "2020-03-06 20-31-28.log"

REAL_TIME_LOG_FILE_DIR = r"C:\Program Files (x86)\Hearthstone\Logs"
REAL_TIME_LOG_FILE_NAME = "Power.log"

THIS_LOG_FILE_NAME = "test.log"


class HSBugFilter(logging.Filter):

    def filter(self, record):
        return record.getMessage().find("폭풍 마나") == -1


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    handlers=[logging.FileHandler(THIS_LOG_FILE_NAME, 'w', 'utf-8')])

hslogger = logging.getLogger('HS')
logging = hslogger

f = HSBugFilter()
hslogger.addFilter(f)
hslogger.info("Program Start")

HS_BUILD_NUMBER = 42174

hs_log_file = open(os.path.join(HS_LOG_FILE_DIR, HS_LOG_FILE_NAME), 'r', encoding="UTF8")
# real_log_file = open(os.path.join(REAL_TIME_LOG_FILE_DIR, REAL_TIME_LOG_FILE_NAME), 'r', encoding="UTF8")


GameStateDebugPrintPowerTXT = open("Test/logs/GameStateDebugPrintPower.log", 'w', encoding="UTF8")
GameStateDebugPrintGameTXT = open("Test/logs/GameStateDebugPrintGame.log", 'w', encoding="UTF8")
PowerTaskListDebugPrintPowerTXT = open("Test/logs/PowerTaskListDebugPrintPower.log", 'w', encoding="UTF8")


# # LOG TEST
# try:
#     print(hearthstone.enums.GameTag.DISABLE_GOLDEN_ANIMATION.value)
# except AttributeError as e:
#     print(f"Unknown tag Error: {e}")
#     logging.warning(f"Unknown tag Error: {e}")


class HSGame(QObject):
    battle_start = Signal(int)

    def __init__(self, log_file):
        self.trigger_keywords = set()
        super().__init__()
        self.log_file = log_file

        self.build_number = None
        self.game_type = None
        self.format_type = None
        self.scenarioID = None

        self.debug_print_line_num = 0
        self.full_entity_num = 0
        self.block_num = 0
        self.sub_spell_num = 0
        self.create_game_num = 0
        self.tag_change_num = 0
        self.show_entity_num = 0
        self.hide_entity_num = 0
        self.meta_data_num = 0
        self.change_entity_num = 0

        self.entities = {}  # entity id -> tag/value dict -> value
        self.entity_names = {}  # entity name -> entity id
        self.game_entity = None
        self.player_me = None
        self.player_other = None
        self.baconshop8playerenchant = None
        self.game_turn = 0

        self.minions_me = []
        self.minions_other = []
        self.graveyard_me = []
        self.graveyard_other = []

        self.contexts = []
        self.recent_parsing_line = None

        # self.line_reader()

        self.is_hero_contain = {}  # key: level, value: bool


    def print_trigger(self):
        print(self.trigger_keywords)

    def init_game(self):
        self.entities = {}
        self.entity_names = {}
        self.game_entity = None
        self.player_me = None
        self.player_other = None
        self.baconshop8playerenchant = None
        self.game_turn = 0

        self.minions_me = [None] * 7
        self.minions_other = [None] * 7
        self.graveyard_me = []
        self.graveyard_other = []

        self.is_hero_contain = {}  # key: level, value: bool

    def read_line(self):
        return self.log_file.readline()

    def line_reader(self):
        line = self.read_line()
        while line:
            self.line_parser(line)
            line = self.read_line()

    @staticmethod
    def tag_value_to_int(tag, value):
        if not tag.isdigit():
            try:
                tag = int(hsenums.GameTag[tag])
            except KeyError:
                logging.error(f"tag_value_to_int() key(tag) error - no tag key, tag: {tag}, value: {value}")
        else:
            tag = int(tag)

        if not value.isdigit():
            try:
                if tag == int(hsenums.GameTag.CARDTYPE):
                    value = int(hsenums.CardType[value])
                elif tag == int(hsenums.GameTag.FACTION):
                    value = int(hsenums.Faction[value])
                elif tag == int(hsenums.GameTag.CARDRACE):
                    value = int(hsenums.Race[value])
                elif tag == int(hsenums.GameTag.RARITY):
                    value = int(hsenums.Rarity[value])
                elif tag == int(hsenums.GameTag.ZONE):
                    value = int(hsenums.Zone[value])
                elif tag == int(hsenums.GameTag.MULLIGAN_STATE):
                    value = int(hsenums.Mulligan[value])
                elif tag == int(hsenums.GameTag.STEP) or tag == int(hsenums.GameTag.NEXT_STEP):
                    value = int(hsenums.Step[value])
                elif tag == int(hsenums.GameTag.PLAYSTATE):
                    value = int(hsenums.PlayState[value])
                elif tag == int(hsenums.GameTag.STATE):
                    value = int(hsenums.State[value])

                else:
                    logging.error(f"tag_value_to_int() key(value) error - no tag name, tag: {tag}, value: {value}")
            except KeyError:
                logging.error(f"tag_value_to_int() key(value) error - no value key, tag: {tag}, value: {value}")
        else:
            value = int(value)

        return tag, value

    def activate_game(self, entity_id):
        if entity_id == self.game_entity and GameTag.STATE.value in self.entities[self.game_entity]:
            if self.entities[self.game_entity][GameTag.STATE.value] == State.COMPLETE:
                print(f"---------GAME END!!!----------")

                self.print_entities_pretty()

    def print_entity_pretty(self, entity_id):
        card_name = ""
        zone = ""
        cardtype = ""
        card_id = ""

        if 'CardID' in self.entities[entity_id]:
            card_id = self.entities[entity_id]['CardID']
            card_name = Util.card_name_by_id(card_id)

        if GameTag.ZONE.value in self.entities[entity_id]:
            zone = self.entities[entity_id][GameTag.ZONE.value]

        if GameTag.CARDTYPE.value in self.entities[entity_id]:
            cardtype = self.entities[entity_id][GameTag.CARDTYPE.value]

        if card_name and \
                zone == Zone.PLAY.value and \
                cardtype in [CardType.HERO.value, CardType.MINION.value, CardType.HERO_POWER.value]:
            # # zone in [Zone.PLAY.value, Zone.DECK.value, Zone.HAND.value, Zone.SETASIDE.value]:
            # print(f"{entity_id} - Name: {card_name}, Zone: {Zone(zone).name}, CardType: {CardType(cardtype).name}")
            #
            # gametags = ["CONTROLLER", "ZONE_POSITION", "PLAYER_TECH_LEVEL", "ATK", "HEALTH", "COST", "TAG_LAST_KNOWN_COST_IN_HAND",
            #             "CARDRACE", "RARITY",
            #             "TECH_LEVEL", "DIVINE_SHIELD", "TAUNT", "POISONOUS", "WINDFURY",
            #             "REBORN", "ELITE", "FROZEN", "LINKED_ENTITY", "CREATOR", "STEALTH", "EXHAUSTED",
            #             "DEATHRATTLE", "ATTACHED", "PLAYER_LEADERBOARD_PLACE"]
            # # GameTag.
            # for gametag in gametags:
            #     if GameTag[gametag].value in self.entities[entity_id]:
            #         print(f"{gametag}:{self.entities[entity_id][GameTag[gametag].value]}", end=" | ")
            # print()



            if cardtype == CardType.MINION.value:

                health = 0
                attack = 0
                pos = 0
                if GameTag['HEALTH'].value in self.entities[entity_id]:
                    health = self.entities[entity_id][GameTag['HEALTH'].value]
                if GameTag['ATK'].value in self.entities[entity_id]:
                    attack = self.entities[entity_id][GameTag['ATK'].value]
                if GameTag['ZONE_POSITION'].value in self.entities[entity_id]:
                    pos = self.entities[entity_id][GameTag['ZONE_POSITION'].value]
                print(f"{entity_id} - {attack}/{health} {card_name}, CardType: {CardType(cardtype).name} Pos: {pos}")
                if card_name == '변신수 제루스':
                    for tag, value in self.entities[entity_id].items():
                        if tag in GameTag.__members__.values():
                            tag = GameTag(tag).name
                        print(f"    TAG: {tag}, VALUE: {value}")



            if cardtype == CardType.HERO_POWER.value:
                print(f"{entity_id} - {card_name}, CardType: {CardType(cardtype).name}")

                for tag, value in self.entities[entity_id].items():
                    if tag in GameTag.__members__.values():
                        tag = GameTag(tag).name
                        # if tag in ['COST', 'HEALTH', 'ATK', 'ZONE', 'ENTITY_ID', 'TAUNT', 'DIVINE_SHIELD', 'ZONE_POSITION', 'EXHAUSTED',
                        #            'RARITY', 'TAG_LAST_KNOWN_COST_IN_HAND', 'CREATOR_DBID', 'TECH_LEVEL', 'CANT_ATTACK', 'CREATOR',
                        #            'IS_BACON_POOL_MINION', 'NUM_TURNS_IN_PLAY', 'JUST_PLAYED', 'BATTLECRY', 'CARDRACE', 'FACTION' ,
                        #            'TRIGGER_VISUAL', 'DEATHRATTLE', 'CARDTYPE', 'ELITE', 'REBORN', 'FROZEN', 'BACON_MINION_IS_LEVEL_TWO', 'PREMIUM',
                        #            'OVERKILL', 'HIDE_WATERMARK', 'HIDE_COST', 'DISCOVER', 'CHARGE', 'POISONOUS', 'CARD_TARGET',
                        #            'WINDFURY', 'USE_DISCOVER_VISUALS', 'MODULAR', 'CardID', 'HERO_POWER', 'PLAYER_TECH_LEVEL', 'BACON_HERO_CAN_BE_DRAFTED']:
                        #     continue
                    if tag == 'CardID':
                        continue
                    print(f"    TAG: {tag}, VALUE: {value}")


            if cardtype == CardType.HERO.value:
                health = 0
                tech_level = 1

                if GameTag['HEALTH'].value in self.entities[entity_id]:
                    health = self.entities[entity_id][GameTag['HEALTH'].value]
                if GameTag['PLAYER_TECH_LEVEL'].value in self.entities[entity_id]:
                    tech_level = self.entities[entity_id][GameTag['PLAYER_TECH_LEVEL'].value]

                print(f"{entity_id} - {card_name}, HP: {health}, tech_level: {tech_level}, CardType: {CardType(cardtype).name}")

                # for tag, value in self.entities[entity_id].items():
                #     if tag in GameTag.__members__.values():
                #         tag = GameTag(tag).name
                #         if tag in ['COST', 'HEALTH', 'ATK', 'ZONE', 'ENTITY_ID', 'TAUNT', 'DIVINE_SHIELD', 'ZONE_POSITION', 'EXHAUSTED',
                #                    'RARITY', 'TAG_LAST_KNOWN_COST_IN_HAND', 'CREATOR_DBID', 'TECH_LEVEL', 'CANT_ATTACK', 'CREATOR',
                #                    'IS_BACON_POOL_MINION', 'NUM_TURNS_IN_PLAY', 'JUST_PLAYED', 'BATTLECRY', 'CARDRACE', 'FACTION' ,
                #                    'TRIGGER_VISUAL', 'DEATHRATTLE', 'CARDTYPE', 'ELITE', 'REBORN', 'FROZEN', 'BACON_MINION_IS_LEVEL_TWO', 'PREMIUM',
                #                    'OVERKILL', 'HIDE_WATERMARK', 'HIDE_COST', 'DISCOVER', 'CHARGE', 'POISONOUS', 'CARD_TARGET',
                #                    'WINDFURY', 'USE_DISCOVER_VISUALS', 'MODULAR', 'CardID', 'HERO_POWER', 'PLAYER_TECH_LEVEL', 'BACON_HERO_CAN_BE_DRAFTED']:
                #             continue
                #     if tag == 'CardID':
                #         continue
                #     print(f"    TAG: {tag}, VALUE: {value}")
                # no_tags = ['CONTROLLER', 'COST', 'HEALTH', 'ATK', 'ZONE', 'ENTITY_ID', 'TAUNT', 'DIVINE_SHIELD', 'ZONE_POSITION', 'EXHAUSTED',
                #            'RARITY', 'TAG_LAST_KNOWN_COST_IN_HAND', 'CREATOR_DBID', 'TECH_LEVEL', 'CANT_ATTACK', 'CREATOR',
                #            'IS_BACON_POOL_MINION', 'NUM_TURNS_IN_PLAY', 'JUST_PLAYED', 'BATTLECRY', 'CARDRACE', 'FACTION' ,
                #            'TRIGGER_VISUAL', 'DEATHRATTLE', 'CARDTYPE', 'ELITE', 'REBORN', 'FROZEN', 'BACON_MINION_IS_LEVEL_TWO', 'PREMIUM',
                #            'OVERKILL', 'HIDE_WATERMARK', 'HIDE_COST', 'DISCOVER', 'CHARGE', 'POISONOUS', 'CARD_TARGET',
                #            'WINDFURY', 'USE_DISCOVER_VISUALS', 'MODULAR', 'hi', 'lo', 'HERO_POWER', 'PLAYER_TECH_LEVEL', 'BACON_HERO_CAN_BE_DRAFTED',
                #             'MAXHANDSIZE', 'STARTHANDSIZE', 'CANT_DRAW',
                #            'OVERRIDE_EMOTE_0', 'OVERRIDE_EMOTE_1', 'OVERRIDE_EMOTE_2', 'OVERRIDE_EMOTE_3', 'OVERRIDE_EMOTE_4', 'OVERRIDE_EMOTE_5',
                #            'NUM_FRIENDLY_MINIONS_THAT_ATTACKED_THIS_TURN', 'NUM_MINIONS_PLAYER_KILLED_THIS_TURN', 'NUM_FRIENDLY_MINIONS_THAT_DIED_THIS_TURN',
                #            'NUM_FRIENDLY_MINIONS_THAT_DIED_THIS_GAME', 'BATTLEGROUNDS_PREMIUM_EMOTES', 'COMBO_ACTIVE', 'RESOURCES', 'RESOURCES_USED', 'MAXRESOURCES']
                # if self.entities[entity_id][GameTag.CONTROLLER] == self.entities[self.player_me]['PlayerID']:
                #     print("--player_me--")
                #     for tag, value in self.entities[self.player_me].items():
                #         if tag in GameTag.__members__.values():
                #             tag = GameTag(tag).name
                #             if tag in no_tags:
                #                 continue
                #         print(f"    TAG: {tag}, VALUE: {value}")
                # else:
                #     print("--player other--")
                #     for tag, value in self.entities[self.player_other].items():
                #         if tag in GameTag.__members__.values():
                #             tag = GameTag(tag).name
                #             if tag in no_tags:
                #                 continue
                #         print(f"    TAG: {tag}, VALUE: {value}")




        # if cardtype == CardType.ENCHANTMENT.value and zone == Zone.PLAY.value:
        #     if not GameTag["ATTACHED"].value in self.entities[entity_id]:
        #         return
        #     attached_id = self.entities[entity_id][GameTag["ATTACHED"].value]
        #
        #     if attached_id not in self.entities:
        #         return
        #     if self.entities[attached_id][GameTag.ZONE.value] != Zone.PLAY.value:
        #         return
        #     if self.entities[attached_id][GameTag.CARDTYPE.value] != CardType.MINION.value:
        #         return
            # is_entity_tag_value = False
            # for tag, value in self.entities[entity_id].items():
            #     if tag in GameTag.__members__.values():
            #         tag = GameTag(tag).name
            #         if tag in ['ZONE', 'ENTITY_ID', 'CARDTYPE', 'ZONE_POSITION', 'CONTROLLER', 'CREATOR_DBID', 'TAG_LAST_KNOWN_COST_IN_HAND',
            #                    ]:
            #             continue
            #         if tag == 'DAMAGE' and value == 0:
            #             continue
            #         if tag in ['CREATOR', ]:
            #             continue
            #         if tag == 'ATTACHED':
            #             att_card_name = card_name_by_id(self.entities[attached_id]['CardID'])
            #             print(f'↓ Attached minion: {att_card_name}')
            #
            #
            #         if card_name == '연마된 무기' and tag == 'TAG_SCRIPT_DATA_NUM_1':
            #             continue
            #
            #         # if tag ==  and value != 0:
            #         print(f"TAG: {tag}, VALUE: {value}")
            #         is_entity_tag_value = True
            # # if is_entity_tag_value:
            # print(f"↑{entity_id} - Name: {card_name}, Zone: {Zone(zone).name}, CardType: {CardType(cardtype).name}")
            # print()



        #     if cardtype == CardType.MINION.value or cardtype == CardType.HERO_POWER.value:
        #         is_entity_tag_value = False
        #         for tag, value in self.entities[entity_id].items():
        #             if tag in GameTag.__members__.values():
        #                 tag = GameTag(tag).name
        #                 if tag in ['CONTROLLER', 'COST', 'HEALTH', 'ATK', 'ZONE', 'ENTITY_ID', 'TAUNT', 'DIVINE_SHIELD', 'ZONE_POSITION', 'EXHAUSTED',
        #                            'RARITY', 'TAG_LAST_KNOWN_COST_IN_HAND', 'CREATOR_DBID', 'TECH_LEVEL', 'CANT_ATTACK', 'CREATOR',
        #                            'IS_BACON_POOL_MINION', 'NUM_TURNS_IN_PLAY', 'JUST_PLAYED', 'BATTLECRY', 'CARDRACE', 'FACTION' ,
        #                            'TRIGGER_VISUAL', 'DEATHRATTLE', 'CARDTYPE', 'ELITE', 'REBORN', 'FROZEN', 'BACON_MINION_IS_LEVEL_TWO', 'PREMIUM',
        #                            'OVERKILL', 'HIDE_WATERMARK', 'HIDE_COST', 'DISCOVER', 'CHARGE', 'POISONOUS', 'CARD_TARGET',
        #                            'WINDFURY', 'USE_DISCOVER_VISUALS', 'MODULAR', 'TAG_SCRIPT_DATA_NUM_1']:
        #                     continue
        #                 if (tag == 'TAG_SCRIPT_DATA_NUM_1' and card_name == '내가 가져야겠어!') or\
        #                     (tag == 'TAG_SCRIPT_DATA_NUM_2' and card_name == '새끼 붉은용') or\
        #                     (tag == 'START_OF_COMBAT' and card_name == '새끼 붉은용'):
        #
        #                     continue
        #                 if tag == 'SPAWN_TIME_COUNT' and value == 1:
        #                     continue
        #                 if tag == 'POWERED_UP' and value == 0:
        #                     continue
        #                 print(f"TAG: {tag}, VALUE: {value}")
        #                 is_entity_tag_value = True
        #         if is_entity_tag_value:
        #             print(f"↑{entity_id} - Name: {card_name}, Zone: {Zone(zone).name}, CardType: {CardType(cardtype).name}")
        #
        #     if cardtype == CardType.MINION.value or cardtype == CardType.HERO_POWER.value:
        #         is_entity_tag_value = False
        #         for tag, value in self.entities[entity_id].items():
        #             if tag in GameTag.__members__.values():
        #                 tag = GameTag(tag).name
        #                 if tag in ['CONTROLLER', 'COST', 'HEALTH', 'ATK', 'ZONE', 'ENTITY_ID', 'TAUNT', 'DIVINE_SHIELD', 'ZONE_POSITION', 'EXHAUSTED',
        #                            'RARITY', 'TAG_LAST_KNOWN_COST_IN_HAND', 'CREATOR_DBID', 'TECH_LEVEL', 'CANT_ATTACK', 'CREATOR',
        #                            'IS_BACON_POOL_MINION', 'NUM_TURNS_IN_PLAY', 'JUST_PLAYED', 'BATTLECRY', 'CARDRACE', 'FACTION' ,
        #                            'TRIGGER_VISUAL', 'DEATHRATTLE', 'CARDTYPE', 'ELITE', 'REBORN', 'FROZEN', 'BACON_MINION_IS_LEVEL_TWO', 'PREMIUM',
        #                            'OVERKILL', 'HIDE_WATERMARK', 'HIDE_COST', 'DISCOVER', 'CHARGE', 'POISONOUS', 'CARD_TARGET',
        #                            'WINDFURY', 'USE_DISCOVER_VISUALS', 'MODULAR', 'TAG_SCRIPT_DATA_NUM_1']:
        #                     continue
        #                 if (tag == 'TAG_SCRIPT_DATA_NUM_1' and card_name == '내가 가져야겠어!') or\
        #                     (tag == 'TAG_SCRIPT_DATA_NUM_2' and card_name == '새끼 붉은용') or\
        #                     (tag == 'START_OF_COMBAT' and card_name == '새끼 붉은용'):
        #
        #                     continue
        #                 if tag == 'SPAWN_TIME_COUNT' and value == 1:
        #                     continue
        #                 if tag == 'POWERED_UP' and value == 0:
        #                     continue
        #                 print(f"TAG: {tag}, VALUE: {value}")
        #                 is_entity_tag_value = True
        #         if is_entity_tag_value:
        #             print(f"↑{entity_id} - Name: {card_name}, Zone: {Zone(zone).name}, CardType: {CardType(cardtype).name}")
        #
        #

    def print_entities_pretty(self):
        for entity_id in self.entities.keys():
            self.print_entity_pretty(entity_id)

    def create_game_handler(self, level):
        self.create_game_num += 1

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
                if not self.player_me:
                    self.player_me = entity_id
                else:
                    self.player_other = entity_id
            elif TAG_VALUE_RE.match(text):
                tag, value = TAG_VALUE_RE.match(text).group("tag", "value")
                tag, value = HSGame.tag_value_to_int(tag, value)
                self.entities[entity_id][tag] = value

    def get_entity_id_by_entity(self, entity):
        if ENTITY_DESCRIPTION_RE.match(entity):
            entity_id = int(ENTITY_DESCRIPTION_RE.match(entity).group("id"))
        elif entity.isdigit():
            entity_id = int(entity)
        elif entity in self.entity_names:
            entity_id = self.entity_names[entity]
        else:
            entity_id = self.player_other
        return entity_id

    def block_handler(self, level):
        self.block_num += 1
        # print(f"{self.block_num}: {self.contexts[level][0]}")
        text = self.contexts[level][0].strip()
        match_data = BLOCK_START_ENTITY_RE.match(text)

        blocktype = match_data.group("BlockType")
        entity_id = self.get_entity_id_by_entity(match_data.group("Entity"))
        self.is_hero_contain[level] = False

        line_num = len(self.contexts[level])
        for i in range(1, line_num - 1):
            self.entity_parser(self.contexts[level][i], level + 1)
        if self.contexts[level][line_num - 1].split()[0] != "BLOCK_END":
            self.entity_parser(self.contexts[level][line_num - 1], level + 1)
            # self.entity_parser((" "*4*level) + "BLOCK_END", level + 1)
        self.call_handler(level + 1)


        if blocktype == "TRIGGER" and entity_id == self.baconshop8playerenchant:
            if self.is_hero_contain[level]:
                print('-' * 50)
                self.game_turn = self.entities[self.game_entity][GameTag.TURN.value]

                print(f"{' ' * 20}BATTLE{self.game_turn // 2}{' ' * 20}")
                self.print_entities_pretty()
                print('-' * 50)

                self.battle_start.emit(self.game_turn // 2)
        # if blocktype == "TRIGGER":
        #     for word in text.split():
        #         idx = word.find('TriggerKeyword=')
        #         if idx == -1:
        #             continue
        #         tkeyword = word[idx+len('TriggerKeyword='):]
        #         self.trigger_keywords.add(tkeyword)
        #         if tkeyword == 'DEATHRATTLE':
        #             print(f"""Deathrattle by {card_name_by_id(self.entities[entity_id]['CardID'])}@{entity_id}""")



    def full_entity_handler(self, level):
        self.full_entity_num += 1

        text = self.contexts[level][0].strip()

        if not FULL_ENTITY_CREATING_RE.match(text):
            logging.error(f"full_entity_handler Error - FULL_ENTITY: {text}")
            return
        entity_id, card_id = FULL_ENTITY_CREATING_RE.match(text).group("ID", "CardID")
        entity_id = int(entity_id)
        self.entities[entity_id] = {}
        self.entities[entity_id]["CardID"] = card_id

        bob_names = [
            "Bobs Gasthaus",
            "Bob's Tavern",
            "Taberna de Bob",
            "Taberna de Bob",
            "Taverne de Bob",
            "Locanda di Bob",
            "ボブの酒場",
            "밥의 선술집",
            "Karczma Boba",
            "Taverna do Bob",
            "Таверна Боба",
            "โรงเตี๊ยมของบ็อบ",
            "鲍勃的酒馆",
            "鮑伯的旅店",
        ]

        if card_id == "TB_BaconShopBob":
            for bob_name in bob_names:
                self.entity_names[bob_name] = entity_id

        if card_id == "TB_BaconShop_8P_PlayerE":
            self.baconshop8playerenchant = entity_id

        for text in self.contexts[level][1:]:
            text = text.lstrip()
            if TAG_VALUE_RE.match(text):
                tag, value = TAG_VALUE_RE.match(text).group("tag", "value")
                tag, value = HSGame.tag_value_to_int(tag, value)
                self.entities[entity_id][tag] = value
            else:
                logging.error(f"full_entity_handler Error - tag/value: {text}")

        self.activate_game(entity_id)

        if self.entities[entity_id]["CardID"].upper().find('HERO') != -1:
            self.is_hero_contain[level - 1] = True
        return

    def tag_change_handler(self, level):
        self.tag_change_num += 1

        if len(self.contexts[level]) != 1:
            logging.error(f"tag_change_handler Error - self.contexts too long: {self.contexts[level]}")
            return
        text = self.contexts[level][0].strip()
        match_data = TAG_CHANGE_RE.match(text)
        if not match_data:
            logging.error(f"tag_change_handler Error - match error: {text}")
            return

        entity = match_data.group("Entity")
        tag = match_data.group("tag")
        value = match_data.group("value")
        entity_id = self.get_entity_id_by_entity(entity)

        prevalue = self.entities[entity_id].get(tag, 0)

        tag, value = self.tag_value_to_int(tag, value)
        self.entities[entity_id][tag] = value

        self.activate_game(entity_id)

        if entity_id == self.game_entity and tag == GameTag.PROPOSED_ATTACKER:

            if not value:
                return
            print('.'*50)
            print(f"""{Util.card_name_by_id(self.entities[value]['CardID'])}@{value} -> """, end='')

        if entity_id == self.game_entity and tag == GameTag.PROPOSED_DEFENDER:
            if not value:
                return
            print(f"""{Util.card_name_by_id(self.entities[value]['CardID'])}@{value}""")

        if tag == GameTag.DAMAGE:
            if not value:
                return
            if self.entities[entity_id][GameTag.ZONE] == Zone.PLAY and self.entities[entity_id][GameTag.CARDTYPE] == CardType.MINION:
                print(f"""{Util.card_name_by_id(self.entities[entity_id]['CardID'])}@{entity_id} damaged {value - prevalue}""")

    def show_entity_handler(self, level):
        self.show_entity_num += 1

        text = self.contexts[level][0].strip()

        if not SHOW_ENTITY_RE.match(text):
            logging.error(f"show_entity_handler Error - SHOW_ENTITY: {text}")
            return
        entity, card_id = SHOW_ENTITY_RE.match(text).group("Entity", "CardID")

        entity_id = self.get_entity_id_by_entity(entity)
        if card_id:
            self.entities[entity_id]['CardID'] = card_id

        for text in self.contexts[level][1:]:
            text = text.lstrip()
            if TAG_VALUE_RE.match(text):
                tag, value = TAG_VALUE_RE.match(text).group("tag", "value")
                tag, value = HSGame.tag_value_to_int(tag, value)
                self.entities[entity_id][tag] = value
            else:
                logging.error(f"show_entity_handler Error - tag/value: {text}")

        self.activate_game(entity_id)

    def hide_entity_handler(self, level):
        self.hide_entity_num += 1

        text = self.contexts[level][0].strip()

        if not HIDE_ENTITY_RE.match(text):
            logging.error(f"hide_entity_handler Error - HIDE_ENTITY: {text}")
            return
        entity, tag, value = HIDE_ENTITY_RE.match(text).group("Entity", "tag", "value")

        entity_id = self.get_entity_id_by_entity(entity)
        tag, value = self.tag_value_to_int(tag, value)
        self.entities[entity_id][tag] = value

        self.activate_game(entity_id)

    def meta_data_handler(self, level):
        self.meta_data_num += 1
        pass

    def change_entity_handler(self, level):
        self.change_entity_num += 1

        text = self.contexts[level][0].strip()

        if not CHANGE_ENTITY_RE.match(text):
            logging.error(f"change_entity_handler Error - CHANGE_ENTITY: {text}")
            return
        entity, card_id = CHANGE_ENTITY_RE.match(text).group("Entity", "CardID")

        entity_id = self.get_entity_id_by_entity(entity)

        for text in self.contexts[level][1:]:
            text = text.lstrip()
            if TAG_VALUE_RE.match(text):
                tag, value = TAG_VALUE_RE.match(text).group("tag", "value")
                tag, value = HSGame.tag_value_to_int(tag, value)
                self.entities[entity_id][tag] = value
            else:
                logging.error(f"change_entity_handler Error - tag/value: {text}")

        self.activate_game(entity_id)

    def sub_spell_handler(self, level):
        self.sub_spell_num += 1

        line_num = len(self.contexts[level])
        for i in range(1, line_num - 1):
            if self.contexts[level][i].lstrip().startswith("Source") \
                    or self.contexts[level][i].lstrip().startswith("Targets"):
                continue
            self.entity_parser(self.contexts[level][i], level + 1)
        if self.contexts[level][line_num - 1].split()[0] != "SUB_SPELL_END" and \
                not (self.contexts[level][line_num - 1].lstrip().startswith("Source")
                     or self.contexts[level][line_num - 1].lstrip().startswith("Targets")):
            self.entity_parser(self.contexts[level][line_num - 1], level + 1)
            # self.entity_parser((" "*4*level) + "SUB_SPELL_END", level + 1)
        self.call_handler(level + 1)

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
                logging.error(f"call_handler() error: {self.contexts[i]}")
                raise NotImplementedError
            del self.contexts[i]

    def entity_parser(self, context, level=0):
        context_level = (len(context) - len(context.lstrip())) // 4
        if context_level > level:
            self.contexts[level].append(context)
            return
        words = context.split()
        if words[0] == "BLOCK_END" or words[0] == "SUB_SPELL_END":
            if level < len(self.contexts):
                self.contexts[level].append(context)
                self.call_handler(level)
        elif words[0] == "CREATE_GAME" or words[0] == "BLOCK_START" or words[0] == "FULL_ENTITY" or words[
            0] == "CHANGE_ENTITY" \
                or words[0] == "SHOW_ENTITY" or words[0] == "META_DATA" or words[0] == "SUB_SPELL_START":
            self.call_handler(context_level)
            if len(self.contexts) != level:
                logging.error(f"entity_parser()  error: level not correct")
                raise IndexError
            self.contexts.append(list())
            self.contexts[level].append(context)
        elif words[0] == "TAG_CHANGE" or words[0] == "HIDE_ENTITY":
            self.call_handler(level)
            self.contexts.append(list())
            self.contexts[level].append(context)
            self.call_handler(level)
        else:
            logging.error(f"entity_parser() error: unknown entity type: {words[0]}")
        return

    def line_parser(self, line):
        if GAME_STATE_DEBUG_PRINT_POWER_RE.match(line):
            self.debug_print_line_num += 1
            self.entity_parser(GAME_STATE_DEBUG_PRINT_POWER_RE.match(line).group("context"))
            GameStateDebugPrintPowerTXT.write(GAME_STATE_DEBUG_PRINT_POWER_RE.match(line).group("context"))
            GameStateDebugPrintPowerTXT.write('\n')
        elif GAME_STATE_DEBUG_PRINT_POWER_LIST_RE.match(line):
            pass
        elif GAME_STATE_DEBUG_PRINT_GAME_RE.match(line):
            self.print_game_parser(GAME_STATE_DEBUG_PRINT_GAME_RE.match(line).group("context"))
            GameStateDebugPrintGameTXT.write(GAME_STATE_DEBUG_PRINT_GAME_RE.match(line).group("context"))
            GameStateDebugPrintGameTXT.write('\n')
        elif POWER_TASK_LIST_DEBUG_DUMP_RE.match(line):
            pass
        elif POWER_TASK_LIST_DEBUG_PRINT_POWER_RE.match(line):
            PowerTaskListDebugPrintPowerTXT.write(POWER_TASK_LIST_DEBUG_PRINT_POWER_RE.match(line).group("context"))
            PowerTaskListDebugPrintPowerTXT.write('\n')
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
                logging.warning(
                    f"line_parser() warning - line break - Line: {line.rstrip()}, New Line: {new_line.rstrip()}")
                self.line_parser(new_line)
            else:
                logging.error(f"line_parser() error - Line: {line}")
        self.recent_parsing_line = line.rstrip()

    def print_game_parser(self, context):

        if BUILD_NUMBER_RE.match(context):
            self.build_number = int(BUILD_NUMBER_RE.match(context).group("BuildNumber"))
            if self.build_number != HS_BUILD_NUMBER:
                logging.warning(f"Build number NOT correct, Program: {HS_BUILD_NUMBER}, Log File: {self.build_number}")
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
    log_file_2020_02_05_22_51_53 = open(os.path.join(HS_LOG_FILE_DIR, "2020-02-05 22-51-53.log"), 'r', encoding="UTF8")
    log_file_2020_02_29_12_56_31 = open(os.path.join(HS_LOG_FILE_DIR, "2020-02-29 12-56-31.log"), 'r', encoding="UTF8")
    log_file_2020_02_29_20_44_13 = open(os.path.join(HS_LOG_FILE_DIR, "2020-02-29 20-44-13.log"), 'r', encoding="UTF8")
    log_file_2020_02_29_21_06_42 = open(os.path.join(HS_LOG_FILE_DIR, "2020-02-29 21-06-42.log"), 'r', encoding="UTF8")
    log_file_2020_03_01_21_19_18 = open(os.path.join(HS_LOG_FILE_DIR, "2020-03-01 21-19-18.log"), 'r', encoding="UTF8")
    log_file_2020_03_01_21_06_47 = open(os.path.join(HS_LOG_FILE_DIR, "2020-03-01 21-06-47.log"), 'r', encoding="UTF8")
    log_file_2020_03_21_23_33_29 = open(os.path.join(HS_LOG_FILE_DIR, "2020-03-21 23-33-29.log"), 'r', encoding="UTF8")
    log_file_2020_03_29_20_39_42 = open(os.path.join(HS_LOG_FILE_DIR, "2020-03-29 20-39-42.log"), 'r', encoding="UTF8")
    log_file_2020_03_29_22_38_02 = open(os.path.join(HS_LOG_FILE_DIR, "2020-03-29 22-38-02.log"), 'r', encoding="UTF8")
    log_file_2020_03_29_21_47_06 = open(os.path.join(HS_LOG_FILE_DIR, "2020-03-31 21-47-06.log"), 'r', encoding="UTF8")

    # # game = HSGame(log_file_2020_02_05_22_51_53)
    # # game.line_reader()
    # #
    # # game = HSGame(log_file_2020_02_29_12_56_31)
    # # game.line_reader()
    #
    # game = HSGame(log_file_2020_02_29_20_44_13)
    # game.line_reader()
    #
    #
    # game = HSGame(log_file_2020_02_29_21_06_42)
    # game.line_reader()

    # game = HSGame(log_file_2020_03_01_21_19_18)
    # game.line_reader()
    #
    # game = HSGame(log_file_2020_03_01_21_06_47)
    # game.line_reader()
    #
    #
    # game = HSGame(log_file_2020_03_21_23_33_29)
    # game.line_reader()

    game = HSGame(log_file_2020_03_29_20_39_42)
    game.line_reader()

    # *******************
    # game = HSGame(log_file_2020_03_29_22_38_02)
    # game.line_reader()

    game = HSGame(log_file_2020_03_29_21_47_06)
    game.line_reader()
    #
    # game = HSGame(open(os.path.join(HS_LOG_FILE_DIR, "2020-03-31 21-47-06.log"), 'r', encoding="UTF8"))
    # game.line_reader()


    # triggerkeyword_set = set()

    # while True:
    #     line = log_file_2020_03_29_21_47_06.readline()
    #     if not line:
    #         break
    #     words = line.split()
    #     for word in words:
    #         if word.startswith('TriggerKeyword'):
    #             triggerkeyword_set.add(word)
    #
    # print(triggerkeyword_set)

    #
    # game = HSGame(log_file_power_new)
    # game.line_reader()

    # game = HSGame(log_file_2020_03_01_21_19_18)
    # game.line_reader()

    # HSGame(log_file_2020_03_01_21_19_18)
    # HSGame(log_file_2020_03_01_21_19_18)
    # HSGame(hs_log_file)
    # HSGame(real_log_file)
