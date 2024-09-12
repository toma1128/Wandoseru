import tkinter as tk
from PIL import Image, ImageTk

# メインウィンドウの作成
root = tk.Tk()
root.title("背景画像表示")
root.geometry("900x500")  # ウィンドウサイズを設定

# 画像を読み込んで背景に設定
bg_image = Image.open("images/wandoser.png")  # 任意の画像パス
bg_image = bg_image.resize((900, 500))  # ウィンドウに合わせてリサイズ
bg_photo = ImageTk.PhotoImage(bg_image)

# キャンバスを作成して背景画像を表示
canvas = tk.Canvas(root, width=500, height=500)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Tkinterのイベントループを開始
root.mainloop()