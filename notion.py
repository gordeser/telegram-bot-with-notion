from config import NOTION_API_TOKEN, CURRENCY_DATABASE_ID, EXPENSES_DATABASE_ID, CZK_PAGE_ID, RUB_PAGE_ID, EUR_PAGE_ID, \
    USD_PAGE_ID, INCOMES_DATABASE_ID, TASKLIST_DATABASE_ID

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
    readUrl = "https://api.notion.com/v1/pages"

    curr = None
    match currency:
        case 'CZK':
            curr = CZK_PAGE_ID
        case 'RUB':
            curr = RUB_PAGE_ID
        case 'EUR':
            curr = EUR_PAGE_ID
        case 'USD':
            curr = USD_PAGE_ID

    page = None
    category = False
    match database:
        case 'expense':
            page = EXPENSES_DATABASE_ID
            category = True
        case 'income':
            page = INCOMES_DATABASE_ID

    data = {
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
            "Comment": {
                "rich_text": [{
                    "text": {
                        "content": comment
                    }
                }]
            }
        }
    }
    if category:
        to_update = {
            'Category': {
                'multi_select': [{
                    'name': 'Uncategorized'
                }]
            }
        }
        data['properties'].update(to_update)
    req = requests.request("POST", readUrl, headers=headers, data=json.dumps(data))
    return req.json()['id']


def addNewInput(text):
    url = "https://api.notion.com/v1/pages"
    data = json.dumps({
        "parent": {
            "database_id": TASKLIST_DATABASE_ID
        },
        "properties": {
            "Name": {
                "title": [{
                    "text": {
                        "content": text
                    }
                }]
            },
            "Status": {
                "select": {
                    "name": "Inputs"
                }
            }
        }
    })
    req = requests.request("POST", url, headers=headers, data=data)
    return req.json()['id']


def deletePage(page_id):
    url = f"https://api.notion.com/v1/blocks/{page_id}"
    req = requests.request("DELETE", url, headers=headers)
    return req
