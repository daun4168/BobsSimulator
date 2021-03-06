from typing import List, Dict, Optional, DefaultDict, Deque, Callable
from collections import defaultdict, deque
from abc import ABCMeta, abstractmethod
from hearthstone.enums import GameTag, CardType, Faction, Race, Zone, State, \
    Rarity, Mulligan, Step, PlayState, CardClass, PowerType
import copy
import random
import logging


class Game:
    def __init__(self):
        self.build_number = None  # type: Optional[int]
        self.game_type = None  # type: Optional[str]
        self.format_type = None  # type: Optional[str]
        self.scenarioID = None  # type: Optional[int]
        self.player_battle_tag = None  # type: Optional[str]

        self.turn_num = 0  # type: int
        self.battle_num = 0  # type: int
        self.leaderboard_place = 1  # type: int
        self.game_end = False

        self.battle = Battle()  # type: Battle
        self.battle_history = {}  # type: Dict[int, Battle] # key: battle_num, value: board


class Battle:
    def __init__(self, me: Optional["Player"] = None, enemy: Optional["Player"] = None):
        if me is None:
            self.me = Player()  # type: Player
        else:
            self.me = me

        if enemy is None:
            self.enemy = Player()  # type: Player
        else:
            self.enemy = enemy

        self.me.opponent = self.enemy
        self.enemy.opponent = self.me
        self.battle_num = 0  # type: int
        self.is_end = False  # type: bool

        self.is_me_trigger_first = True  # type: bool
        self.is_me_attack = None  # type: Optional[bool]
        self.attack_player = None  # type: Optional[Player]
        self.seq = 0  # type: int

    def players(self):
        if self.is_me_trigger_first:
            return self.me, self.enemy
        else:
            return self.enemy, self.me

    def print_log(self, logger: logging.Logger):
        logger.info(f"# Battle Info")
        self.me.print_log(logger, is_me=True)
        logger.info(f"# versus")
        self.enemy.print_log(logger, is_me=True)

    def info(self):
        text = ""
        text += self.enemy.info()
        text += '\n'
        text += self.me.info()
        return text


class Player:
    def __init__(self):
        self.board = [None] * 8  # type: List[Optional[Minion]]
        self.hero = Hero()  # type: Hero
        self.hero_power = HeroPower()  # type: HeroPower
        self.secrets = []  # type: List[Secret]
        self.graveyard = []  # type: List[Minion]

        self.opponent = None  # type: Optional[Player]

        self.next_atk_minion_pos = None  # type: Optional[int]
        self.not_attack_last_seq = False  # type: bool

        self.death_triggers = defaultdict(deque)  # type: DefaultDict[int, Deque[Minion]]
        self.trigger_pos = 0  # type: int
        self.death_num_this_turn_by_race = defaultdict(int)  # type: DefaultDict[Race, int]

        self.reborn_triggers = defaultdict(deque)  # type: DefaultDict[int, Deque[str]]
        self.reborn_trigger_pos = 0  # type: int

    def info(self):
        text = ""
        text += self.hero.info()
        for i in range(1, 8):
            if self.board[i] is None:
                text += f"<X>[{' '*20}]"
            else:
                text += self.board[i].info()
        return text

    def death_init(self):
        self.death_triggers = defaultdict(deque)
        self.trigger_pos = 0
        self.death_num_this_turn_by_race = defaultdict(int)

        self.reborn_triggers = defaultdict(deque)
        self.reborn_trigger_pos = 0

    def print_log(self, logger: logging.Logger, is_me=True):
        self.hero.print_log(logger, is_me)
        self.hero_power.print_log(logger, is_me)
        for secret in self.secrets:
            secret.print_log(logger, is_me)
        for minion in self.board:
            if minion is None:
                continue
            minion.print_log(logger, is_me)

    def minion_num(self):
        return len(self.board) - self.board.count(None)

    def empty(self) -> bool:
        return self.board.count(None) == len(self.board)

    def minions(self) -> List['Minion']:
        minion_list = []
        for minion in self.board:
            if minion:
                minion_list.append(minion)
        return minion_list

    def left_minion(self) -> Optional['Minion']:
        for minion in self.minions():
            if minion.hp() > 0:
                return minion
        return None

    def append_minion(self, new_minion: 'Minion', pos: Optional[int] = None):
        if self.minion_num() >= 7:
            return False
        if pos is None:
            pos = self.minion_num() + 1

        # pos change
        for minion in self.minions():
            if minion.pos >= pos:
                minion.pos += 1

        # player.next_atk_minion_pos change
        if self.next_atk_minion_pos is not None:
            if new_minion.pos < self.next_atk_minion_pos:
                self.next_atk_minion_pos += 1

        new_minion.zone = Zone.PLAY
        new_minion.pos = pos
        new_minion.player = self
        self.board[pos] = new_minion

    def sum_damage(self):
        damage = 0
        damage += self.hero.tech_level

        for minion in self.board:
            if minion is None:
                continue
            damage += minion.tech_level
        return damage


