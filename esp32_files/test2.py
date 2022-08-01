import urequests
import network
import time
import config
import connect_to_wifi


connect_to_wifi.connect_to_wifi()
ip = connect_to_wifi.get_network_details()
print(ip)

p=0 
# Making a POST request
while True:
    myobj = {'somekey': p, 'client ip' : str(ip)}
    r = urequests.post("http://192.168.42.209:8080", json = myobj)
    p = p+1
# check status code for response received
# success code - 200
    print(r)
    print(r.status_code)
    print(r.content)
    time.sleep(3)
    
    if p>10:
        break
    
# print content of request
#print(a)