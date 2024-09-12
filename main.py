import json
import cv2
from pyzbar.pyzbar import decode

# with open('./json/',"w",encoding="utf-8") as writeout:
#    json.dump(data,indent=3,fp=writeout,ensure_ascii=False)

print("START")
# 入力データ
data = '''{
   "records": [
      {
         "subject_id": {
            "type": "SINGLE_LINE_TEXT",
            "value": "01"
         },
         "レコード番号": {
            "type": "RECORD_NUMBER",
            "value": "2"
         },
         "更新者": {
            "type": "MODIFIER",
            "value": {
               "code": "liuyixiaopu@gmail.com",
               "name": "小浦琉以"
            }
         },
         "作成者": {
            "type": "CREATOR",
            "value": {
               "code": "liuyixiaopu@gmail.com",
               "name": "小浦琉以"
            }
         },
         "belongings_name_lookup": {
            "type": "SINGLE_LINE_TEXT",
            "value": "national_language_text"
         },
         "belongings_id_lookup1": {
            "type": "SINGLE_LINE_TEXT",
            "value": "001"
         },
         "$revision": {
            "type": "__REVISION__",
            "value": "1"
         },
         "更新日時": {
            "type": "UPDATED_TIME",
            "value": "2024-09-10T07:01:00Z"
         },
         "belongings_id2": {
            "type": "SINGLE_LINE_TEXT",
            "value": "002"
         },
         "belongings_id3": {
            "type": "SINGLE_LINE_TEXT",
            "value": "003"
         },
         "belongings_id4": {
            "type": "SINGLE_LINE_TEXT",
            "value": "004"
         },
         "subject_name": {
            "type": "SINGLE_LINE_TEXT",
            "value": "national_language"
         },
         "belongings_name4": {
            "type": "SINGLE_LINE_TEXT",
            "value": "national_language_ondoku"
         },
         "作成日時": {
            "type": "CREATED_TIME",
            "value": "2024-09-10T07:01:00Z"
         },
         "belongings_name2": {
            "type": "SINGLE_LINE_TEXT",
            "value": "national_language_note"
         },
         "belongings_name3": {
            "type": "SINGLE_LINE_TEXT",
            "value": "national_language_Kanji"
         },
         "$id": {
            "type": "__ID__",
            "value": "2"
         }
      }
   ],
   "totalCount": null
}'''

# JSONデータをパース
records = json.loads(data)["records"]

# belongings_idとbelongings_nameのペアを動的に収集
belongings_pairs = {}
for record in records:
    for key, value in record.items():
        if key.startswith("belongings_id"):
            name_key = key.replace("id", "name")
            if name_key in record:
                belongings_pairs[value["value"]] = record[name_key]["value"]

def read_qr_code_from_camera():
    # カメラの初期化
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("cannot open camera")
        return
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # フレームからQRコードをデコードする
        decoded_objects = decode(frame)
        for obj in decoded_objects:
            qr_code_data = obj.data.decode("utf-8")
            print("Type:", obj.type)
            print("Data:", qr_code_data)
            
            # QRコードのIDをチェックして対応する belongings_name の値を取得
            belongings_name_value = belongings_pairs.get(qr_code_data)
            if belongings_name_value:
                print(f"ID {qr_code_data} に対応する belongings_name の値は: {belongings_name_value}")
            else:
                print(f"ID {qr_code_data} に対応する belongings_name の値は見つかりませんでした。")

        # フレームを表示する
        cv2.imshow('QR Code Reader', frame)
        # 'q'キーが押されたらループを終了する
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break   
    # カメラとウィンドウを解放する
    cap.release()
    cv2.destroyAllWindows()

print("ok")

if __name__ == '__main__':
    read_qr_code_from_camera()
    print("main start")
