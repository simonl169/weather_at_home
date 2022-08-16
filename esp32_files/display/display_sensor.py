import epaper2in13b
from machine import Pin,SPI
from time import sleep_ms
from writer import Writer
import freesans14
import urequests
import network
import time
import config
import connect_to_wifi
import get_sensor_info





connect_to_wifi.connect_to_wifi()
ip = connect_to_wifi.get_network_details()
print(ip)

sck = Pin(18)
miso = Pin(19)
mosi = Pin(23)
dc = Pin(17)
cs = Pin(5)
rst = Pin(16)
busy = Pin(4)
spi = SPI(2, baudrate=20000000, polarity=0, phase=0, sck=sck, miso=miso, mosi=mosi)







e = epaper2in13b.EPD(spi, cs, dc, rst, busy)
e.init()

w = 104
h = 212
x = 0
y = 0

import framebuf

print("Screen ready")


buf = bytearray(w * h // 8)
fb = framebuf.FrameBuffer(buf, h, w, framebuf.MONO_VLSB)

buf2 = bytearray(w * h // 8)
fb2 = framebuf.FrameBuffer(buf2, h, w, framebuf.MONO_VLSB)


black = 0
white = 1

fb.fill(white)
fb2.fill(white)


class NotionalDisplay(framebuf.FrameBuffer):
    def __init__(self, width, height, buffer, linespace, indentspace):
        self.width = width
        self.height = height
        self.buffer = buffer
        self.mode = framebuf.MONO_VLSB
        self.linespacing = linespace
        self.indentspacing = indentspace
        super().__init__(self.buffer, self.width, self.height, self.mode)

    def show(self):
        ...


my_display = NotionalDisplay(212, 104, buf, 5, 5)
my_display2 = NotionalDisplay(212, 104, buf2, 5, 5)

wri = Writer(my_display, freesans14)


# verbose = False to suppress console output
Writer.set_textpos(my_display, 5, 5) # row, col

print("Collecting data...")



response_status_code, sensor_response = get_sensor_info.get_sensor_info(0)

try:
    date_response = urequests.get("http://192.168.42.209:5000/get_date")
except:
    print('Error time')

try:
    time_response = urequests.get("http://192.168.42.209:5000/get_time")
except:
    print('Error time')
    
date_string = str(date_response.text)
time_string = str(time_response.text)
date_time_string = "Date: " + date_string + "\t" + time_string + "\n"

temperature_string = "Temp: " + str(sensor_response[0][1]) + " C\n"
humidity_string = "Humidity: " + str(sensor_response[0][2]) + " %\n"
pressure_string = "Pressure: " + str(sensor_response[0][3]) + " hPa"

#wri.printstring('Date: 12 Aug 2018, 10:30\n')
#wri.printstring('Time: 2022-08-16\t16:57:58\n')

print("printing...")
wri.printstring(date_time_string)
wri.printstring('Sensor: Balkon\n')
wri.printstring(temperature_string)
wri.printstring(humidity_string)
wri.printstring(pressure_string)

my_display2.show()
my_display.show()

#e.display_frame(buf, buf2)


buf_black = bytearray(w * h // 8)
buf_red = bytearray(w * h // 8)

fb = framebuf.FrameBuffer(buf_black, h, w, framebuf.MONO_VLSB)
fb2 = framebuf.FrameBuffer(buf_red, h, w, framebuf.MONO_VLSB)

#fb.fill(white)
#fb.text('Simon', 10, 10,black)
#fb2.fill(white)

buf_epaper_black = bytearray(w * h // 8)
buf_epaper_red = bytearray(w * h // 8)

x=0; y=0; n=1; R=0

for i in range(1, 14):
    for j in range(1, 213):
        R = (n-x)+((n-y)*12)
        buf_epaper_black[R-1] = buf[n-1]
        buf_epaper_red[R-1] = buf2[n-1]
        n +=1
    x = n+i-1
    y = n-1


e.display_frame(buf_epaper_black, buf_epaper_red)
