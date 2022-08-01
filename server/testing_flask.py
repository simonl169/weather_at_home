import logging
from time import sleep, strftime
import json
from urllib.parse import urlparse
import pandas as pd
import plotly.express as px
import plotly
from flask import Flask, render_template, request, url_for, flash, redirect
import os


os.chdir('/home/pi/coding/weather')
print(os.getcwd())


app = Flask(__name__)
##---------------------------------------
class live():
    "This is a sensor class"
    live_temp = 'not set'
    live_hum = 'not set'
    live_pres = 'not set'
    last_update = 'not set'
    
    def __init__(self, sensor_data):

        self.sensorID = sensor_data['sensorID']
        self.sensorName = sensor_data['sensorName']
        self.sensorLocation = sensor_data['sensorLocation']
        self.sensorType = sensor_data['sensorType']
        self.sensorAPIKey = sensor_data['sensorAPIKey']
        f = open("%s.txt"% self.sensorName, "w")
        f.write("Time \t Temperature \t Humidity \t Pressure \n")
        f.close()

def convert_json_to_class(data):
    sensors = [0 for id in range(len(data['sensors']))]
    for id in range(len(data['sensors'])):
        #print(data['sensors'][id])
        sensors[id] = live(data['sensors'][id])
    return sensors
    
    
    
      
with open('sensors.json') as json_file:
    data = json.load(json_file)

sensors_tuple = convert_json_to_class(data)

##---------------------------------------------------------




      
        
@app.route('/')
def hello():
    #print(sensors_tuple[0].sensorLocation)
    
    #return 'Hello world'
    return render_template('index.html', list_of_sensors = sensors_tuple)
    
    

@app.route('/post_json', methods=['POST'])
def process_json():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
    
        json_data = request.get_json()
        api_key_received = json_data['API_KEY']
        
        if api_key_received in (obj.sensorAPIKey for obj in sensors_tuple):
            sensors_tuple[0].live_temp = json_data['temperature']
            sensors_tuple[0].live_hum = json_data['humidity']
            sensors_tuple[0].live_pres = json_data['pressure']        
            sensors_tuple[0].last_update = strftime("%Y-%m-%d %H:%M:%S")
            
            f = open("%s.txt"% sensors_tuple[0].sensorName, "a")
            f.write(sensors_tuple[0].last_update + "\t" + sensors_tuple[0].live_temp + "\t" + sensors_tuple[0].live_hum + "\t" + sensors_tuple[0].live_pres + "\n")
            f.close()
            
            return 'Weather data received and stored'
        else:
            return 'Invalid API Key provided'
      
    else:
        return 'Content-Type not supported!'
        
        
        
        
        
@app.route('/details/<id>')
def details(id):
    id = int(id)
    sensor_x = sensors_tuple[id]
    return render_template('sensor_detail.html', sensor_x = sensor_x) 
    
    
@app.route('/history')
def history():
    filename = "%s.txt"% sensors_tuple[0].sensorName
    #print(filename)
    

    data = pd.read_csv(filename, sep="\t", header=0)
    data.columns = ["Time", "Temperature", "Humidity", "Pressure"]
    
    fig = px.line(data, x="Time", y="Temperature", title="Temperatur", markers=True) 
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    fig2 = px.line(data, x="Time", y="Humidity", title="Rel. Luftfeuchtigkeit", markers=True) 
    graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('sensor_history.html', graphJSON=graphJSON, graphJSON2=graphJSON2)     

if __name__ == '__main__':

    
    app.run(host='192.168.42.209')