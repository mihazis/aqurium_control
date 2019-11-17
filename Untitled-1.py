import time
WIFI_CONNECTION_WAIT_PERIOD_MS = 25000

def connectToWiFi():
 print('Enter connection Wi-Fi procedure')
 if sta_if.active():
  print('Reset activity')
  sta_if.active(False)
  time.sleep(1)
 sta_if.active(True)
 sta_if.connect("SSID","PASS")
 start = time.ticks_ms()
 while not sta_if.isconnected():
  if time.ticks_diff(time.ticks_ms(), start) > WIFI_CONNECTION_WAIT_PERIOD_MS:
   print('Connection to Wi-Fi timeout.')
   return