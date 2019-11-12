import machine
import network
from time import sleep

def connect(ssid, password): #подключение к wi-fi import wifi
  
  wifiled = machine.Pin(2, machine.Pin.OUT) #синий светодиод, должен загораться при успешном коннекте с wifi
  wifiled.value(0)
  station = network.WLAN(network.STA_IF)
 
  if station.isconnected() == True:
      tuple1 = station.ifconfig()
      ipold = tuple1[0]
      wifiled.value(1)
      return ipold
 
  station.active(True)
  print("до")
  station.connect(ssid, password) #   wifi.connect('Tensor', '876543210')
  while station.isconnected() == False:
      pass
 
  tuple1 = station.ifconfig()
  ipold = tuple1[0]
  wifiled.value(1)
  return ipold

def disconnect():
    station = network.WLAN(network.STA_IF)
    if station.isconnected() == True:
        station.active(False)
        wifiled = machine.Pin(2, machine.Pin.OUT)
        wifiled.value(0)
    else:
        return "already disconnected"

def status():
    station = network.WLAN(network.STA_IF)
    if station.isconnected() == True:
        print('connected')
    else:
        print('disconnected')

