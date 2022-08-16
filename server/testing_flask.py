import logging
from time import sleep, strftime
import json
from urllib.parse import urlparse
import pandas as pd
import plotly.express as px
import plotly
from flask import Flask, render_template, request, url_for, flash, redirect, session, make_response
import os
from os.path import exists
from datetime import datetime
from datetime import timedelta




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
        
        if exists("%s.txt"% self.sensorName):
            f = open("%s.txt"% self.sensorName, "a")    
            f.write("\n")
            f.close()
            print("File already there, just appending")
        else:
            f = open("%s.txt"% self.sensorName, "w")
            f.write("Time \t Temperature \t Humidity \t Pressure \n")
            f.close()
            print("File not existing, create new...")
        
        
        


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
@app.route('/index')
def index():
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
    
    
@app.route('/history/<id>')
def history(id):

    id = int(id)
    filename = "%s.txt"% sensors_tuple[id].sensorName
    #print(filename)
    now = datetime.now() + timedelta(days = 1)
    today_string = now.strftime("%Y-%m-%d")
    three_days_ago = datetime.now() + timedelta(days = -3)
    start_string = three_days_ago.strftime("%Y-%m-%d")

    data = pd.read_csv(filename, sep="\t", header=0)
    data.columns = ["Time", "Temperature", "Humidity", "Pressure"]
    
    start_date = start_string
    end_date = today_string
    
    
    fig = px.line(data, x="Time", y="Temperature", title="Temperatur", markers=True)
    fig.update_layout(paper_bgcolor="#212121", font=dict(size=18, color="#dcdcdc"))
    fig.update_xaxes(type="date", range=[start_date, end_date])
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    
    fig2 = px.line(data, x="Time", y="Humidity", title="Rel. Luftfeuchtigkeit", markers=True)
    fig2.update_layout(paper_bgcolor="#212121", font=dict(size=18, color="#dcdcdc"))    
    fig2.update_xaxes(type="date", range=[start_date, end_date])
    graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    
    
    fig3 = px.line(data, x="Time", y="Pressure", title="Pressure", markers=True) 
    fig3.update_layout(paper_bgcolor="#212121", font=dict(size=18, color="#dcdcdc"))
    fig3.update_xaxes(type="date", range=[start_date, end_date])
    graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    
    print(request.args.get("current_page"))
    return render_template('sensor_history.html', graphJSON=graphJSON, graphJSON2=graphJSON2, graphJSON3=graphJSON3)   



@app.route('/get_info', methods=['GET'])
def get_info():
    content_type = request.headers.get('method')
    print(content_type)
    
    #id = int(id)
    id = 0
    filename = "%s.txt"% sensors_tuple[id].sensorName
    data = pd.read_csv(filename, sep="\t", header=0)
    data.columns = ["Time", "Temperature", "Humidity", "Pressure"]
    
    data2 = data.tail(1)
   
    
    
    response = app.response_class(
        response=data2.to_json( orient="values", lines=False),
        status=200,
        mimetype='application/json'
    )
    return response
    

@app.route('/get_date', methods=['GET'])
def get_date():
    now = datetime.now()
    today_string_date = now.strftime("%Y-%m-%d")
    
    
    response = app.response_class(
        response=today_string_date,
        status=200,
        mimetype='text/plain'
    )
    return response
    
@app.route('/get_time', methods=['GET'])
def get_time():
    now = datetime.now()
    today_string_time = now.strftime("%H:%M:%S")
    
    
    response = app.response_class(
        response=today_string_time,
        status=200,
        mimetype='text/plain'
    )
    return response
    
 
    

if __name__ == '__main__':

    
    app.run(host='192.168.42.209')
    
    
    