
from BobsSimulator.HSType import Hero, Minion, Battle, ENTITY_TYPES, Enchantment


entity_id_to_minion_dict = {}

battle = Battle()
minion = Minion()


battle.me.board[2] = minion
entity_id_to_minion_dict[10] = minion


enchant = Enchantment()

enchant.entity_id = 200

entity_id_to_minion_dict[10].enchantments.append(enchant)


print(1)