import requests
import json
import os

#スケジュールテーブル
headers = {
    'X-Cybozu-API-Token': '2o42utiugLff8j1aYaJ5RXt9yvJEEQfgl6rpWNTi',
}

params = {
    'app': '35',
}

response = requests.get('https://eiflga3pibge.cybozu.com/k/v1/records.json', params=params, headers=headers)

with open(schedule_path,"w",encoding="utf-8") as writeout:
    json.dump(response.json(),indent=3,fp=writeout,ensure_ascii=False)

print("スケジュールテーブルを取得しました")