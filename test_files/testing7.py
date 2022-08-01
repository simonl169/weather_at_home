import json
import pandas as pd


#f = open("Sensor.txt", "r")


data = []

data = pd.read_csv('Sensor.txt', sep="\t", header=0)
data.columns = ["Time", "Temperature", "Humidity", "Pressure"]

print(data)



a = '24.5C'
a = a.replace('C','')
a = float(a)
print(a)