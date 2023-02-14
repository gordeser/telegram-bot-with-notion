from config import NOTION_API_TOKEN, CURRENCY_DATABASE_ID, EXPENSES_DATABASE_ID, CZK_PAGE_ID, RUB_PAGE_ID, EUR_PAGE_ID, \
    USD_PAGE_ID, INCOMES_DATABASE_ID

from datetime import datetime

import requests
import json

headers = {
    "Authorization": "Bearer " + NOTION_API_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}


def getAmountOfCurrencies():
    readUrl = f"https://api.notion.com/v1/databases/{CURRENCY_DATABASE_ID}/query"
    res = requests.request("POST", readUrl, headers=headers)
    data = res.json()
    currencies = {
        'USD': data['results'][0]['properties']['Remain']['formula']['number'],
        'RUB': data['results'][1]['properties']['Remain']['formula']['number'],
        'EUR': data['results'][2]['properties']['Remain']['formula']['number'],
        'CZK': data['results'][3]['properties']['Remain']['formula']['number']
    }
    return currencies


def addNewPage(database, name, currency, amount, comment):
    readUrl = f"https://api.notion.com/v1/pages"

    match currency:
        case 'CZK':
            curr = CZK_PAGE_ID
        case 'RUB':
            curr = RUB_PAGE_ID
        case 'EUR':
            curr = EUR_PAGE_ID
        case 'USD':
            curr = USD_PAGE_ID

    match database:
        case 'expense':
            page = EXPENSES_DATABASE_ID
        case 'income':
            page = INCOMES_DATABASE_ID

    data = json.dumps({
        "parent": {
            "database_id": page
        },
        "properties": {
            "Name of item": {
                "title": [{
                    "text": {
                        "content": name
                    }
                }]
            },
            "Amount": {
                "number": amount
            },
            "Currency": {
                "relation": [{
                    "id": curr
                }]
            },
            "Date": {
                "date": {
                    "start": datetime.today().isoformat() + '+01:00'
                }
            },
            "Comment": {
                "rich_text": [{
                    "text": {
                        "content": comment
                    }
                }]
            }
        }
    })
    req = requests.request("POST", readUrl, headers=headers, data=data)
    return req.json()['id']


def deletePage(page_id):
    url = f"https://api.notion.com/v1/blocks/{page_id}"
    req = requests.request("DELETE", url, headers=headers)
    return req
