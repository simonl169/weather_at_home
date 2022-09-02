import urequests
import network
import time
import config
import connect_to_wifi
from machine import Pin, I2C, ADC
from time import sleep
import bme280
import machine


def read_voltage(GPIO_PIN):
    pot = ADC(Pin(GPIO_PIN))
    pot.atten(ADC.ATTN_11DB)
    #ADC.ATTN_0DB — the full range voltage: 1.2V
    #ADC.ATTN_2_5DB — the full range voltage: 1.5V
    #ADC.ATTN_6DB — the full range voltage: 2.0V
    #ADC.ATTN_11DB Full range: 3.3v
    
    pot_value = pot.read()  
    volts = pot_value*3.3/4095
    
    return pot_value, volts



def main():
    print('Executing weather station')
    i2c = machine.I2C(1, scl=Pin(22), sda=Pin(21), freq=10000)
    connect_to_wifi.connect_to_wifi()
    ip = connect_to_wifi.get_network_details()
    print(ip)
    
    int_id = config.SENSOR_ID


    # Making a POST request
    while True:
        bme = bme280.BME280(i2c=i2c)
        temp = bme.temperature
        hum = bme.humidity
        pres = bme.pressure
        bit_value, volts = read_voltage(34)
    
        temp = temp.replace('C','')
        hum = hum.replace('%','')
        pres = pres.replace('hPa','')
        # uncomment for temperature in Fahrenheit
        #temp = (bme.read_temperature()/100) * (9/5) + 32
        #temp = str(round(temp, 2)) + 'F'
        
        print('Temperature: ', temp)
        print('Humidity: ', hum)
        print('Pressure: ', pres)
        print('3.3V Value: ', volts)
        
        myobj = {'API_KEY': config.API_KEY,'SENSOR_ID': config.SENSOR_ID, 'sensor_name' : config.SENSOR_NAME, 'sensor_ip' : str(ip), 'sensor_location': config.SENSOR_LOC, 'temperature' : temp, 'humidity' : hum, 'pressure' : pres, 'volts' : volts}
        
        request_url = "http://192.168.42.209:5000/post_json/" + str(config.SENSOR_ID)
        #print(request_url)
    #r = urequests.post("http://192.168.42.209:8080", json = myobj)
        try:
            r = urequests.post(request_url, json = myobj)
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