class live():
    def __init__(self):
        self.live_temp = 'not set'
        self.live_hum = 'not set'
        self.live_pres = 'not set'




sensor_1 = live()
sensor_2 = live()        


a = [sensor_1, sensor_2]


for sensor_x in a:
    
    print(a[0].live_temp)