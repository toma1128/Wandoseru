import RPi.GPIO as GPIO
from time import sleep

# #MOTOR setup
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)
MOTOR = 14

while(True):
    GPIO.output(MOTOR, GPIO.HIGH)
    print("on")
    sleep(3)

    GPIO.output(MOTOR, GPIO.LOW )
    print("off")
    sleep(1)


# GPIO.setup(14, GPIO.OUT)
# LED = 14

# while(True):
#     GPIO.output(LED, GPIO.HIGH)
#     print("high")
#     sleep(1)
#     GPIO.output(LED, GPIO.LOW)
#     print("low")
#     sleep(1)