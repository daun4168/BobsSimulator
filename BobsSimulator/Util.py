import xmltodict
import json
import hearthstone.enums as hsenums

from PySide2.QtCore import QEventLoop, QTimer


from BobsSimulator.HSLogging import main_logger
from BobsSimulator.Main import VERSION_NUMBER
import hearthstone_data
import hearthstone

# carddefs_path = 'res/CardDefs.xml'
# carddefs_version = 43246
carddefs_path = hearthstone_data.get_carddefs_path()
carddefs_version = int(float(hearthstone_data.__version__))

if VERSION_NUMBER != carddefs_version:
    main_logger.warning(f"Build number NOT correct, Program: {VERSION_NUMBER}, CardDefs: {carddefs_version}")


card_name_dict = {}
CardDefs = open(carddefs_path, 'r', encoding='UTF8')
card_dict = xmltodict.parse(CardDefs.read())
CardDefs.close()

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


def qsleep(ms):
    loop = QEventLoop()
    QTimer.singleShot(ms, loop.quit)
    loop.exec_()


def card_name_by_id(card_id, locale='koKR'):
    if not card_id:
        return ""
    return card_name_dict[card_id][locale]


def tag_value_to_int(tag, value):
    if not tag.isdigit():
        try:
            tag = int(hsenums.GameTag[tag])
        except KeyError:
            main_logger.exception(f"tag_value_to_int() key(tag) error - no tag key, tag: {tag}, value: {value}")
    else:
        tag = int(tag)

    if not value.isdigit():
        try:
            if tag == int(hsenums.GameTag.CARDTYPE):
                value = int(hsenums.CardType[value])
            elif tag == int(hsenums.GameTag.FACTION):
                value = int(hsenums.Faction[value])
            elif tag == int(hsenums.GameTag.CARDRACE):
                value = int(hsenums.Race[value])
            elif tag == int(hsenums.GameTag.RARITY):
                value = int(hsenums.Rarity[value])
            elif tag == int(hsenums.GameTag.ZONE):
                value = int(hsenums.Zone[value])
            elif tag == int(hsenums.GameTag.MULLIGAN_STATE):
                value = int(hsenums.Mulligan[value])
            elif tag == int(hsenums.GameTag.STEP) or tag == int(hsenums.GameTag.NEXT_STEP):
                value = int(hsenums.Step[value])
            elif tag == int(hsenums.GameTag.PLAYSTATE):
                value = int(hsenums.PlayState[value])
            elif tag == int(hsenums.GameTag.STATE):
                value = int(hsenums.State[value])
            elif tag == int(hsenums.GameTag.CLASS):
                value = int(hsenums.CardClass[value])
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



