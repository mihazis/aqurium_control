# This is your main script.
from machine import Pin, SPI
import ssd1306
import time
#import network
import wifiConnect

res =Pin(16)
dc = Pin(17)
cs = Pin(5)
spi1 = SPI(2, baudrate=14500000, sck=Pin(18), mosi=Pin(23))
oled = ssd1306.SSD1306_SPI(128,64,spi1,dc,res,cs)
p = 1

'''while True:
    for s in range(0, 12):
        for p in range(0, 12):
            p += 1
            #oled.fill(1)
            oled.fill(0) #пока в роли очистки
            oled.text("TEXT", s*6, p*4)
            oled.pixel(0, 0, 1)
            time.sleep(0.2)
            oled.invert(True)
            oled.show()'''

oled.fill(1)
oled.text("TEXT", 40, 40)
oled.show()
#wifiConnect.connect()upip.install('micropython-uasyncio')