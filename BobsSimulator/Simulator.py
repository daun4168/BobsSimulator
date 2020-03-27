from PySide2.QtCore import Signal, QObject

from BobsSimulator.HSType import Battle, Minion, Zone
from BobsSimulator.HSLogging import simulator_logger
import copy
import random


class Simulator(QObject):
    def __init__(self):
        QObject.__init__()
        self.battle = Battle()

    def simulate(self, battle: Battle, simulate_num=1) -> list:
        result = []
        simulator_logger.info(f'''# {"=" * 50}''')
        simulator_logger.info("# Simulate Start")
        simulator_logger.info("-" * 50)
        simulator_logger.info("# Battle Info")
        battle.print_log(simulator_logger)
        simulator_logger.info("-" * 50)

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

            if self.battle.seq > 10000:
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
            player.atk_minion_pos = None

    def simulate_hero_power(self):
        pass

    def next_attacker(self):
        player = self.battle.atk_player()
        if player.atk_minion_pos is None:
            player.atk_minion_pos = 1
        for i in range(player.minion_num()):
            if player.board[player.atk_minion_pos].attack != 0:
                return player.board[player.atk_minion_pos]
            player.atk_minion_pos += 1
            if player.atk_minion_pos > player.minion_num():
                player.atk_minion_pos -= player.minion_num()
        return None

    def simulate_attack(self):
        attacker = self.next_attacker()
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
