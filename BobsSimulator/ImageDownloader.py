import urllib.request
import xmltodict
import json
import shutil
from os.path import join
import os
from urllib.error import HTTPError
import hearthstone_data


carddefs_path = hearthstone_data.get_carddefs_path()
carddefs_version = int(float(hearthstone_data.__version__))
RES = '256x'

print(f'version: {carddefs_version}')

ROOT_DIR = os.getcwd()

card_dict = {}

card_defs = open(carddefs_path, 'r', encoding='UTF8')
card_dict = xmltodict.parse(card_defs.read())
card_defs.close()

card_dict = json.dumps(card_dict)
card_dict = json.loads(card_dict)

card_num = len(card_dict['CardDefs']['Entity'])
try_num = 0
recent_print_percent = 0

no_file_path = join(ROOT_DIR, f"res/img/cards/{RES}/no_img_{RES}.jpg")

for card in card_dict['CardDefs']['Entity']:
    try_num += 1
    print(f'{try_num}/{card_num}')
    card_id = card['@CardID']

    file_path = join(ROOT_DIR, f"res/img/cards/{RES}/{card_id}.jpg")

    if os.path.isfile(file_path):
        print(f'Already Exist: {card_id}')
        continue

    url = f"https://art.hearthstonejson.com/v1/{RES}/{card_id}.jpg"

    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urllib.request.urlopen(req)
    except urllib.error.HTTPError:
        print(f'HTTP Error: {card_id}')
        shutil.copy(no_file_path, file_path)
        continue
    with open(file_path, 'wb') as f:
        print(f'Success: {card_id}')
        f.write(response.read())
    f.close()





