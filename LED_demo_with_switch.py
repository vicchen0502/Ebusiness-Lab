import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(20, GPIO.IN)

flag = False
for i in range(10):
  if GPIO.input(20) == 1:
    if flag == True:
      GPIO.output(2, GPIO.LOW)
      flag = False
      print('state:',GPIO.input(20),'light:flash(0)')
      time.sleep(1)
    else:
      GPIO.output(2,GPIO.HIGH)
      flag = True
      print('state:',GPIO.input(20),'light:flash(1)')
      time.sleep(1)
  else:
    GPIO.output(2,GPIO.HIGH)
    flag = True
    print('state:',GPIO.input(20),'light:keep')
    time.sleep(1)
GPIO.cleanup()
