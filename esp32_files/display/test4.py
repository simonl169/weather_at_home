import urequests
import network
import time
import config
import connect_to_wifi
from machine import Pin, I2C
from time import sleep
import json

connect_to_wifi.connect_to_wifi()
ip = connect_to_wifi.get_network_details()
print(ip)


        
#r = urequests.post("http://192.168.42.209:8080", json = myobj)
try:
    r = urequests.get("http://192.168.42.209:5000/get_info")
    print(r.status_code)
    print(r.content)
    
    response_dict = json.loads(r.content)
    
    print(response_dict[0][1])
    print(response_dict[0][2])
    print(response_dict[0][3])  
    

except OSError as e:
    print('An error occured: ')
    print(e)
except:
    print('Some other error')
