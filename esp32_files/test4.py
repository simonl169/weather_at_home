import urequests
import network
import time
import config
import connect_to_wifi


ip = connect_to_wifi.get_network_details()

p=15

myobj = {'somekey': p, 'client ip' : str(ip)}
r = urequests.post("http://192.168.42.209:8080", json = myobj)
