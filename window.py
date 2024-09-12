import tkinter as tk

# メインウィンドウの作成
root = tk.Tk()
root.title("QR読み取りかいし")
root.geometry("600x400")  # 初期ウィンドウサイズ

root.config(bg='#3D3535')  # 背景色

# ボタンを押したときの関数
def start():
    print("スタートボタンが押されました")

def read():
    print("読み取り開始ボタンが押されました")

def stop():
    print("ストップボタンが押されました")

# ボタンのスタイルを設定
def create_button(master, text, bg_color, row, column, width, height):
    button = tk.Button(master, text=text, font=("Arial", 12), bg=bg_color, relief="raised", bd=5, width=width, height=height)
    button.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
    return button

# 上部のラベル（QRよみとりかいし）
label_top = tk.Label(root, text="QRよみとりかいし", font=("Arial", 14), bg='#DAD3CC', fg='black')
label_top.grid(row=0, column=0, columnspan=3, sticky="nsew", pady=10)

# ボタンの配置と色を画像通りに設定
btn_start = create_button(root, "スタート", "#0000FF", 1, 1, 8, 4)  # 緑色（スタートボタン）
btn_read = create_button(root, "読み取り開始", "#00FF00", 2, 0, 8, 4)  # 青色（読み取り開始ボタン）
btn_stop = create_button(root, "ストップ", "#FF0000", 2, 2, 8, 4)  # 赤色（ストップボタン）

# 右側のラベルの状態を変更する関数
def change_color(label, status):
    if status == "active":
        label.config(bg="#00FF00")  # アクティブな場合は緑色
    else:
        label.config(bg="#F0ECE2")  # デフォルトの灰色

# 右側のラベル（教科書、ノート、ドリル、カード）
label_kyoukasho = tk.Label(root, text="教科書", font=("Arial", 12), bg="#F0ECE2", relief="raised", bd=5)
label_note = tk.Label(root, text="ノート", font=("Arial", 12), bg="#F0ECE2", relief="raised", bd=5)
label_drill = tk.Label(root, text="ドリル", font=("Arial", 12), bg="#F0ECE2", relief="raised", bd=5)
label_card = tk.Label(root, text="カード", font=("Arial", 12), bg="#F0ECE2", relief="raised", bd=5)

# 右側ラベルの配置 (ウィンドウのリサイズに対応)
label_kyoukasho.grid(row=1, column=3, sticky="nsew", padx=10, pady=10)
label_note.grid(row=2, column=3, sticky="nsew", padx=10, pady=10)
label_drill.grid(row=3, column=3, sticky="nsew", padx=10, pady=10)
label_card.grid(row=4, column=3, sticky="nsew", padx=10, pady=10)

# サンプルで色を変える（判定後に変更）
change_color(label_kyoukasho, "active")  # 教科書のラベルをアクティブ状態に
change_color(label_note, "inactive")     # ノートのラベルを非アクティブ状態に
change_color(label_drill, "inactive")    # ドリルのラベルを非アクティブ状態に
change_color(label_card, "inactive")     # カードのラベルを非アクティブ状態に

# メインウィンドウの列と行のリサイズ設定
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)

# Tkinterのイベントループを開始
root.mainloop()