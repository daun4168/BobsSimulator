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

        seq = 0

        did_attack_last_seq = True
        did_attack_this_seq = True

        while True:
            if self.battle.me.empty() and self.battle.enemy.empty():  # Draw
                return 0
            elif self.battle.me.empty():  # Lose






        battle.test_number += i

        return battle.test_number