class HSObject(metaclass=ABCMeta):
    def __init__(self):
        self.card_id = ""  # type: str
        self.created_enchants = []  # type: List[Enchantment]
        self.zone = Zone.INVALID  # type: Zone
        self.player = None  # type: Optional[Player]

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def info(self) -> str:
        pass


class Hero(HSObject):
    def __init__(self):
        super().__init__()
        self.health = 40  # type: int
        self.damage = 0  # type: int
        self.taken_damage = 0  # type: int
        self.tech_level = 0  # type: int


    def name(self):
        from BobsSimulator.Util import Util
        return Util.card_name_by_id(self.card_id)

    def info(self):
        text = f"{self.name() + '(' + str(self.tech_level) + ')'}"
        non_ascii = 0
        for c in text:
            if ord(c) < 0 or ord(c) > 127:
                non_ascii += 1

        return f"{text:<{20-non_ascii}}"

    def print_log(self, logger: logging.Logger, is_me=True):
        from BobsSimulator.Util import Util
        from BobsSimulator.Config import LOCALE
        name = Util.card_name_by_id(self.card_id, locale=LOCALE)
        if is_me:
            start_text = "PlayerHero"
        else:
            start_text = "EnemyHero"
        logger.info(
            f"""* {start_text} -name "{name}@{self.card_id}" -hp {self.health - self.damage} -tech {self.tech_level} """)

    def hp(self):
        return self.health - self.damage


class HeroPower(HSObject):
    def __init__(self):
        super().__init__()
        self.used = False  # type: bool

    def name(self):
        from BobsSimulator.Util import Util
        return Util.card_name_by_id(self.card_id)

    def info(self):
        text = ""
        text += self.name()
        if self.used:
            text += " +used"
        return f"[{text}]"

    def print_log(self, logger: logging.Logger, is_me=True):
        from BobsSimulator.Util import Util
        from BobsSimulator.Config import LOCALE
        name = Util.card_name_by_id(self.card_id, locale=LOCALE)
        if is_me:
            start_text = "PlayerHeroPower"
        else:
            start_text = "EnemyHeroPower"
        log_text = f"""* {start_text} -name "{name}@{self.card_id}" """
        if self.used:
            log_text += "-used "
        logger.info(log_text)


class Secret:
    def __init__(self):
        self.card_id = ""  # type: str

    def name(self):
        from BobsSimulator.Util import Util
        return Util.card_name_by_id(self.card_id)

    def info(self):
        text = ""
        text += f"name: {self.name()}"

        return text

    def print_log(self, logger: logging.Logger, is_me=True):
        from BobsSimulator.Util import Util
        from BobsSimulator.Config import LOCALE
        name = Util.card_name_by_id(self.card_id, locale=LOCALE)
        if is_me:
            start_text = "PlayerSecret"
        else:
            start_text = "EnemySecret"
        log_text = f"""* {start_text} -name "{name}@{self.card_id}" """
        logger.info(log_text)


class Enchantment(HSObject):
    def __init__(self):
        super().__init__()
        self.attached_minion = None  # type: Optional[Minion]
        self.creator = None  # type: Optional[Minion, Hero, HeroPower]
        self.is_aura = False  # type: bool

    def name(self):
        from BobsSimulator.Util import Util
        return Util.card_name_by_id(self.card_id)

    def info(self):
        text = ""
        text += f"{self.name()}  "
        if self.is_aura:
            text += f"(AURA)"
        text += f"attached-{self.attached_minion.info()} "
        text += f"creator-{self.creator.info()} "

        return f"[{text}]"


