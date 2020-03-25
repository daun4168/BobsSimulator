from PySide2.QtCore import Signal, QObject

from BobsSimulator.HSType import Battle
from BobsSimulator.HSLogging import simulator_logger

import copy


class Simulator(QObject):
    def __init__(self):
        QObject.__init__()
        self.battle = None


    def simulate(self, battle: Battle, simulate_num=1) -> list:
        result = []
        simulator_logger.info("="*50)
        simulator_logger.info("Simulate Start")

        for i in range(simulate_num):
            self.battle = copy.deepcopy(battle)
            result.append(self.simulate_once())
        simulator_logger.info("=" * 50)
        return result

    def simulate_once(self):
        self.battle.seq = 0
        players = [self.battle.me, self.battle.enemy]
        for player in players:
            player.not_attack_last_seq = True


        while True:
            if self.battle.me.not_attack_last_turn and self.battle.enemy.not_attack_last_turn:  # Draw
                return 0
            if self.battle.me.empty() and self.battle.enemy.empty():  # Draw
                return 0
            elif self.battle.me.empty():  # Lose
                return -self.battle.enemy.sum_damage()
            elif self.battle.enemy.empty():  # Win
                return self.battle.me.sum_damage()

            if seq > 10000:
                simulator_logger.error("INFINITE LOOP")
                return 0

    def simulate_hero_power(self):
        pass






        battle.test_number += i

        return battle.test_number


