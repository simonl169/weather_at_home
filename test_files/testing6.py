import json



class live():
    "This is a sensor class"
    live_temp = 'not set'
    live_hum = 'not set'
    live_pres = 'not set'
    
    def __init__(self, sensor_data):

        self.sensorID = sensor_data['sensorID']
        self.sensorName = sensor_data['sensorName']
        self.sensorLocation = sensor_data['sensorLocation']
        self.sensorType = sensor_data['sensorType']
        self.sensorAPIKey = sensor_data['sensorAPIKey']
        

def convert_json_to_class(data):
    sensors = [0 for id in range(len(data['sensors']))]
    for id in range(len(data['sensors'])):
        #print(data['sensors'][id])
        sensors[id] = live(data['sensors'][id])
    return sensors
    
    
    
      
with open('sensors.json') as json_file:
    data = json.load(json_file)
    
    
    #data = data['sensors']
    


for id in range(len(data['sensors'])):
    print(id)
    #print(data['sensors'][id])
    
    
    
sensors_tuple = convert_json_to_class(data)
print('hello')
print(sensors_tuple[1].live_temp)

#sensor_1 = live(data['sensors'][0])

for id in range(len(sensors_tuple)):
    print(sensors_tuple[id].sensorAPIKey)

Key = "8pnNdoln"





if Key in (obj.sensorAPIKey for obj in sensors_tuple):
    print('yes')
else:
    print('no')



#sensor_1 = live()
#sensor_2 = live()        


#a = [sensor_1, sensor_2]


#for sensor_x in a:
    
 #   print(a[0].live_temp)