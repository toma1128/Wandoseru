import json
import cv2
import requests
from pyzbar.pyzbar import decode
from picamera2 import Picamera2
import time
import os
from dotenv import load_dotenv
import tkinter as tk

load_dotenv()

schedule_path = './json/schedule_result.json'
headers = {
    'X-Cybozu-API-Token': os.environ['TOKEN'],
}

params = {
    'app': os.environ['APP'],
}

# カメラの初期化
picam2 = Picamera2()

labels = []     #ラベルの配列
actives = {}    #背景色の変更用の配列

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

#画面設定
# ボタンのスタイルを設定
def create_button(master, text, bg_color, row, column, width, height, command):
    button = tk.Button(master, text=text, font=("Arial", 12), bg=bg_color, relief="raised", bd=5, width=width, height=height, command=command)
    button.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
    return button

# メインウィンドウの作成
root = tk.Tk()
root.title("QR読み取りかいし")
root.geometry("600x400")  # 初期ウィンドウサイズ

root.config(bg='#3D3535')  # 背景色

def all_actives():
    return all(status == "active" for status in actives.values())

#motor start
def start():
    print("pressed start")
    if all_actives():
        print("OK")

#QRコードの読み取り関数
def read_qr():
    config = picam2.create_preview_configuration()
    picam2.configure(config)
    picam2.start()

    print("QR START, 15seconds timeout.")
    start_time = time.time()

    try:
        while True:
            current_time = time.time()
            if current_time - start_time > 15:
                print("\nTimeout")
                break

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
                    #QRコードが読み取れたら終了
                    actives[qr_code_data] = "active"
                    print(f"Updated actives: {actives}")

                    for i, (qr_id, name) in enumerate(belongings_pairs.items()):
                        status = actives.get(qr_id, "active")
                        change_color(labels[i], status)
                    
                    root.update()
                    return qr_code_data
                else:
                    print(f"ID {qr_code_data} not respondo to belongings_name")

            # 短い遅延を入れて、CPUの使用率を下げる
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\n end program")
    finally:
        # カメラを解放する
        picam2.stop()

#motor stop
def stop():
    print("pressed stop")
    if all_actives():
        print("OK")

# 上部のラベル（QRよみとりかいし）
label_top = tk.Label(root, text="QRよみとりかいし", font=("Arial", 14), bg='#DAD3CC', fg='black')
label_top.grid(row=0, column=0, columnspan=3, sticky="nsew", pady=10)

btn_start = create_button(root, "スタート", "#0000FF", 1, 1, 8, 4, start)  # 緑色（スタートボタン）
btn_read = create_button(root, "読み取り開始", "#00FF00", 2, 0, 8, 4, read_qr)  # 青色（読み取り開始ボタン）
btn_stop = create_button(root, "ストップ", "#FF0000", 2, 2, 8, 4, stop)  # 赤色（ストップボタン）

# 右側のラベルの状態を変更する関数
def change_color(label, status):
    if status == "active":
        label.config(bg="#00FF00")  # アクティブな場合は緑色
    else:
        label.config(bg="#F0ECE2")  # デフォルトの灰色

i = 1

for qr_id, text in belongings_pairs.items():
    label = tk.Label(root, text=text, font=("Arial", 12), bg="#F0ECE2", relief="raised", bd=5)
    label.grid(row=i, column=3, padx=10, pady=10, sticky="nsew")
    labels.append(label)
    actives[qr_id] = "inactive"
    i+=1

# 初期状態でラベルの色を設定
for i, (qr_id, name) in enumerate(belongings_pairs.items()):
    status = actives.get(qr_id, "inactive")
    change_color(labels[i], status)

# メインウィンドウの列と行のリサイズ設定
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)

if __name__ == '__main__':
    root.mainloop()