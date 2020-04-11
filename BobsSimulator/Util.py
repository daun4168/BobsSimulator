import xmltodict
import json
import random
from typing import Dict, Optional, List, Iterable
from collections import defaultdict

from BobsSimulator.HSLogging import main_logger
from BobsSimulator.Main import VERSION_NUMBER, LOCALE
from BobsSimulator.HSType import GameTag, CardType, Faction, Race, Rarity, Zone, Mulligan, Step, State, CardClass, PlayState, Minion, RACE_ALL
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
                        for race_all in RACE_ALL:
                            cls.bp_race_dict[race_all].append(card_id)
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
    def random_bp_minion_cost(cls, cost: int, golden=False, except_card_ids: Iterable[str] = None) -> Optional[Minion]:
        return Util.random_bp_minion_by_list(cls.bp_cost_dict[cost], golden, except_card_ids)

    @classmethod
    def random_bp_minion_tech(cls, tech: int, golden=False, except_card_ids: Iterable[str] = None) -> Optional[Minion]:
        return Util.random_bp_minion_by_list(cls.bp_tech_dict[tech], golden, except_card_ids)

    @classmethod
    def random_bp_minion_race(cls, race: Race, golden=False, except_card_ids: Iterable[str] = None) -> Optional[Minion]:
        return Util.random_bp_minion_by_list(cls.bp_race_dict[race], golden, except_card_ids)

    @classmethod
    def random_bp_minion_elite(cls, golden=False, except_card_ids: Iterable[str] = None) -> Optional[Minion]:
        return Util.random_bp_minion_by_list(cls.bp_elite_list, golden, except_card_ids)

    @classmethod
    def random_bp_minion_deathrattle(cls, golden=False, except_card_ids: Iterable[str] = None) -> Optional[Minion]:
        return Util.random_bp_minion_by_list(cls.bp_deathrattle_list, golden, except_card_ids)

    @classmethod
    def random_bp_minion(cls, golden=False, except_card_ids: Iterable[str] = None) -> Optional[Minion]:
        return Util.random_bp_minion_by_list(cls.bp_minion_list, golden, except_card_ids)

    @classmethod
    def random_bp_minion_by_list(cls, card_ids, golden=False, except_card_ids: Iterable[str] = None) -> Optional[Minion]:
        choice_list: list
        if type(except_card_ids) is str:
            choice_list = [card_id for card_id in card_ids if card_id != except_card_ids]
        elif except_card_ids:
            choice_list = [card_id for card_id in card_ids if card_id not in except_card_ids]
        else:
            choice_list = card_ids

        try:
            card_id = random.choice(choice_list)
        except IndexError:
            return None

        return cls.make_default_minion(card_id, golden=golden)

    @classmethod
    def make_default_minion(cls, card_id, golden=False, level2=None) -> Minion:
        minion = Minion()
        minion.card_id = card_id
        if GameTag["PREMIUM"].value in cls.card_dict[card_id]:
            minion.golden = bool(cls.card_dict[card_id][GameTag["PREMIUM"].value])
        minion.golden = minion.golden or golden
        if GameTag["BACON_MINION_IS_LEVEL_TWO"].value in cls.card_dict[card_id]:
            minion.level2 = bool(cls.card_dict[card_id][GameTag["BACON_MINION_IS_LEVEL_TWO"].value])
        if GameTag["ELITE"].value in cls.card_dict[card_id]:
            minion.elite = bool(cls.card_dict[card_id][GameTag["ELITE"].value])
        if GameTag["TECH_LEVEL"].value in cls.card_dict[card_id]:
            minion.tech_level = cls.card_dict[card_id][GameTag["TECH_LEVEL"].value]
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
        if GameTag["CARDRACE"].value in cls.card_dict[card_id]:
            minion.race = Race(cls.card_dict[card_id][GameTag["CARDRACE"].value])

        if level2:
            if not minion.card_id.startswith('TB_BaconUps'):
                minion.attack *= 2
                minion.health *= 2
            minion.golden = True
            minion.level2 = True

        if minion.card_id in ("BGS_071", "TB_BaconUps_123"):  # Deflect-o-Bot
            minion.divine_shield = True

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

    @staticmethod
    def make_number_circle(num: int):
        if num is None:
            return ''
        if num < 0 or num > 20:
            return str(num)
        if num == 0:
            return '\u24ea'
        return chr(0x245f + num)


Util.init_util()

if __name__ == "__main__":
    import hearthstone
    import hearthstone_data

    # for card_id in Util.bp_minion_list:
    #     print(Util.card_name_by_id(card_id))

    # print(Util.enum_id_to_card_id(58412))

    # print(hearthstone.__version__)
    # print(hearthstone_data.__version__)
    # print(hearthstone_data.get_carddefs_path())
    #
    # card_name_by_id('LOOT_078')

    # print(Util.make_number_circle(1))

    for i in range(50):
        new_minion = Util.random_bp_minion_race(Race.BEAST)
        print(new_minion.info())



