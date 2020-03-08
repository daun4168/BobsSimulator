import urllib.request
import xmltodict
import json
from os.path import join
import os
from urllib.error import HTTPError

# urllib.request.urlretrieve(다운로드 할 이미지 URL, 저장할 경로 및 파일명)

ROOT_DIR = os.getcwd()

card_name_dict = {}
CardDefs = open(join(ROOT_DIR, r"res\CardDefs.xml"), 'r', encoding='UTF8')

card_dict = xmltodict.parse(CardDefs.read())
card_dict = json.dumps(card_dict)
card_dict = json.loads(card_dict)

card_num = len(card_dict['CardDefs']['Entity'])
download_num = 0
recent_print_percent = 0
is_down_start = False
for card in card_dict['CardDefs']['Entity']:
    card_id = card['@CardID']

    if card_id == "TRL_059e":
        is_down_start = True

    if is_down_start:

        url = f"https://art.hearthstonejson.com/v1/512x/{card_id}.jpg"

        file_path = join(ROOT_DIR, f"res/cards/512x/{card_id}.jpg")
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            response = urllib.request.urlopen(req)
        except urllib.error.HTTPError:
            print(url)
            print(f'{card_id} - HTTP ERROR')
            continue
        with open(file_path, 'wb') as f:
            f.write(response.read())
        f.close()
        download_num += 1
        if recent_print_percent < download_num//card_num * 100:
            print(f"{download_num//card_num * 100}% - {download_num}/{card_num}")
            recent_print_percent = download_num//card_num * 100




