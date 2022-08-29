# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
import read_battery_voltage
from machine import deepsleep


read_battery_voltage.main()