class Minion(HSObject):
    def __init__(self):
        super().__init__()
        self.golden = False  # type: bool  # PREMIUM
        self.level2 = False  # type: bool  # BACON_MINION_IS_LEVEL_TWO
        self.elite = False  # type: bool  # is legendary?
        self.tech_level = 1  # type: int
        self.cost = 0  # type: int
        self.race = None  # type: Optional[Race]
        self.attack = 0  # type: int
        self.health = 0  # type: int
        self.damage = 0  # type: int
        self.taunt = False  # type: bool
        self.divine_shield = False  # type: bool
        self.poisonous = False  # type: bool
        self.windfury = 0  # attack n times more!
        self.reborn = False  # type: bool
        self.deathrattle = False  # type: bool
        self.aura = False  # type: bool
        self.overkill = False  # type: bool
        self.start_of_combat = False  # type: bool
        self.atk_lowest_atk_minion = False  # type: bool

        self.enchants = []  # type: List[Enchantment]
        self.auras = []  # type: List[Enchantment]

        self.creator = None  # type: Optional[HSObject]

        self.to_be_destroyed = False  # type: bool
        self.last_damaged_by = None  # type: Optional[HSObject]

        self.pos = 0  # type: int
        self.exhausted = False  # type: bool

    def name(self):
        from BobsSimulator.Util import Util
        return Util.card_name_by_id(self.card_id)

    def info(self):
        return self.info_emoji()
        from BobsSimulator.Util import Util
        text = ''
        if self.golden:
            text += '황금 '
        text += f'{self.name()} {self.attack}/{self.hp()}'

        if self.deathrattle:
            text += '|죽메'
        if self.divine_shield:
            text += '|천보'
        if self.poisonous:
            text += '|독성'
        if self.taunt:
            text += '|도발'
        if self.reborn:
            text += '|환생'

        non_ascii = 0
        for c in text:
            if ord(c) < 0 or ord(c) > 127:
                non_ascii += 1

        return f'<{self.pos}>[{text:^{20-non_ascii}}]'

    def info_emoji(self):
        from BobsSimulator.Util import Util
        text = ''
        if self.golden:
            text += '🌟'
        text += f'{self.name()} {self.attack}/{self.hp()}'

        if self.deathrattle:
            text += '💀'
        if self.divine_shield:
            text += '⚪'
        if self.poisonous:
            text += '☣️'
        if self.taunt:
            text += '🛡️'
        if self.reborn:
            text += '🎗️'

        non_ascii = 0
        for c in text:
            if ord(c) < 0 or ord(c) > 127:
                non_ascii += 1

        return f'{Util.make_number_circle(self.pos)}[{text:^{20-non_ascii}}]'

    def hp(self):
        return self.health - self.damage

    def buff(self, atk, hp):
        if atk >= 0:
            self.attack += atk
        else:
            self.attack = max(self.attack + atk, 0)

        if hp >= 0:
            self.health += hp
        else:
            self.health = max(self.health + hp, 1)
            self.damage = max(self.damage + hp, 0)


    def print_log(self, logger: logging.Logger, is_me=True):
        from BobsSimulator.Util import Util
        from BobsSimulator.Config import LOCALE
        name = Util.card_name_by_id(self.card_id, locale=LOCALE)
        if is_me:
            start_text = "PlayerMinion"
        else:
            start_text = "EnemyMinion"

        log_text = f"""* {start_text} -name "{name}@{self.card_id}" -atk {self.attack} -hp {self.health - self.damage} -pos {self.pos} """
        if self.level2:
            log_text += "-level2 "
        if self.taunt:
            log_text += "-taunt "
        if self.divine_shield:
            log_text += "-divine_shield "
        if self.poisonous:
            log_text += "-poisonous "
        if self.windfury:
            log_text += "-windfury "
        if self.reborn:
            log_text += "-reborn "

        for enchant in self.enchants:
            enchant_cardid = enchant.card_id
            enchant_name = Util.card_name_by_id(enchant_cardid, locale=LOCALE)
            log_text += f"""-enchant "{enchant_name}@{enchant_cardid}" """
        logger.info(log_text)


