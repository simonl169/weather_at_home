import epaper2in13b
from machine import Pin,SPI
from time import sleep_ms

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
buf = bytearray(w * h // 8)
buf2 = bytearray(w * h // 8)
fb = framebuf.FrameBuffer(buf, w, h, framebuf.MONO_HLSB)
fb2 = framebuf.FrameBuffer(buf2, w, h, framebuf.MONO_HLSB)
black = 0
white = 1
fb.fill(white)
fb2.fill(white)

# --------------------

# write hello world with black bg and white text
#from image_dark import hello_world_dark

#print('Image dark')
#bufImage = hello_world_dark
#fbImage = framebuf.FrameBuffer(bufImage, 104, 212, framebuf.MONO_HLSB)
#fb.blit(fbImage, 20, 2)

#e.display_frame(buf, buf)

#sleep_ms(2000)  # wait for 2 seconds before doing a partial update

#print('Frame buffer things')
#fb.fill(white)
#rotate = 'ROTATE_90'
#e.set_rotate(rotate)
#fb.text('Hello World',10,10,black)

#e.display_frame(buf, buf2)

#sleep_ms(2000)


x=0; y=0; n=1; R=0

buf_black = bytearray(w * h // 8)
buf_red = bytearray(w * h // 8)

fb = framebuf.FrameBuffer(buf_black, h, w, framebuf.MONO_VLSB)
fb2 = framebuf.FrameBuffer(buf_red, h, w, framebuf.MONO_VLSB)
fb.fill(white)
fb.text('Simon\'s Weather Station!', 10, 10,black)
fb.text('Temperature: 28 C', 10, 30,black)
fb.text('Humidity: 50 %', 10, 50,black)
fb.text('Pressure: 1000 mbar', 10, 70,black)
fb2.fill(white)

buf_epaper_black = bytearray(w * h // 8)
buf_epaper_red = bytearray(w * h // 8)

for i in range(1, 14):
    for j in range(1, 213):
        R = (n-x)+((n-y)*12)
        buf_epaper_black[R-1] = buf_black[n-1]
        buf_epaper_red[R-1] = buf_red[n-1]
        n +=1
    x = n+i-1
    y = n-1

e.display_frame(buf_epaper_black, buf_epaper_red)
