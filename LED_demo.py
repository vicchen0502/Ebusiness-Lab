import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT, initial=GPIO.LOW)

flag = False
for i in range(10):
  if flag == True:
    GPIO.output(2, GPIO.LOW)
    flag = False
    time.sleep(1)
  else:
    GPIO.output(2,GPIO.HIGH)
    flag = True
    time.sleep(1)
GPIO.cleanup()
