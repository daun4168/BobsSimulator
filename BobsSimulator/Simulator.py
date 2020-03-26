from PySide2.QtCore import Signal, QObject

from BobsSimulator.HSType import Battle
from BobsSimulator.HSLogging import simulator_logger

import copy
import random




class Simulator(QObject):
    def __init__(self):
        QObject.__init__()
        self.battle = Battle()

    def simulate(self, battle: Battle, simulate_num=1) -> list:
        result = []
        simulator_logger.info(f'''# {"="*50}''')
        simulator_logger.info("# Simulate Start")
        simulator_logger.info("-"*50)
        simulator_logger.info("# Battle Info")
        battle.print_log(simulator_logger)
        simulator_logger.info("-"*50)

        for i in range(simulate_num):
            simulator_logger.info("-"*50)
            simulator_logger.info(f"# Simulation {i+1}/{simulate_num}")
            self.battle = copy.deepcopy(battle)
            result.append(self.simulate_once())
            simulator_logger.info("-"*50)
        simulator_logger.info("=" * 50)
        return result

    def simulate_once(self):
        self.simulate_init()

        self.set_attack_player()
        self.simulate_hero_power()

        while True:
            self.battle.seq += 1
            if self.battle.me.not_attack_last_turn and self.battle.enemy.not_attack_last_turn:  # Draw
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

    def simulate_init(self):
        self.battle.seq = 0
        for player in self.battle.players():
            player.not_attack_last_seq = False

    def set_attack_player(self):
        if self.battle.me.minion_num() > self.battle.enemy.minion_num():
            self.battle.atk_player = self.battle.me
        elif self.battle.me.minion_num() < self.battle.enemy.minion_num():
            self.battle.atk_player = self.battle.enemy
        else:
            self.battle.atk_player = random.choice(self.battle.players())

        for player in self.battle.players():
            player.atk_minion_pos = None

    def simulate_hero_power(self):
        pass

    def next_attacker(self):


    def simulate_attack(self):
        pass


