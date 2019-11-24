#micropython script for Aquarium manager device NikitinMS 17.11.2019
import ssd1306
import time
import machine
import network
import utime
import ntptime
import wifi
from umqtt.simple import MQTTClient
import ubinascii

mqtt_server = 'tailor.cloudmqtt.com'
res = machine.Pin(16)
dc = machine.Pin(17)
cs = machine.Pin(5)
spi1 = machine.SPI(2, baudrate=14500000, sck=machine.Pin(18), mosi=machine.Pin(23))
oled = ssd1306.SSD1306_SPI(128,64,spi1,dc,res,cs)
utc_shift = 3 #задать дельту временной зоны
startTime = time.ticks_ms()
wifissid1 = 'Tensor'
wifipassword1 = '87654321'
wifissid2 = 'Tomato24'
wifipassword2 = '77777777'
relay1 = machine.Pin(25)
relay2 = machine.Pin(26)
mq_mess1 = 0

def disconnect():
    station = network.WLAN(network.STA_IF)
    if station.active():
        station.disconnect()
        station.active(False)
        oled.text('disconnected!', 0, 30)
        time.sleep(1)
        oled.fill(0)
        time.sleep(1)
def log(logs):
    oled.fill(0)
    oled.text(logs, 0, 50)
    oled.show()
    time.sleep(1)
def connect(ssid, password):
    log('connect start')
    station = network.WLAN(network.STA_IF) 
 
    if not station.active():
        station.active(True) 
  
    if station.isconnected():
        tuple1 = station.ifconfig()
        ipold = tuple1[0]
        return ipold
  
    try:
        station.connect(ssid, password)
        time.sleep(3)
        while station.isconnected() == False:
            if time.ticks_diff(time.ticks_ms(), startTime) > 15000:
                log("raise")
                raise PasswordError('Неверный пароль')
            log(str(time.ticks_diff(time.ticks_ms(), startTime)))
            #time.sleep_ms(1000)
        tuple1 = station.ifconfig()
        ipold = tuple1[0]
        return ipold
          
    except PasswordError:
        time.sleep_ms(1000)
        return '127.0.0.1' 
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
def sync_time():        #пробуем синхронизировать время
    try:
        ntptime.settime()
        #oled.fill(0)
        #oled.show()
        #oled.text('sync is succesful', 0, 10)
        #oled.show()
        time.sleep(1)
    except Exception as ex:
        #oled.fill(0)
        #oled.show()
        #oled.text('something went wrong', 0, 10)
        #oled.show()
        time.sleep(15)
    else:
        #oled.fill(0)
        #oled.text('OK', 0, 10)
        oled.show()
        time.sleep(1)
    finally:
        #oled.fill(0)
        #oled.text('OK!', 0, 10)
        oled.show()
        time.sleep(1)
    
    tm = utime.localtime(utime.mktime(utime.localtime()) + utc_shift*3600)
    tm = tm[0:3] + (0,) + tm[3:6] + (0,)
    rtc.datetime(tm)
def update_oled():      #выводим информацию на экран 1306 с обновлением часов
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
    #oled.text(str(rc), 0, 40)
    oled.show()
    oled.fill(0)
    time.sleep(1)
def tcb(timer):         #функция, выполняющаяся по коллбэку таймера
    update_oled()
    global tcounter
    if tcounter & 1:
        p1.value(0)
    else:
        p1.value(1)
    tcounter += 1
    if (tcounter % 10000) == 0:
        print("[tcb] timer: {} counter: {}".format(timer.timernum(), tcounter))

#disconnect()

ip = str(connect(wifissid1, wifipassword1))
if ip == '127.0.0.1':
    log('test')
    ip = str(connect(wifissid2, wifipassword2))
    log('test2')


rtc = machine.RTC()
sync_time()
tcounter = 0
p1 = machine.Pin(27)
p1.init(p1.OUT)
p1.value(1)
t1 = machine.Timer(2)
t1.init(period=1000, mode=t1.PERIODIC, callback=tcb)


client=MQTTClient(client_id='mihazi', server='tailor.cloudmqtt.com', port=15899, user='fwdgumzq', password='uWDiXJNmeB4e')


try:            
    client.connect()
except Exception as e:
    print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
    sys.exit()

client.publish('1', ip)

client_id = ubinascii.hexlify(machine.unique_id())
print(client_id)
topic_sub = b'notification'
topic_pub = b'hello'


#while mq_mess1 == 0:
client.publish(b"notification", b"hello")
#    client.publish(b"notification", b"hello")