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
    def getCurrencyRemain(currency):
        readUrl = f"https://api.notion.com/v1/pages/{currency}/properties/eue%7C"
        res = requests.request("GET", readUrl, headers=headers)
        data = res.json()
        return data['formula']['number']

    currencies = {
        'USD': getCurrencyRemain(USD_PAGE_ID),
        'RUB': getCurrencyRemain(RUB_PAGE_ID),
        'EUR': getCurrencyRemain(EUR_PAGE_ID),
        'CZK': getCurrencyRemain(CZK_PAGE_ID)
    }

    return currencies


def addNewPage(database, name, currency, amount, comment):
    readUrl = "https://api.notion.com/v1/pages"

    curr = None
    if currency == 'CZK':
        curr = CZK_PAGE_ID
    elif currency == 'RUB':
        curr = RUB_PAGE_ID
    elif currency == 'EUR':
        curr = EUR_PAGE_ID
    elif currency == 'USD':
        curr = USD_PAGE_ID

    page = None
    category = False
    if database == "expense":
        page = EXPENSES_DATABASE_ID
        category = True
    elif database == "income":
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
