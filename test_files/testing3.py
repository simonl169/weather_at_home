#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from time import sleep, strftime
import json
from urllib.parse import urlparse


class live():
    def __init__(self):
        self.live_temp = 'not set'
        self.live_hum = 'not set'
        self.live_pres = 'not set'
        

        

class S(BaseHTTPRequestHandler):
    


    sensor_1 = live()
    sensor_2 = live()
    
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
    
        url = urlparse(self.path)
        print(self.path)
        print("url: '%s' url.path: '%s'" % (url, url.path))
        
        
        myStr = url.path.replace('/', '')
        print("The string is:", myStr)
        myVars = locals()
        myVars.__setitem__(myStr, "pythonforbeginners.com")
        print("The variables are:")
        print(myVars)
        print(myStr)
    
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        #self.wfile.write("Current temperature =  {} \n".format(self.sensor_1.live_temp).encode('utf-8'))
        #self.wfile.write("Current humidity =  {} \t".format(self.sensor_1.live_hum).encode('utf-8'))
        #self.wfile.write("Current pressure =  {} \t".format(self.sensor_1.live_pres).encode('utf-8'))
        if self.path.endswith('/'):
            self.wfile.write("<html><head><title>Weather Station</title></head>".encode('utf-8'))
            self.wfile.write("<body><p>Sensor 1</p>".encode('utf-8'))
            self.wfile.write("<a href=http://192.168.42.209:8080/sensor_1>Sensor 1</a>".encode('utf-8'))
            self.wfile.write("</body></html>".encode('utf-8'))
            
        else:
            self.wfile.write("<html><head><title>Weather Station</title></head>".encode('utf-8'))
            self.wfile.write("<body><p>Sensor 1</p>".encode('utf-8'))
            self.wfile.write("<p>Current temperature =  {} <p>".format(self.sensor_1.live_temp).encode('utf-8'))
            self.wfile.write("<p>Current humidity =  {} <p>".format(self.sensor_1.live_hum).encode('utf-8'))
            self.wfile.write("<p>Current pressure =  {} <p>".format(self.sensor_1.live_pres).encode('utf-8'))
            self.wfile.write("<a href=http://192.168.42.209:8080>Home</a>".encode('utf-8'))
            self.wfile.write("</body></html>".encode('utf-8'))
        

        

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request2 for {}".format(self.path).encode('utf-8'))
        
        
        with open("./cpu_temp.csv", "a") as testfile:
            data_sensor = post_data.decode('utf-8')
            print(data_sensor)
            print(str(self.headers))
            
            
            y = json.loads(data_sensor)
            print(y['temperature'])
            self.sensor_1.live_temp = y['temperature']
            self.sensor_1.live_hum = y['humidity']
            self.sensor_1.live_pres = y['pressure']
            testfile.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(data_sensor)))
            
        

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO, filename='/home/pi/coding/weather/testGene.log')
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')

    print('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')
    print('Stopping httpd...\n')
    

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()