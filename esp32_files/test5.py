import urequests
import network
import time
import config
import connect_to_wifi
from machine import Pin, I2C
from time import sleep
import bme280
import machine


def main():
    
    i2c = machine.I2C(1, scl=Pin(22), sda=Pin(21), freq=10000)
    connect_to_wifi.connect_to_wifi()
    ip = connect_to_wifi.get_network_details()
    print(ip)

    p=0 
    # Making a POST request
    while True:
        bme = bme280.BME280(i2c=i2c)
        temp = bme.temperature
        hum = bme.humidity
        pres = bme.pressure
        # uncomment for temperature in Fahrenheit
        #temp = (bme.read_temperature()/100) * (9/5) + 32
        #temp = str(round(temp, 2)) + 'F'
        
        print('Temperature: ', temp)
        print('Humidity: ', hum)
        print('Pressure: ', pres)
        
        myobj = {'somekey': p, 'Sensor_Name' : config.SENSOR_NAME, 'Sensor IP' : str(ip), 'temperature' : temp, 'humidity' : hum, 'pressure' : pres}
        
        r = urequests.post("http://192.168.42.209:8080", json = myobj)
    # check status code for response received
    # success code - 200
        print(r)
        print(r.status_code)
        print(r.content)
        time.sleep(300)
        
        #if p>10:
            #break
        
    # print content of request
    #print(a)
if __name__ == '__main__':
    main()