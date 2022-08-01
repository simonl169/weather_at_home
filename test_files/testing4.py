import json


with open('sensors.json') as json_file:
    data = json.load(json_file)
    #data = data['sensors']
    print(data)
    
    


print(data['sensors'][0].keys())
#print(data['numberOfSensors'])

for id in range(2):
    print(id)
    print(data['sensors'][id]['sensorName'])
    
#x = range(3, 6)
#for n in x:
#  print(n) 