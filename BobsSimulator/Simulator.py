import copy
import random
from typing import List, Dict, Optional

from PySide2.QtCore import Signal, QObject

from BobsSimulator.HSType import Battle, Minion, Zone, Player
from BobsSimulator.HSLogging import simulator_logger, console_logger
from BobsSimulator.Util import card_name_by_id



class Simulator(QObject):
    def __init__(self):
        super().__init__()
        self.battle = Battle()

    def simulate(self, battle: Battle, simulate_num=1) -> list:
        result = []
        simulator_logger.info(f'''# {"=" * 50}''')
        simulator_logger.info("# Simulate Start")
        simulator_logger.info("-" * 50)
        simulator_logger.info("# Battle Info")
        battle.print_log(simulator_logger)
        simulator_logger.info("-" * 50)


        print('='*50)
        print("# Simulate Start")
        print(battle.info())

        for i in range(simulate_num):
            simulator_logger.info("-" * 50)
            simulator_logger.info(f"# Simulation {i + 1}/{simulate_num}")
            self.battle = copy.deepcopy(battle)
            result.append(self.simulate_once())
            simulator_logger.info("-" * 50)
        simulator_logger.info("=" * 50)
        return result

    def simulate_once(self):
        self.simulate_init()

        self.set_attack_player()
        self.simulate_hero_power()

        while True:
            self.battle.seq += 1
            if self.battle.me.not_attack_last_seq and self.battle.enemy.not_attack_last_seq:  # Draw
                return 0
            if self.battle.me.empty() and self.battle.enemy.empty():  # Draw
                return 0
            elif self.battle.me.empty():  # Lose
                return -self.battle.enemy.sum_damage()
            elif self.battle.enemy.empty():  # Win
                return self.battle.me.sum_damage()

            if self.battle.seq > 1000:
                simulator_logger.error("INFINITE LOOP")
                return 0

            self.simulate_attack()
            self.battle.is_me_attack = not self.battle.is_me_attack  # change atk player

    def simulate_init(self):
        self.battle.seq = 0
        for player in self.battle.players():
            player.not_attack_last_seq = False

    def set_attack_player(self):
        if self.battle.me.minion_num() > self.battle.enemy.minion_num():
            self.battle.is_me_attack = True
        elif self.battle.me.minion_num() < self.battle.enemy.minion_num():
            self.battle.is_me_attack = False
        else:
            self.battle.is_me_attack = bool(random.getrandbits(1))
        for player in self.battle.players():
            player.next_atk_minion_pos = None

    def simulate_hero_power(self):
        # TODO: make function
        pass

    def next_attacker(self, player: Player):
        if player.empty():
            return None
        if player.next_atk_minion_pos is None:
            player.next_atk_minion_pos = 1
        for i in range(player.minion_num()):
            if player.board[player.next_atk_minion_pos].attack != 0:
                attacker = player.board[player.next_atk_minion_pos]
                player.next_atk_minion_pos += 1
                if player.next_atk_minion_pos > player.minion_num():
                    player.next_atk_minion_pos -= player.minion_num()
                return attacker
            player.next_atk_minion_pos += 1
            if player.next_atk_minion_pos > player.minion_num():
                player.next_atk_minion_pos -= player.minion_num()
        return None

    def simulate_attack(self):

        attacker = self.next_attacker(self.battle.atk_player())
        if attacker is None:
            self.battle.atk_player().not_attack_last_seq = True
            return

        num_of_atk = 1 + attacker.windfury
        for i in range(num_of_atk):
            if attacker.zone != Zone.PLAY:
                return
            self.attack_once(attacker)

    def attack_once(self, attacker: Minion):
        if self.battle.dfn_player().empty():
            return

        defender = None  # type: Optional[Minion]
        if attacker.atk_lowest_atk_minion:
            defender = self.random_lowest_atk_minion(self.battle.dfn_player())
        else:
            defender = self.random_defense_minion(self.battle.dfn_player())
        print(f"ATTACK {self.battle.atk_player().hero.name()}'s {attacker.info()} -> {self.battle.dfn_player().hero.name()}'s {defender.info()}")

        self.simulate_damage_by_minion(defender, attacker)
        self.simulate_damage_by_minion(attacker, defender)

        # cleave
        if attacker.card_id in ("GVG_113", "LOOT_078"):  # Foe Reaper 4000, Cave Hydra
            if defender.pos > 1 and self.battle.dfn_player().board[defender.pos - 1] is not None:
                self.simulate_damage_by_minion(self.battle.dfn_player().board[defender.pos - 1], attacker)
            if defender.pos < 7 and self.battle.dfn_player().board[defender.pos + 1] is not None:
                self.simulate_damage_by_minion(self.battle.dfn_player().board[defender.pos + 1], attacker)
        self.check_deaths()
        print(self.battle.info())


    def check_deaths(self):

        for player in self.battle.players():
            for minion in player.minions():
                # Do Deaths
                if minion.damage >= minion.health:
                    print(f'REMOVE: {minion.info()}')
                    player.remove_minion(minion)
                # 하이에나류 버프
        # 곡예사, 죽메


    def simulate_damage_by_minion(self, defender: Minion, attacker: Minion):
        self.simulate_damage(defender, attacker.attack, attacker.poisonous)

        if attacker.overkill:
            # TODO: overkill something
            pass

    def simulate_damage(self, defender: Minion, amount: int, poisonous: bool = False):
        if amount <= 0:
            return False
        # print(f"# {defender_player.hero.name()}'s {defender.info()} damaged {amount} {'poisonous' if poisonous else ''}")
        if defender.divine_shield:
            defender.divine_shield = False
            self.frendly_minion_break_divine_shield(defender.player)
            return False
        else:
            defender.damage += amount
            if defender.hp() > 0 and poisonous:
                defender.damage = defender.health
            self.minion_damaged(defender)
            return True

    def frendly_minion_break_divine_shield(self, player: Player):
        pass

    def minion_damaged(self, minion: Minion):
        pass

    def random_lowest_atk_minion(self, player: Player) -> Optional[Minion]:
        if player.empty():
            return None
        lowest_atk = None
        lowest_atk_minions = []  # type: List[Minion]

        for minion in player.minions():
            if not lowest_atk_minions:
                lowest_atk = minion.attack
                lowest_atk_minions.append(minion)
                continue

            if minion.attack == lowest_atk:
                lowest_atk_minions.append(minion)
            elif minion.attack < lowest_atk:
                lowest_atk_minions.clear()
                lowest_atk_minions.append(minion)

        return random.choice(lowest_atk_minions)

    def random_defense_minion(self, player: Player) -> Optional[Minion]:
        if player.empty():
            return None
        taunt_minions = []  # type: List[Minion]

        for minion in player.minions():
            if minion.taunt:
                taunt_minions.append(minion)

        if taunt_minions:
            return random.choice(taunt_minions)
        else:
            return random.choice(player.minions())











