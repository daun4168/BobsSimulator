import xmltodict
import json
from typing import Dict
from PySide2.QtCore import QEventLoop, QTimer

from BobsSimulator.HSLogging import main_logger
from BobsSimulator.Main import VERSION_NUMBER
from BobsSimulator.HSType import GameTag, CardType, Faction, Race, Rarity, Zone, Mulligan, Step, State, CardClass, PlayState
import hearthstone_data

# carddefs_path = 'res/CardDefs.xml'
# carddefs_version = 43246
carddefs_path = hearthstone_data.get_carddefs_path()
carddefs_version = int(float(hearthstone_data.__version__))

if VERSION_NUMBER != carddefs_version:
    main_logger.warning(f"Build number NOT correct, Program: {VERSION_NUMBER}, CardDefs: {carddefs_version}")


def qsleep(ms):
    loop = QEventLoop()
    QTimer.singleShot(ms, loop.quit)
    loop.exec_()


card_name_dict = {}  # type: Dict
is_card_name_dict_init = False


def _init_card_name_dict():
    global card_name_dict
    global is_card_name_dict_init
    card_defs = open(carddefs_path, 'r', encoding='UTF8')
    card_dict = xmltodict.parse(card_defs.read())
    card_defs.close()

    card_dict = json.dumps(card_dict)
    card_dict = json.loads(card_dict)

    lang_list = [
        'koKR',
        'enUS',
    ]

    card_data_list = card_dict["CardDefs"]["Entity"]
    for card_data in card_data_list:
        card_id = card_data["@CardID"]
        card_name_dict[card_id] = {}
        for lang in lang_list:
            card_name_dict[card_id][lang] = card_data['Tag'][0][lang]
    is_card_name_dict_init = True


def card_name_by_id(card_id, locale='koKR'):
    if not is_card_name_dict_init:
        _init_card_name_dict()

    if not card_id:
        return ""
    return card_name_dict[card_id][locale]


def tag_value_to_int(tag, value):
    if not tag.isdigit():
        try:
            tag = int(GameTag[tag])
        except KeyError:
            main_logger.exception(f"tag_value_to_int() key(tag) error - no tag key, tag: {tag}, value: {value}")
    else:
        tag = int(tag)

    if not value.isdigit():
        try:
            if tag == int(GameTag.CARDTYPE):
                value = int(CardType[value])
            elif tag == int(GameTag.FACTION):
                value = int(Faction[value])
            elif tag == int(GameTag.CARDRACE):
                value = int(Race[value])
            elif tag == int(GameTag.RARITY):
                value = int(Rarity[value])
            elif tag == int(GameTag.ZONE):
                value = int(Zone[value])
            elif tag == int(GameTag.MULLIGAN_STATE):
                value = int(Mulligan[value])
            elif tag == int(GameTag.STEP) or tag == int(GameTag.NEXT_STEP):
                value = int(Step[value])
            elif tag == int(GameTag.PLAYSTATE):
                value = int(PlayState[value])
            elif tag == int(GameTag.STATE):
                value = int(State[value])
            elif tag == int(GameTag.CLASS):
                value = int(CardClass[value])
            else:
                main_logger.error(f"tag_value_to_int() key(value) error - no tag name, tag: {tag}, value: {value}")
        except KeyError:
            main_logger.exception(f"tag_value_to_int() key(value) error - no value key, tag: {tag}, value: {value}")
    else:
        value = int(value)

    return tag, value


if __name__ == "__main__":
    import hearthstone
    import hearthstone_data

    print(hearthstone.__version__)
    print(hearthstone_data.__version__)
    print(hearthstone_data.get_carddefs_path())
