#micropython script for Aquarium manager device NikitinMS 17.11.2019
import ssd1306
import time
import machine
import network
import utime
import ntptime

def connect(ssid, password): #подключение к wi-fi
  
  wifiled = machine.Pin(2, machine.Pin.OUT) #синий светодиод, должен загораться при успешном коннекте с wifi
  wifiled.value(0)
  station = network.WLAN(network.STA_IF)
 
  if station.isconnected() == True:
      tuple1 = station.ifconfig()
      ipold = tuple1[0]
      wifiled.value(1)
      return ipold
 
  station.active(True)
  station.connect(ssid, password)
 
  while station.isconnected() == False:
      pass
 
  tuple1 = station.ifconfig()
  ipold = tuple1[0]
  wifiled.value(1)
  return ipold

#определяем контакты подключения экрана и инициализируем его
res = machine.Pin(16)
dc = machine.Pin(17)
cs = machine.Pin(5)
spi1 = machine.SPI(2, baudrate=14500000, sck=machine.Pin(18), mosi=machine.Pin(23))
oled = ssd1306.SSD1306_SPI(128,64,spi1,dc,res,cs)

utc_shift = 3 #задать дельту временной зоны

# вызываем функцию коннекта к wi-fi и выводим ip на экран

try:
    ip = str(connect('Tensor', '87654321'))
except:
    oled.text('Error hz', 0, 0)
    oled.show()
    time.sleep(5)

#организуем синхронизацию и вывод времени на экран
rtc = machine.RTC()

def sync_time(): #пробуем синхронизировать время
    try:
        ntptime.settime()
        oled.fill(0)
        oled.show()
        oled.text('sync is succesful', 0, 10)
        oled.show()
        time.sleep(1)
    except Exception as ex:
        oled.fill(0)
        oled.show()
        oled.text('something went wrong', 0, 10)
        oled.show()
        time.sleep(15)
    else:
        oled.fill(0)
        oled.text('OK', 0, 10)
        oled.show()
        time.sleep(1)
    finally:
        oled.fill(0)
        oled.text('OK!', 0, 10)
        oled.show()
        time.sleep(1)
    
    tm = utime.localtime(utime.mktime(utime.localtime()) + utc_shift*3600)
    tm = tm[0:3] + (0,) + tm[3:6] + (0,)
    rtc.datetime(tm)
sync_time()

#выводим информацию на экран 1306 с обновлением часов
def update_oled():
    tim = rtc.datetime()
    year = str(tim[0])
    mon0 = str(tim[1])
    day0 = str(tim[2])
    hour0 = str(tim[4])
    min0 = str(tim[5])
    sec0 = str(tim[6])

    if int(mon0) < 10: #добавляем ноль, если меньше 10
        mon1 = str("0" + mon0)
        print(mon1)
    else:
        mon1 = mon0

    if int(day0) < 10: #добавляем ноль, если меньше 10
        day1 = str("0" + day0)
    else:
        day1 = day0

    if int(hour0) < 10: #добавляем ноль, если меньше 10
        hour1 = str("0" + hour0)
    else:
        hour1 = hour0

    if int(min0) < 10: #добавляем ноль, если меньше 10
        min1 = str("0" + min0)
    else:
        min1 = min0

    
    if int(sec0) < 10: #добавляем ноль, если меньше 10
        sec1 = str("0" + sec0)
    else:
        sec1 = sec0

    oled.text(ip, 0, 0)
    oled.text(hour1 + ":" + min1 + ":" + sec1, 0, 21)
    oled.text(day1 + "." + mon1 + "." + year, 0, 30)
    oled.show()
    oled.fill(0)
    time.sleep(1)

tcounter = 0
p1 = machine.Pin(27)
p1.init(p1.OUT)
p1.value(1)

def tcb(timer): #функция, выполняющаяся по коллбэку таймера
    update_oled()
    global tcounter
    if tcounter & 1:
        p1.value(0)
    else:
        p1.value(1)
    tcounter += 1
    if (tcounter % 10000) == 0:
        print("[tcb] timer: {} counter: {}".format(timer.timernum(), tcounter))

t1 = machine.Timer(2)
t1.init(period=1000, mode=t1.PERIODIC, callback=tcb)

def try_relay():
    ss1 = machine.Pin(25)
    ss2 = machine.Pin(26)
    ss1.init(ss1.OUT)
    ss2.init(ss2.OUT)
    while True:
        ss1.value(1)
        ss2.value(0)
        time.sleep(0.3)
        ss1.value(0)
        ss2.value(1)
    
#try_relay()