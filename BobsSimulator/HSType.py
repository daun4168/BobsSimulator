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


class Player:
    def __init__(self):
        self.board = [None] * 8
        self.hero = Hero()
        self.hero_power = HeroPower()
        self.secrets = []
        self.graveyard = []

    def empty(self):
        return self.board.count(None) == len(self.board)

    def sum_damage(self):
        damage = 0



        return damage


class Hero:
    def __init__(self):
        self.entity_id = 0
        self.card_id = ""
        self.health = 40
        self.damage = 0
        self.taken_damage = 0
        self.tech_level = 0


class HeroPower:
    def __init__(self):
        self.entity_id = 0
        self.card_id = ""
        self.exhausted = False


class Secret:
    def __init__(self):
        self.entity_id = 0
        self.card_id = ""


class Enchantment:
    def __init__(self):
        self.entity_id = 0
        self.card_id = ""
        self.attached_id = 0


class Minion:
    def __init__(self):
        self.entity_id = 0
        self.card_id = ""
        self.golden = False
        self.elite = False
        self.tech_level = 1
        self.cost = 0

        # self.race = None -> CARDRACE ******
        # self.faction -> FACTION *******
        # self.battlecry

        self.exhausted = 0

        self.attack = 0
        self.health = 0
        self.damage = 0
        self.taunt = False
        self.divine_shield = False
        self.poisonous = False
        self.windfury = False
        self.reborn = False
        self.deathrattle = False
        self.battlecry = False
        self.start_of_combat = False
        self.enchantments = []

        self.zone = None
        self.pos = None
        self.is_mine = False  # if card is player's, True



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


