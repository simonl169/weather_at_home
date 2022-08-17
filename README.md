# Weather station using ESP32 as sensor and Raspberry Pi 4 as server

## Idea
The idea of this project is to gather athmosphere data as temperature, pressure and humidity from various sensors (and or websites) and store them centrally on a Raspi 4, which then serves the data on a webserver.
The other point is for me to start some advanced Python and get familiar with Git/Github

## Goals
The goal is, to have as many sensors or data inputs as you want and have access to the data via the browser. Also, we need a nice graph and comparison between the sensors.
The whole project is meant to run on your own local hardware, so nothing has to communicate with the web. At some point, I wanna also try an use docker to run it on my home server, not just the raspberry pi.


## What's the status?
Right now, I have the following working:
- Server on Raspberry Pi receiving and serving the data
- ESP32 ready to collect data via a BME280 and send to raspberry via Wifi
- Graph view of individual sensors
- foundation to extend to more sensors, also of different type (module and sensor itself)
- ESP32 with wavesahre ePaper display as additional data display

![This is an image](https://github.com/simonl169/weather_at_home/blob/main/docs/temperature_history_exampl.PNG)


## What's missing?
- the docker part
- a bigger ePaper (have to buy one)
- clean up code
- add more physical sensors
- have some nice housing for the sensors
- power supply for the sensors (right now running via my old phone charger)
- PCB to fit everything into a housing
