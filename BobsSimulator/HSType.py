class Game:
    def __init__(self):
        self.turn = 0
        self.battle = 0
        self.player_hero_id = ""
        self.player_hp = 40
        self.player

class Hero:
    def __init__(self):
        self.card_id = ""
        self.health = 40
        self.tech_level = 0


class Card:
    def __init__(self):
        self.card_id = ""
        self.golden = False

        self.attack = 0
        self.health = 0
        self.taunt = False
        self.divine_shield = False
        self.poisonous = False
        self.windfury = False
        self.reborn = False
        self.death_rate = []

        self.zone = None
        self.player = None
        self.is_mine = False


class Board:
    def __init__(self):
        self.turn_num = 0
        self.battle_num = 0

        self.player_board = [None] * 7
        self.player_hero = Hero()

        self.enemy_board = [None] * 7
        self.enemy_hero = Hero()




