import requests
import json
import os
import datetime

weeks = 5 # 曜日数

today_week = datetime.datetime.today().weekday()

json_date_path = '../json/date_result.json'
subject_path = '../json/subject_result.json'
schedule_path = '../json/schedule_result.json'

#スケジュールテーブル
headers = {
    'X-Cybozu-API-Token': 'EOcLccRb6vLvtuo8xTlDHR5AwowWEW0nN36prqtB',
}

params = {
    'app': '35',
}

response = requests.get('https://eiflga3pibge.cybozu.com/k/v1/records.json', params=params, headers=headers)

with open(schedule_path,"w",encoding="utf-8") as writeout:
    json.dump(response.json(),indent=3,fp=writeout,ensure_ascii=False)

print("スケジュールテーブルを取得しました")


#曜日ごとの教科
if(not os.path.exists(json_date_path)):
    headers = {
        'X-Cybozu-API-Token': 'az29WJKQKd1cDJLA9KxcLyzVslw8mntg45dGh1BW',
    }

    params = {
        'app': '34',
    }

    response = requests.get('https://eiflga3pibge.cybozu.com/k/v1/records.json', params=params, headers=headers)

    with open(json_date_path,"w",encoding="utf-8") as writeout:
        json.dump(response.json(),indent=3,fp=writeout,ensure_ascii=False)

    print("曜日ごとの教科を取得しました")

#教科情報
if(not os.path.exists(subject_path)):
    headers = {
        'X-Cybozu-API-Token': 'SM9pQdxI7JZBWk3vXP7UkLOQGo2Sz7Jhg5oDarSB',
    }

    params = {
        'app': '33',
    }

    response2 = requests.get('https://eiflga3pibge.cybozu.com/k/v1/records.json', params=params, headers=headers)

    with open(subject_path,"w",encoding="utf-8") as writeout:
        json.dump(response2.json(),indent=3,fp=writeout,ensure_ascii=False)
    
    print("教科情報と持ち物を取得しました")

with open(json_date_path,"r",encoding="utf-8") as read_test:
    read_json = json.load(read_test)

with open(subject_path,"r",encoding="utf-8") as read_test:
    read_json2 = json.load(read_test)

with open(schedule_path,"r",encoding="utf-8") as read_test:
    read_json3 = json.load(read_test)

records = read_json['records']
records2 = read_json2['records']
records3 = read_json3['records']

subjects = {}

for record in records2:
    subject_id = record['教科ID']['value']
    bring_name = record['持ち物名']['value']
    bring_id = record['持ち物ID']['value']

    if (subject_id in subjects.keys()):
        subjects[subject_id]["brings"].append({
            "bring_name" : bring_name,
            "bring_id" : bring_id
        })
    else:
        subjects[subject_id] = {
            "info" : {
                "subject_name" : record['教科名']['value'],
                "subject_id" : subject_id
            },
            "brings" : [
                {
                    "bring_name" : bring_name,
                    "bring_id" : bring_id
                }
            ]
        }

with open('../json/subjects.json',"w",encoding="utf-8") as writeout:
    json.dump(subjects,indent=3,fp=writeout,ensure_ascii=False)

date = {}

for record in records:
    date_id = record['曜日ID']['value']
    date_name = record['曜日名']['value']

    subject_id = record['教科ID_参照用__0']['value']

    if (date_id in date.keys()):
        date[date_id][subject_id] = subjects[subject_id]
    else:
        date[date_id] = {
            "info" : {
                "date_name" : date_name,
                "date_id" : date_id,
            },
            subject_id : subjects[subject_id]
        }

schedules = {}

for record in records3:
    schedule_id = record['スケジュールID']['value']
    date_id = record['曜日ID']['value']
    date_name = record['曜日名']['value']

    if(schedule_id in schedules.keys()):
        schedules[schedule_id][date_id] = date[date_id]
    else:
        schedules[schedule_id] = {
            "info" : {
                "schedule_id" : schedule_id
            },
            date_id : date[date_id]
        }

with open('../json/total_result.json',"w",encoding="utf-8") as writeout:
    json.dump(schedules,indent=3,fp=writeout,ensure_ascii=False)

result = {}

keys_iterator = iter(schedules)

for i in range(0, weeks - today_week, 1):
    key = next(keys_iterator)

result = schedules[key]