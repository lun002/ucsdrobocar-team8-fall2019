import serial
import pynmea2
import time
 
port = "/dev/ttyACM1"
serialPort = serial.Serial(port, baudrate = 9600, timeout = 0.01)
# port2 = "/dev/ttyACM1"
# serialPort2 = serial.Serial(port2, baudrate = 9600, timeout = 0.01)

while True:
    gps_data = serialPort.readline()
    gps_str = gps_data.decode("utf-8")
    # print(gps_str)
    if gps_str.find('GGA') > 0:
        # print('test1')
        msg = pynmea2.parse(gps_str)
        #__________
        # print(msg)
        # print(msg.lon)
        # print("Timestamp: %s -- Lat: %s %s -- Lon: %s %s -- Altitude: %s %s -- Satellites: %s" % (msg.timestamp,msg.lat,msg.lat_dir,msg.lon,msg.lon_dir,msg.altitude,msg.altitude_units,msg.num_sats)) 
        #___________
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
            print("horizontal dilution:" + msg.horizontal_dil)
            print(msg.timestamp)
            print(msg.num_sats)
            coord1 = (lat,lon)
            print(coord1)