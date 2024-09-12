import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

schedule_path = './json/schedule_result.json'
headers = {
    'X-Cybozu-API-Token': os.environ['TOKEN'],
}

params = {
    'app': os.environ['APP'],
}

response = requests.get('https://dw13zrg8vath.cybozu.com/k/v1/records.json', params=params, headers=headers)
with open(schedule_path,"w",encoding="utf-8") as writeout:
    json.dump(response.json(),indent=3,fp=writeout,ensure_ascii=False)

print("got json")