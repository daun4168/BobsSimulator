import xmltodict
import json

card_name_dict = {}
CardDefs = open(r'res/CardDefs.xml', 'r', encoding='UTF8')

card_dict = xmltodict.parse(CardDefs.read())
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


def card_name_by_id(card_id, lang='koKR'):
    if not card_id:
        return ""
    return card_name_dict[card_id][lang]

