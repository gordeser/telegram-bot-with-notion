from config import NOTION_API_TOKEN, DATABASE_ID

import requests
import json

headers = {
    "Authorization": "Bearer " + NOTION_API_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22"
}


def readDatabase():
    readUrl = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    res = requests.request("POST", readUrl, headers=headers)
    data = res.json()
    print(res.status_code)

    with open('./full-properties.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False)
    return data


db = readDatabase()
usd_amount = db['results'][0]['properties']['Remain']['formula']['number']
rub_amount = db['results'][1]['properties']['Remain']['formula']['number']
eur_amount = db['results'][2]['properties']['Remain']['formula']['number']
czk_amount = db['results'][3]['properties']['Remain']['formula']['number']