RACE_ALL = (
    Race.ELEMENTAL,
    Race.MECHANICAL,
    Race.DEMON,
    Race.MURLOC,
    Race.DRAGON,
    Race.PET,
    Race.PIRATE,
    Race.TOTEM,
)

DEATHRATTLE_ENCHANT_CARD_IDS = (
    "BOT_312e",
    "TB_BaconUps_032e",
    "UNG_999t2e",
)


class AuraInfo:
    def __init__(self, giver_card_id: str, enchant_card_id: str, add_atk: int = 0, add_hp: int = 0, check_func: Callable[[Minion, HSObject], bool] = None):
        self.giver_card_id = giver_card_id  # type: Optional[str]
        self.enchant_card_id = enchant_card_id  # type: Optional[str]
        self.add_atk = add_atk  # type: int
        self.add_hp = add_hp  # type: int

        if check_func is not None:
            self.check_func = check_func

    @staticmethod
    def check_func(minion: Minion, giver: HSObject) -> bool:
        return True


AURAINFO_LIST = [

    # """Murloc Warleader"""
    # """Mrgglaargl!"""
    AuraInfo(
        giver_card_id="EX1_507",
        enchant_card_id="EX1_507e",
        add_atk=2,
        add_hp=0,
        check_func=lambda minion, giver: minion.race in (Race.MURLOC, Race.ALL) and giver.player is minion.player
    ),

    AuraInfo(
        giver_card_id="TB_BaconUps_008",
        enchant_card_id="TB_BaconUps_008e",
        add_atk=4,
        add_hp=0,
        check_func=lambda minion, giver: minion.race in (Race.MURLOC, Race.ALL) and giver.player is minion.player
    ),

    # """Siegebreaker"""
    # """Siegebreaking!"""
    AuraInfo(
        giver_card_id="EX1_185",
        enchant_card_id="EX1_185e",
        add_atk=1,
        add_hp=0,
        check_func=lambda minion, giver: minion.race in (Race.DEMON, Race.ALL) and giver.player is minion.player
    ),

    AuraInfo(
        giver_card_id="TB_BaconUps_053",
        enchant_card_id="TB_BaconUps_053e",
        add_atk=2,
        add_hp=0,
        check_func=lambda minion, giver: minion.race in (Race.DEMON, Race.ALL) and giver.player is minion.player
    ),

    # """Mal'Ganis"""
    # """Grasp of Mal'Ganis"""
    AuraInfo(
        giver_card_id="GVG_021",
        enchant_card_id="GVG_021e",
        add_atk=2,
        add_hp=2,
        check_func=lambda minion, giver: minion.race in (Race.DEMON, Race.ALL) and giver.player is minion.player
    ),

    AuraInfo(
        giver_card_id="TB_BaconUps_060",
        enchant_card_id="TB_BaconUps_060e",
        add_atk=4,
        add_hp=4,
        check_func=lambda minion, giver: minion.race in (Race.DEMON, Race.ALL) and giver.player is minion.player
    ),


    # """Dire Wolf Alpha"""
    # """Strength of the Pack"""
    AuraInfo(
        giver_card_id="EX1_162",
        enchant_card_id="EX1_162o",
        add_atk=1,
        add_hp=0,
        check_func=lambda minion, giver: minion.pos in (giver.pos - 1, giver.pos + 1) and giver.player is minion.player
    ),

    AuraInfo(
        giver_card_id="TB_BaconUps_088",
        enchant_card_id="TB_BaconUps_088e",
        add_atk=2,
        add_hp=0,
        check_func=lambda minion, giver: minion.pos in (giver.pos - 1, giver.pos + 1) and giver.player is minion.player
    ),

    # """Deathwing"""
    # """ALL Will Burn!"""
    AuraInfo(
        giver_card_id="TB_BaconShop_HP_061",
        enchant_card_id="TB_BaconShop_HP_061e",
        add_atk=2,
        add_hp=0,
        check_func=lambda minion, giver: True
    ),


]

AURAINFO_DICT = {}

for aurainfo in AURAINFO_LIST:
    AURAINFO_DICT[aurainfo.giver_card_id] = aurainfo
    AURAINFO_DICT[aurainfo.enchant_card_id] = aurainfo


if __name__ == "__main__":
    pass

