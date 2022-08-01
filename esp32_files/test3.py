import time
from machine import Pin

led = Pin(25, Pin.OUT)

while True:
    led.value(not led.value())
    time.sleep(1.0)
    print('test')