# This is your main script.
import ssd1306
import time
from wifiConnect import connect
from machine import Pin, SPI

#определяем контакты подключения экрана и инициализируем его
res =Pin(16)
dc = Pin(17)
cs = Pin(5)
spi1 = SPI(2, baudrate=14500000, sck=Pin(18), mosi=Pin(23))
oled = ssd1306.SSD1306_SPI(128,64,spi1,dc,res,cs)

# вызываем функцию коннекта к wi-fi и выводим ip на экран
oled.text(str(connect()), 0, 0)
oled.show()