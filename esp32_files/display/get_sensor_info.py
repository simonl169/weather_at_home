import urequests
import connect_to_wifi
import json


def get_sensor_info(sensor_id):
    connect_to_wifi.connect_to_wifi()
    ip = connect_to_wifi.get_network_details()

    try:
        r = urequests.get("http://192.168.42.209:5000/get_info")
        #print(r.status_code)
        #print(r.content)
    
        response_dict = json.loads(r.content)
    
        #print(response_dict[0][1])
        #print(response_dict[0][2])
        #print(response_dict[0][3]) 

    except OSError as e:
        print('An error occured: ')
        print(e)
        return 
    except:
        print('Some other error')
        
        
    return r.status_code, response_dict

if __name__ == '__main__':
    sensor_id = 0
    response_status_code, sensor_response = get_sensor_info(sensor_id)
    print(response_status_code)
    print(sensor_response[0][1])
    print(sensor_response[0][2])
    print(sensor_response[0][3]) 