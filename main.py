import json
import cv2
import requests
from pyzbar.pyzbar import decode
from picamera2 import Picamera2
import time
import os
from dotenv import load_dotenv
import tkinter as tk
import RPi.GPIO as GPIO

# #MOTOR setup
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)
MOTOR = 14

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
# メインウィンドウの作成
root = tk.Tk()
root.title("QR読み取りかいし")
root.attributes('-fullscreen', True)
root.geometry("1024x600")  # 初期ウィンドウサイズ
root.config(bg='#3D3535')  # 背景色


# フルスクリーンを解除する関数
def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))

# ESCキーでフルスクリーンを切り替え
root.bind('<Escape>', toggle_fullscreen)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}+0+0")

def all_actives():
    return all(status == "active" for status in actives.values())

#motor start
def start():
    print("pressed start")
    if all_actives():
        print("all OK")
        GPIO.output(MOTOR, GPIO.HIGH)
        print("on")

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
        print("all OK")
        GPIO.output(MOTOR, GPIO.LOW )
        print("off")

# ボタン作成関数（枠線をFrameで作成）
def create_button(master, bg_color, x, y, width, height, comment, command):
    # ボタンを包むフレームを作成し、白い枠線を追加
    frame = tk.Frame(master, bg="white", bd=15)
    frame.place(x=x, y=y, anchor="center")

    # ボタンを作成し、フレーム内に配置
    button = tk.Button(frame, text="", bg=bg_color, relief="raised", bd=5, 
                       width=width, height=height, command=command)
    button.pack()

    # コメント用ラベルをボタンのすぐ下に配置
    comment_label = tk.Label(master, text=comment, font=("Arial", 10, "bold"), fg="white", bg="#3A3A3A")
    comment_label.place(x=x, y=y + 100, anchor="n")  # 少し下にずらす

    return button

# 上部のラベル（QRよみとりかいし）
label_top = tk.Label(root, text="QRよみとりかいし", font=("Arial", 14), bg='#DAD3CC', fg='black')
label_top.place(x=512, y=35, anchor="n", width=550, height=50)

btn_start = create_button(root, "#0000FF", 350, 230, 13, 7,"スタート", start)  # 緑色（スタートボタン）
btn_read = create_button(root, "#00FF00", 200, 450, 13, 7, "読み取り開始", read_qr)  # 青色（読み取り開始ボタン）
btn_stop = create_button(root, "#FF0000", 500, 450, 13, 7, "ストップ", stop)  # 赤色（ストップボタン）

# 右側のラベルの状態を変更する関数
def change_color(label, status):
    if status == "active":
        label.config(bg="#00FF00")  # アクティブな場合は緑色
    else:
        label.config(bg="#F0ECE2")  # デフォルトの灰色

i = 1
y = [160, 265, 370, 475]

for qr_id, text in belongings_pairs.items():
    label = tk.Label(root, text=text, font=("Arial", 12), bg="#F0ECE2", relief="raised", bd=5)
    label.place(x=850, y=y[i-1], anchor="n", width=200, height=70)
    labels.append(label)
    actives[qr_id] = "inactive"
    i+=1

# 初期状態でラベルの色を設定
for i, (qr_id, name) in enumerate(belongings_pairs.items()):
    status = actives.get(qr_id, "inactive")
    change_color(labels[i], status)

if __name__ == '__main__':
    root.mainloop()