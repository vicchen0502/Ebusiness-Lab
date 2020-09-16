import Adafruit_DHT,time
while True:
  h, t = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4)
  print('濕度為',h,',溫度為',t,'℃')
  time.sleep(1)
