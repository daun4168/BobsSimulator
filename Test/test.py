
from time import time
from BobsSimulator.HSType import Race

st_time = time()

from BobsSimulator.Util import Util
for i in range(50):
    new_minion = Util.random_bp_minion_race(Race.BEAST)

print("Cython Util time: ", time() - st_time)



st_time = time()

from BobsSimulator.Util import Util
for i in range(50):
    new_minion = Util.random_bp_minion_race(Race.BEAST)

print("Util2 time: ", time() - st_time)
