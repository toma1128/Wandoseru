import json
import cv2
import requests
from pyzbar.pyzbar import decode
from picamera2 import Picamera2
import time
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

with open(schedule_path,"r",encoding="utf-8") as read_test:
    data = json.load(read_test)

# JSONデータをパース
records = data["records"]

# belongings_idとbelongings_nameのペアを動的に収集
belongings_pairs = {}
for record in records:
    for key, value in record.items():
        # belongings_idで始まるキーを探す
        if key.startswith("belongings_id"):
            # belongings_idをbelongings_nameに置き換えたキーを探す
            name_key = key.replace("id", "name")
            if name_key in record:
                # belongings_idとbelongings_nameのペアを辞書に追加
                belongings_pairs[value["value"]] = record[name_key]["value"]

def read_qr_code_from_camera():
    # カメラの初期化
    picam2 = Picamera2()
    config = picam2.create_preview_configuration()
    picam2.configure(config)
    picam2.start()

    print("QR START, Ctrl+C to END.")

    try:
        while True:
            # フレームをキャプチャ
            frame = picam2.capture_array()

            # フレームからQRコードをデコードする
            decoded_objects = decode(frame)
            for obj in decoded_objects:
                qr_code_data = obj.data.decode("utf-8")
                print("\nQRcode got : ")
                print("Type:", obj.type)
                print("Data:", qr_code_data)
                
                # QRコードのIDをチェックして対応する belongings_name の値を取得
                belongings_name_value = belongings_pairs.get(qr_code_data)
                if belongings_name_value:
                    print(f"It was {qr_code_data} torespond to {belongings_name_value}")
                else:
                    print(f"ID {qr_code_data} not respondo to belongings_name")

            # 短い遅延を入れて、CPUの使用率を下げる
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n end program")
    finally:
        # カメラを解放する
        picam2.stop()

if __name__ == '__main__':
    read_qr_code_from_camera()