

import re

cardxml = open(r'C:\Program Files (x86)\Hearthstone\Data\Win\cards0.unity3d', 'r', encoding='UTF8').read()
cards = re.findall(r'\<Entity.*?Entity\>', cardxml, re.DOTALL)
with open('cards.xml', 'w') as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>')
    for card in cards:
        f.write(card)
        f.write('\n')