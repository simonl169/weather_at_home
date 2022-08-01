import network
import time
import config

station = network.WLAN(network.STA_IF)
station.active(True)

def connect_to_wifi():
    
    print(config.WIFI_SSID)
    
    
    def get_connection_status():
        connection_status = station.isconnected()
        print('test')
        return connection_status
        
    connection_status = get_connection_status()
    
    if connection_status == True:
        print('Already connected to Wifi')
        print('IP address: ' + station.ifconfig()[0])
        print('Gateway: ' + station.ifconfig()[2])
        print('DNS: ' + station.ifconfig()[3])
        print('Continuing...')
        return 0
    else:
        connection_try = 0
        
        while connection_try<4 and connection_status == False:
            
            
            if 4-connection_try > 0:
                print('Connecting to Wifi...')
                print('Try number: ' + str(connection_try+1) + ' ...')
                station.active(True)                
                try:
                    time.sleep(5)
                    station.connect(config.WIFI_SSID, config.WIFI_PASSWD)
                    #station.connect(WIFI_SSID, config.WIFI_PASSWD)
                    time.sleep(2)
                    
                except:
                    print('Could not connect to Wifi')
                    
                    
                
            else:
                print('Could not connect to Wifi, aborting...')
                return 0
            
            connection_status = get_connection_status()
            if connection_status == True:
                print('Connected')
                return 0
                
            connection_try += 1
            
            print('Retrying...')
            
            
        else:
            print('done...!')
       
    print('Continuing...')            

def get_network_details():
    #print('IP address: ' + station.ifconfig()[0])

    return station.ifconfig()[0]

if __name__ == '__main__':
    connect_to_wifi()
    
    
    
    
    
    
    
    
    
    
    
    
    

