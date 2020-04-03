
from collections import defaultdict


dd = defaultdict(list)


dd[1].append(1)

dd[3].append(4)
dd[4].append(4)
dd[3].append(2)

idx = 0
while dd:
    this_idx = idx
    for value in dd[this_idx]:
        print(this_idx, value)
    del dd[this_idx]
    idx += 1

# print(dd)
# print(bool(dd))
