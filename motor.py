import RPi.GPIO as GPIO
import time

RED_BTN = 17
BLUE_BTN = 27
GREEN_BTN = 22
RED_LED = 23
BLUE_LED = 24
GREEN_LED = 25

GPIO.setmode(GPIO.BCM)

#led,button setup
GPIO.setup(RED_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BLUE_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(GREEN_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(BLUE_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)

#MOTOR setup
GPIO.setup(12, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
MOTOR1 = GPIO.PWM(12, 20)
MOTOR2 = GPIO.PWM(13, 20)

def red_led_flicker():
  GPIO.output(RED_LED, 1)
  time.sleep(0.1)
  GPIO.output(RED_LED, 0)
  time.sleep(0.1)

def motor_cycle():
  MOTOR2.ChangeDutyCycle(0)
  for duty in range(0, 100, 5):
    MOTOR1.ChangeDutyCycle(duty)
    time.sleep(0.5)

def motor_stop():
  MOTOR1.ChangeDutyCycle(0)
  MOTOR2.ChangeDutyCycle(0)

def loop():
  try:

    start_get_qr = False  #QRコードを読み取るか
    bring_all_ok = False  #持ち物が全部読み取れたか
    is_camera_streaming = False   #カメラが動いているか
    start_motor = False
    stop_motor = False
    current_time = 0.0
    start_time = 0.0
    qr_data = None
    TIMEOUT = 10

    while(True):
      if start_get_qr == False:
        print("GREEN_BTN is Ready")
        start_get_qr = GPIO.input(GREEN_BTN)
      else:    #緑のボタンが押された時
        #カメラの初期化
        if is_camera_streaming == False:   #カメラがオンになっていない場合
          GPIO.output(GREEN_LED, 1)
          print("start QR module")
          # theCamera.begin(1, CAM_VIDEO_FPS_15, 
          #   CAM_IMGSIZE_QVGA_H, CAM_IMGSIZE_QVGA_V, CAM_IMAGE_PIX_FMT_RGB565)
          # theCamera.startStreaming(true, CamCB)
          start_time = time.time()
          is_camera_streaming = True

        elif current_time - start_time >= TIMEOUT and is_camera_streaming == True:   #カメラが止まっていないかつ,タイムアウトしたら
          GPIO.output(GREEN_LED, 0)
          print("QR end (error)")
          for i in range(2):
            red_led_flicker()
          #theCamera.end()
          is_camera_streaming = True;
        # 現在の時間を取得
        current_time = time.time()

        if qr_data == None:  #全件取得できた場合
          start_get_qr = False;
          bring_all_ok = True;
          GPIO.output(BLUE_LED, 1);

      if bring_all_ok:
        if start_motor != True:
          start_motor = GPIO.input(BLUE_BTN)
        else:  #青いボタンが押されたら
          motor_cycle()
          stop_motor = True
          if stop_motor != False :
            stop_motor = GPIO.input(RED_BTN)
          else:
            print("RED_BTN pressed")
            motor_stop()
            start_motor =True
      time.sleep(0.02)  #チャタリング防止
  finally:
    GPIO.cleanup()


loop()

GPIO.cleanup(RED_BTN)
GPIO.cleanup(BLUE_BTN)
GPIO.cleanup(GREEN_BTN)
GPIO.cleanup(RED_LED)
GPIO.cleanup(BLUE_LED)
GPIO.cleanup(GREEN_LED)