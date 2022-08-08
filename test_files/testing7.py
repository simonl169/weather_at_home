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


from os.path import exists


if exists("./Sensor 1.txt"):
    f = open("./Sensor 1.txt", "a")    
    f.write("hello \n hello")
    f.close()
    print("1")
else:
    f = open("./Sensor 1.txt", "w")
    f.write("Time \t Temperature \t Humidity \t Pressure \n")
    f.close()
    print("2")

