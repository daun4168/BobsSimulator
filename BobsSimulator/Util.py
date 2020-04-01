import xmltodict
import json
import random
from typing import Dict, Optional, List
from collections import defaultdict

from BobsSimulator.HSLogging import main_logger
from BobsSimulator.Main import VERSION_NUMBER, LOCALE
from BobsSimulator.HSType import GameTag, CardType, Faction, Race, Rarity, Zone, Mulligan, Step, State, CardClass, PlayState, Minion
import hearthstone_data

# carddefs_path = 'res/CardDefs.xml'
# carddefs_version = 43246

class Util:
    card_dict = {}  # type: Dict[str, Dict]
    enum_id_to_card_id_dict = {}  # type: Dict
    bp_cost_dict = defaultdict(list)  # type: Dict[int, List[str]]
    bp_tech_dict = defaultdict(list)  # type: Dict[int, List[str]]
    bp_race_dict = defaultdict(list)  # type: Dict[Race, List[str]]
    bp_elite_list = []
    bp_deathrattle_list = []
    bp_minion_list = []

    @classmethod
    def init_util(cls):
        cls._init_card_name_dict()
        cls._init_random_list()

    @classmethod
    def _init_card_name_dict(cls):
        carddefs_path = hearthstone_data.get_carddefs_path()
        carddefs_version = int(float(hearthstone_data.__version__))

        if VERSION_NUMBER != carddefs_version:
            main_logger.warning(f"Build number NOT correct, Program: {VERSION_NUMBER}, CardDefs: {carddefs_version}")

        card_defs = open(carddefs_path, 'r', encoding='UTF8')
        xml_card_dict = xmltodict.parse(card_defs.read())
        card_defs.close()

        xml_card_dict = json.dumps(xml_card_dict)
        xml_card_dict = json.loads(xml_card_dict)

        lang_list = [
            'koKR',
            'enUS',
        ]

        card_data_list = xml_card_dict["CardDefs"]["Entity"]
        for card_data in card_data_list:
            card_id = card_data["@CardID"]
            enum_id = int(card_data["@ID"])
            cls.enum_id_to_card_id_dict[enum_id] = card_id
            cls.card_dict[card_id] = {}
            for lang in lang_list:
                cls.card_dict[card_id][lang] = card_data['Tag'][0][lang]
            tag_value_list = card_data['Tag']
            for tag_value_dict in tag_value_list:
                if '@value' in tag_value_dict and '@type' in tag_value_dict and tag_value_dict['@type'] == 'Int':
                    if '@enumID' in tag_value_dict:
                        Util.card_dict[card_id][int(tag_value_dict['@enumID'])] = int(tag_value_dict['@value'])

    @classmethod
    def _init_random_list(cls):
        for card_id, tag_value_dict in cls.card_dict.items():
            if GameTag.IS_BACON_POOL_MINION in tag_value_dict and tag_value_dict[GameTag.IS_BACON_POOL_MINION]:
                cls.bp_minion_list.append(card_id)
                if GameTag.COST in tag_value_dict:
                    cost = tag_value_dict[GameTag.COST]
                    cls.bp_cost_dict[cost].append(card_id)
                if GameTag.TECH_LEVEL in tag_value_dict:
                    tech = tag_value_dict[GameTag.TECH_LEVEL]
                    cls.bp_tech_dict[tech].append(card_id)
                if GameTag.CARDRACE in tag_value_dict:
                    race = Race(tag_value_dict[GameTag.CARDRACE])
                    cls.bp_race_dict[race].append(card_id)
                    if race == Race.ALL:
                        cls.bp_race_dict[Race.ELEMENTAL].append(card_id)
                        cls.bp_race_dict[Race.MECHANICAL].append(card_id)
                        cls.bp_race_dict[Race.DEMON].append(card_id)
                        cls.bp_race_dict[Race.MURLOC].append(card_id)
                        cls.bp_race_dict[Race.DRAGON].append(card_id)
                        cls.bp_race_dict[Race.BEAST].append(card_id)
                        cls.bp_race_dict[Race.PIRATE].append(card_id)
                        cls.bp_race_dict[Race.TOTEM].append(card_id)
                if GameTag.ELITE in tag_value_dict and tag_value_dict[GameTag.ELITE]:
                    cls.bp_elite_list.append(card_id)
                if GameTag.DEATHRATTLE in tag_value_dict and tag_value_dict[GameTag.DEATHRATTLE]:
                    cls.bp_deathrattle_list.append(card_id)

    @classmethod
    def default_value_by_id(cls, card_id: str, tag: GameTag):
        if card_id not in cls.card_dict:
            return None
        if tag not in cls.card_dict[card_id]:
            return None
        return cls.card_dict[card_id][tag]

    @classmethod
    def default_health_by_id(cls, card_id) -> int:
        value = cls.default_value_by_id(card_id, GameTag.HEALTH)
        if value:
            return value
        else:
            return 0

    @classmethod
    def default_attack_by_id(cls, card_id) -> int:
        value = cls.default_value_by_id(card_id, GameTag.ATK)
        if value:
            return value
        else:
            return 0

    @classmethod
    def card_name_by_id(cls, card_id, locale=LOCALE) -> str:
        if not card_id:
            return ""
        return cls.card_dict[card_id][locale]

    @classmethod
    def random_bp_minion_cost(cls, cost: int) -> Optional[Minion]:
        try:
            card_id = random.choice(cls.bp_cost_dict[cost])
        except IndexError:
            return None
        return cls.make_default_minion(card_id)

    @classmethod
    def random_bp_minion_tech(cls, tech: int) -> Optional[Minion]:
        try:
            card_id = random.choice(cls.bp_tech_dict[tech])
        except IndexError:
            return None
        return cls.make_default_minion(card_id)

    @classmethod
    def random_bp_minion_race(cls, race: Race) -> Minion:
        card_id = random.choice(cls.bp_race_dict[race])
        return cls.make_default_minion(card_id)

    @classmethod
    def random_bp_minion_elite(cls) -> Minion:
        card_id = random.choice(cls.bp_elite_list)
        return cls.make_default_minion(card_id)

    @classmethod
    def random_bp_minion_deathrattle(cls) -> Minion:
        card_id = random.choice(cls.bp_deathrattle_list)
        return cls.make_default_minion(card_id)

    @classmethod
    def random_bp_minion(cls) -> Minion:
        card_id = random.choice(cls.bp_minion_list)
        return cls.make_default_minion(card_id)

    @classmethod
    def make_default_minion(cls, card_id) -> Minion:
        minion = Minion()
        minion.card_id = card_id
        if GameTag["PREMIUM"].value in cls.card_dict[card_id]:
            minion.golden = bool(cls.card_dict[card_id][GameTag["PREMIUM"].value])
        if GameTag["BACON_MINION_IS_LEVEL_TWO"].value in cls.card_dict[card_id]:
            minion.level2 = bool(cls.card_dict[card_id][GameTag["BACON_MINION_IS_LEVEL_TWO"].value])
        if GameTag["ELITE"].value in cls.card_dict[card_id]:
            minion.elite = bool(cls.card_dict[card_id][GameTag["ELITE"].value])
        if GameTag["TECH_LEVEL"].value in cls.card_dict[card_id]:
            minion.tech_level = cls.card_dict[card_id][GameTag["TECH_LEVEL"].value]
        if GameTag["EXHAUSTED"].value in cls.card_dict[card_id]:
            minion.exhausted = bool(cls.card_dict[card_id][GameTag["EXHAUSTED"].value])
        if GameTag["COST"].value in cls.card_dict[card_id]:
            minion.cost = cls.card_dict[card_id][GameTag["COST"].value]
        if GameTag["ATK"].value in cls.card_dict[card_id]:
            minion.attack = cls.card_dict[card_id][GameTag["ATK"].value]
        if GameTag["HEALTH"].value in cls.card_dict[card_id]:
            minion.health = cls.card_dict[card_id][GameTag["HEALTH"].value]
        if GameTag["DAMAGE"].value in cls.card_dict[card_id]:
            minion.damage = cls.card_dict[card_id][GameTag["DAMAGE"].value]
        if GameTag["TAUNT"].value in cls.card_dict[card_id]:
            minion.taunt = bool(cls.card_dict[card_id][GameTag["TAUNT"].value])
        if GameTag["DIVINE_SHIELD"].value in cls.card_dict[card_id]:
            minion.divine_shield = bool(cls.card_dict[card_id][GameTag["DIVINE_SHIELD"].value])
        if GameTag["POISONOUS"].value in cls.card_dict[card_id]:
            minion.poisonous = bool(cls.card_dict[card_id][GameTag["POISONOUS"].value])
        if GameTag["WINDFURY"].value in cls.card_dict[card_id]:
            minion.windfury = int(cls.card_dict[card_id][GameTag["WINDFURY"].value])
        if GameTag["REBORN"].value in cls.card_dict[card_id]:
            minion.reborn = bool(cls.card_dict[card_id][GameTag["REBORN"].value])
        if GameTag["DEATHRATTLE"].value in cls.card_dict[card_id]:
            minion.deathrattle = bool(cls.card_dict[card_id][GameTag["DEATHRATTLE"].value])
        if GameTag["AURA"].value in cls.card_dict[card_id]:
            minion.aura = bool(cls.card_dict[card_id][GameTag["AURA"].value])
        if GameTag["START_OF_COMBAT"].value in cls.card_dict[card_id]:
            minion.start_of_combat = bool(cls.card_dict[card_id][GameTag["START_OF_COMBAT"].value])
        if GameTag["OVERKILL"].value in cls.card_dict[card_id]:
            minion.overkill = bool(cls.card_dict[card_id][GameTag["OVERKILL"].value])
        if GameTag["TAG_SCRIPT_DATA_NUM_1"].value in cls.card_dict[card_id]:
            minion.TAG_SCRIPT_DATA_NUM_1 = cls.card_dict[card_id][GameTag["TAG_SCRIPT_DATA_NUM_1"].value]
        if GameTag["TAG_SCRIPT_DATA_NUM_2"].value in cls.card_dict[card_id]:
            minion.TAG_SCRIPT_DATA_NUM_2 = cls.card_dict[card_id][GameTag["TAG_SCRIPT_DATA_NUM_2"].value]
        if GameTag["CARDRACE"].value in cls.card_dict[card_id]:
            minion.race = Race(cls.card_dict[card_id][GameTag["CARDRACE"].value])
        if 1530 in cls.card_dict[card_id]:  # Zapp, Attack minion with the lowest Attack
            minion.atk_lowest_atk_minion = bool(cls.card_dict[card_id][1530])

        return minion

    @classmethod
    def enum_id_to_card_id(cls, enum_id: int) -> str:
        if enum_id in cls.enum_id_to_card_id_dict:
            return cls.enum_id_to_card_id_dict[enum_id]
        else:
            return ''


    @staticmethod
    def tag_value_to_int(tag, value):
        if not tag.isdigit():
            try:
                tag = int(GameTag[tag])
            except KeyError:
                main_logger.exception(f"tag_value_to_int() key(tag) error - no tag key, tag: {tag}, value: {value}")
        else:
            tag = int(tag)

        if not value.isdigit():
            try:
                if tag == int(GameTag.CARDTYPE):
                    value = int(CardType[value])
                elif tag == int(GameTag.FACTION):
                    value = int(Faction[value])
                elif tag == int(GameTag.CARDRACE):
                    value = int(Race[value])
                elif tag == int(GameTag.RARITY):
                    value = int(Rarity[value])
                elif tag == int(GameTag.ZONE):
                    value = int(Zone[value])
                elif tag == int(GameTag.MULLIGAN_STATE):
                    value = int(Mulligan[value])
                elif tag == int(GameTag.STEP) or tag == int(GameTag.NEXT_STEP):
                    value = int(Step[value])
                elif tag == int(GameTag.PLAYSTATE):
                    value = int(PlayState[value])
                elif tag == int(GameTag.STATE):
                    value = int(State[value])
                elif tag == int(GameTag.CLASS):
                    value = int(CardClass[value])
                else:
                    main_logger.error(f"tag_value_to_int() key(value) error - no tag name, tag: {tag}, value: {value}")
            except KeyError:
                main_logger.exception(f"tag_value_to_int() key(value) error - no value key, tag: {tag}, value: {value}")
        else:
            value = int(value)

        return tag, value


Util.init_util()

if __name__ == "__main__":
    import hearthstone
    import hearthstone_data

    # for card_id in Util.bp_minion_list:
    #     print(Util.card_name_by_id(card_id))

    print(Util.enum_id_to_card_id(58412))

    # print(hearthstone.__version__)
    # print(hearthstone_data.__version__)
    # print(hearthstone_data.get_carddefs_path())
    #
    # card_name_by_id('LOOT_078')



