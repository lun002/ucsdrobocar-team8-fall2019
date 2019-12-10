import serial
import pynmea2
import time
 
port = "/dev/ttyACM1"
serialPort = serial.Serial(port, baudrate = 9600, timeout = 0.01)
port2 = "/dev/ttyACM0"
serialPort2 = serial.Serial(port2, baudrate = 9600, timeout = 0.01)

class GPS:
    def __init__(self):
        self.coord1 = (33.881927, -117.235508)
        self.running = True
        self.Kalman_bool = True

    def read(self):
        gps_data = serialPort.readline()
        gps_str = gps_data.decode("utf-8")
        if gps_str.find('GGA') > 0:
            msg = pynmea2.parse(gps_str)
            lat_string = msg.lat
            lon_string = msg.lon
            if (lat_string.find(".")>0 and lon_string.find(".")>0):
                lat_DD = int(float(lat_string)/100)
                lon_DD = int(float(lon_string)/100)
                lat_SS = float(lat_string) - lat_DD*100
                lon_SS = float(lon_string) - lon_DD*100
                lat = lat_DD + lat_SS/60
                lon = lon_DD + lon_SS/60
                if(msg.lat_dir=="S"):
                    lat = -lat
                if(msg.lon_dir=="W"):
                    lon = -lon
                self.coord1 = (lat,lon)
                print('GPS:' + str(self.coord1))
                self.Kalman_bool = True
                print("yes2")

    def update(self):
        if(self.running):
            self.coord = self.read()
            
    def run(self, Kalman_bool):
        return self.coord1, self.Kalman_bool

    def run_threaded(self):
        self.update()
        print("GPS"+ str(self.coord1))
        return self.coord1, self.Kalman_bool

    def shutdown(self):
        self.running = False

class printer():
    def run(self, statement):
        print(statement)
    
    def update(self,statement):
        print(statement)
        
    def run_threaded(self, statement):
        self.update(statement)

class compass_bearing:
    def __init__(self):
        self.compass_bearing = 0
        self.left_distance = 100
        self.right_distance = 100
        self.middle_distance = 100
        self.accel_x = 0
        self.accel_y = 0
        self.running = True
    
    def read(self):
        compass_serial = serialPort2.readline()
        compass_string = compass_serial.decode("ISO-8859-1")
        # compass_string = compass_string + ",20,100,20" #delete me
        if (compass_string.find(":") >= 0):
            #parsing
            print(compass_string)
            compass_string = compass_string.replace(":","")
            compass_string2 = compass_string.replace("\r\n", "")
            compass_string3 = compass_string2.replace("\x8d","")
            compass_string3 = compass_string3.replace("í\n","")
            compass_string3 = compass_string3.replace("ô",'')
            compass_string3 = compass_string3.replace("ù",'')
            compass_string4 = compass_string3.split(",")
            self.compass_bearing = float(compass_string4[0])
            self.accel_x = float(compass_string4[1])
            self.accel_y = float(compass_string4[2])
            try:
                self.left_distance = float(compass_string4[3])
                self.middle_distance = float(compass_string4[4])
                self.right_distance = float(compass_string4[5])
            except:
                print("ultrasonic sampling error")
            # print(self.compass_bearing)
            # print("accel:")
            # print(self.accel_x)
            # print(self.accel_y)
            # print(self.left_distance)
            # print(self.middle_distance)
            # print(self.right_distance)

    def update(self):
        if(self.running):
            self.read()
     
    def run(self):
        self.read()
        return self.compass_bearing, self.left_distance, self.middle_distance, self.right_distance, self.accel_x, self.accel_y
    
    def run_threaded(self):
        self.update()
        return self.compass_bearing, self.left_distance, self.middle_distance, self.right_distance, self.accel_x, self.accel_y
    
    def shutdown(self):
        self.running = False

        

# while True:
#     compass_serial = serialPort2.readline()
#     compass_string = compass_serial.decode("ISO-8859-1")
#     if compass_string.find("Medium,   Compass bearing:") > 0:
#         compass_string2 = compass_string.split("Medium,   Compass bearing:")
#         compass_string3 = compass_string2[1].replace("\r\n", "")
#         compass_bearing = float(compass_string3)
#         print(compass_bearing)