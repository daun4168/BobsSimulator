from typing import List
import logging

class Game:
    def __init__(self):
        self.build_number = None
        self.game_type = None
        self.format_type = None
        self.scenarioID = None
        self.player_battle_tag = None

        self.turn_num = 0
        self.battle_num = 0
        self.leaderboard_place = 1

        self.battle = Battle()
        self.battle_history = {}  # key: battle_num, value: board


class Battle:
    def __init__(self):
        self.me = Player()
        self.enemy = Player()

        self.atk_player = None
        self.seq = 0

    def players(self):
        return [self.me, self.enemy]

    def print_log(self, logger: logging.Logger):
        logger.info(f"# Battle Info")
        self.me.print_log(logger, is_me=True)
        logger.info(f"# versus")
        self.enemy.print_log(logger, is_me=True)


class Player:
    def __init__(self):
        self.board = [None] * 8
        self.hero = Hero()
        self.hero_power = HeroPower()
        self.secrets = []
        self.graveyard = []

        self.atk_minion_pos = None
        self.not_attack_last_seq = False

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
        return self.board.count(None)

    def empty(self):
        return self.board.count(None) == len(self.board)

    def sum_damage(self):
        damage = 0
        damage += self.hero.tech_level

        for minion in self.board:
            if minion is None:
                continue
            damage += minion.tech_level
        return damage


class Hero:
    def __init__(self):
        self.entity_id = 0
        self.card_id = ""
        self.health = 40
        self.damage = 0
        self.taken_damage = 0
        self.tech_level = 0

    def print_log(self, logger: logging.Logger, is_me=True):
        from BobsSimulator.Util import card_name_by_id
        from BobsSimulator.Main import LOCALE
        name = card_name_by_id(self.card_id, locale=LOCALE)
        if is_me:
            start_text = "PlayerHero"
        else:
            start_text = "EnemyHero"
        logger.info(f"""* {start_text} -name "{name}@{self.card_id}" -hp {self.health - self.damage} -tech {self.tech_level} """)


class HeroPower:
    def __init__(self):
        self.entity_id = 0
        self.card_id = ""
        self.exhausted = False

    def print_log(self, logger: logging.Logger, is_me=True):
        from BobsSimulator.Util import card_name_by_id
        from BobsSimulator.Main import LOCALE
        name = card_name_by_id(self.card_id, locale=LOCALE)
        if is_me:
            start_text = "PlayerHeroPower"
        else:
            start_text = "EnemyHeroPower"
        log_text = f"""* {start_text} -name "{name}@{self.card_id}" """
        if self.exhausted:
            log_text += "-exhausted "
        logger.info(log_text)


class Secret:
    def __init__(self):
        self.entity_id = 0
        self.card_id = ""

    def print_log(self, logger: logging.Logger, is_me=True):
        from BobsSimulator.Util import card_name_by_id
        from BobsSimulator.Main import LOCALE
        name = card_name_by_id(self.card_id, locale=LOCALE)
        if is_me:
            start_text = "PlayerSecret"
        else:
            start_text = "EnemySecret"
        log_text = f"""* {start_text} -name "{name}@{self.card_id}" """
        logger.info(log_text)


class Enchantment:
    def __init__(self):
        self.entity_id = 0
        self.card_id = ""
        self.attached_id = 0


class Minion:
    def __init__(self):
        self.entity_id = 0
        self.card_id = ""
        self.golden = False  # PREMIUM
        self.level2 = False  # BACON_MINION_IS_LEVEL_TWO
        self.elite = False  # is legendary?
        self.tech_level = 1
        self.cost = 0

        # self.race = None -> CARDRACE ******
        # self.faction -> FACTION *******

        self.exhausted = 0

        self.attack = 0
        self.health = 0
        self.damage = 0
        self.taunt = False
        self.divine_shield = False
        self.poisonous = False
        self.windfury = 0  # attack n times more!
        self.reborn = False
        self.charge = False
        self.modular = False
        self.deathrattle = False
        self.battlecry = False
        self.discover = False
        self.aura = False
        self.overkill = False
        self.start_of_combat = False
        self.TAG_SCRIPT_DATA_NUM_1 = 0  # Number of Hero Power Used
        self.TAG_SCRIPT_DATA_NUM_2 = 0  # Red Whelp combat start damage
        self.enchantments = []

        self.zone = None
        self.pos = None
        self.is_mine = False  # if card is player's, True

    def print_log(self, logger: logging.Logger, is_me=True):
        from BobsSimulator.Util import card_name_by_id
        from BobsSimulator.Main import LOCALE
        name = card_name_by_id(self.card_id, locale=LOCALE)
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

        for enchant in self.enchantments:
            enchant_cardid = enchant.card_id
            enchant_name = card_name_by_id(enchant_cardid, locale=LOCALE)
            log_text += f"""-enchant "{enchant_name}@{enchant_cardid}" """
        logger.info(log_text)


ENTITY_TYPES = ["CREATE_GAME",
                "FULL_ENTITY",
                "TAG_CHANGE",
                "BLOCK_START",
                "BLOCK_END",
                "SHOW_ENTITY",
                "HIDE_ENTITY",
                "META_DATA",
                "CHANGE_ENTITY",
                "RESET_GAME",
                "SUB_SPELL_START",
                "SUB_SPELL_END",
                ]

DEATHRATTLE_BUFF_CARDIDS = [
    "BOT_312e",
    "TB_BaconUps_032e",
    "UNG_999t2e",
]

BOB_NAMES = [
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


