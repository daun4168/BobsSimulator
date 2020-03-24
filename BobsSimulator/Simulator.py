from PySide2.QtCore import Signal, QObject

from BobsSimulator.HSType import Battle
from BobsSimulator.HSLogging import simulator_logger

import copy


class Simulator(QObject):
    def __init__(self):
        QObject.__init__()

    @staticmethod
    def simulate(battle: Battle, simulate_num=1) -> list:
        result = []
        simulator_logger.info("="*50)
        simulator_logger.info("Simulate Start")

        for i in range(simulate_num):
            copy_battle = copy.deepcopy(battle)
            result.append(Simulator.simulate_once(copy_battle))
        simulator_logger.info("=" * 50)
        return result

    @staticmethod
    def simulate_once(battle: Battle):

        battle.test_number += i

        return battle.test_number
