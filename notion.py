from config import NOTION_API_TOKEN, DATABASE_ID

import requests
import json

headers = {
    "Authorization": "Bearer " + NOTION_API_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22"
}


def getAmountOfCurrencies():
    readUrl = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    res = requests.request("POST", readUrl, headers=headers)
    data = res.json()
    currencies = {
        'USD': data['results'][0]['properties']['Remain']['formula']['number'],
        'RUB': data['results'][1]['properties']['Remain']['formula']['number'],
        'EUR': data['results'][2]['properties']['Remain']['formula']['number'],
        'CZK': data['results'][3]['properties']['Remain']['formula']['number']
    }
    return currencies

