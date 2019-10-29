# This is your main script.
import ssd1306
import time
import machine
import network

def connect(): #подключение к wi-fi
  ssid = "Tensor"
  password =  "87654321"
 
  station = network.WLAN(network.STA_IF)
 
  if station.isconnected() == True:
      tuple1 = station.ifconfig()
      #print(tuple1[0])
      ipold = tuple1[0]
      
      return ipold
 
  station.active(True)
  station.connect(ssid, password)
 
  while station.isconnected() == False:
      pass
 
  tuple1 = station.ifconfig()
  ipold = tuple1[0]
  return ipold

#определяем контакты подключения экрана и инициализируем его
res = machine.Pin(16)
dc = machine.Pin(17)
cs = machine.Pin(5)
spi1 = machine.SPI(2, baudrate=14500000, sck=machine.Pin(18), mosi=machine.Pin(23))
oled = ssd1306.SSD1306_SPI(128,64,spi1,dc,res,cs)

# вызываем функцию коннекта к wi-fi и выводим ip на экран
oled.text(str(connect()), 0, 0)
oled.show()

'''#организуем синхронизацию и вывод времени на экран
rtc = machine.RTC()
rtc.init((2019,10,23,15,2,0,0,0))
#rtc.datetime()
#oled.text(rtc.now(), 0, 21)
oled.text('sync time...', 0, 0)
oled.show()
rtc.ntp_sync(server="hr.pool.ntp.org", tz="CET-1CEST,M3.5.0,M10.5.0/3")
oled.text('done!', 0, 0)
oled.show()
while True:
    tim = rtc.datetime()
    #print(tim)
    year = str(tim[0])
    month = str(tim[1])
    day = str(tim[2])
    hour = str(tim[4])
    minute = str(tim[5])
    second = str(tim[6])
    oled.text(str(connect()), 0, 0)
    oled.text(hour, 0, 21)
    oled.text(minute, 18, 21)
    oled.text(second, 36, 21)
    oled.show()
    oled.fill(0)
    time.sleep(1)'''
