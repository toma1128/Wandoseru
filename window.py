import tkinter as tk
from PIL import Image, ImageTk

# メインウィンドウの作成
root = tk.Tk()
root.title("背景画像表示")

# スクリーンサイズを取得してウィンドウをフルスクリーンに設定
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}+0+0")

# スクリーンサイズに合わせて背景画像をリサイズ
bg_image = Image.open("images/wandoser.png")  # 任意の画像パス
bg_image = bg_image.resize((screen_width, screen_height))  # スクリーンサイズに合わせてリサイズ
bg_photo = ImageTk.PhotoImage(bg_image)

# キャンバスを作成して背景画像を表示
canvas = tk.Canvas(root, width=screen_width, height=screen_height)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# フルスクリーン表示にするための設定
root.attributes('-fullscreen', True)

# Tkinterのイベントループを開始
root.mainloop()