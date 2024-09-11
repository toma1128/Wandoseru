import requests
import json
import os
import sys

config_path = "/home/uuutomauuu/Desktop/conf/config.py"
sys.path.append(os.path.dirname(config_path))

import config

with open(config.schedule_path,"w",encoding="utf-8") as writeout:
    json.dump(config.response.json(),indent=3,fp=writeout,ensure_ascii=False)

print("スケジュールテーブルを取得しました")