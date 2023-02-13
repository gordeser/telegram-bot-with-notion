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


readDatabase()
