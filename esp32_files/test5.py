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
    print('Executing weather station')
    i2c = machine.I2C(1, scl=Pin(22), sda=Pin(21), freq=10000)
    connect_to_wifi.connect_to_wifi()
    ip = connect_to_wifi.get_network_details()
    print(ip)


    # Making a POST request
    while True:
        bme = bme280.BME280(i2c=i2c)
        temp = bme.temperature
        hum = bme.humidity
        pres = bme.pressure
    
        temp = temp.replace('C','')
        hum = hum.replace('%','')
        pres = pres.replace('hPa','')
        # uncomment for temperature in Fahrenheit
        #temp = (bme.read_temperature()/100) * (9/5) + 32
        #temp = str(round(temp, 2)) + 'F'
        
        print('Temperature: ', temp)
        print('Humidity: ', hum)
        print('Pressure: ', pres)
        
        myobj = {'API_KEY': config.API_KEY, 'sensor_name' : config.SENSOR_NAME, 'sensor_ip' : str(ip), 'sensor_location': config.SENSOR_LOC, 'temperature' : temp, 'humidity' : hum, 'pressure' : pres}
        
    #r = urequests.post("http://192.168.42.209:8080", json = myobj)
        try:
            r = urequests.post("http://192.168.42.209:5000/post_json", json = myobj)
            print(r.status_code)
            print(r.content)
        except OSError as e:
            print('An error occured: ')
            print(e)
        except:
            print('Some other error')
    # check status code for response received
    # success code - 200


        time.sleep(300)

        #if p>10:
            #break
        
    # print content of request
    #print(a)
if __name__ == '__main__':
    print('Executing weather station as main')
    main()