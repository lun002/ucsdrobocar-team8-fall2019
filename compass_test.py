import serial

port = "/dev/ttyACM1"
serialPort = serial.Serial(port, baudrate = 9600, timeout = 0.01)
port2 = "/dev/ttyACM0"
serialPort2 = serial.Serial(port2, baudrate = 9600, timeout = 0.01)

while True:
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
        compass_string4 = compass_string3.split(",")
        compass_bearing = float(compass_string4[0])
        accel_x = float(compass_string4[1])
        accel_y = float(compass_string4[2])
        try:
            left_distance = float(compass_string4[3])
            middle_distance = float(compass_string4[4])
            right_distance = float(compass_string4[5])
        except:
            print("ultrasonic sampling error")

# while True:
#     compass_serial = serialPort2.readline()
#     compass_string = compass_serial.decode("ISO-8859-1")
#     if compass_string.find("Medium,   Compass bearing:") > 0:
#         compass_string2 = compass_string.split("Medium,   Compass bearing:")
#         compass_string3 = compass_string2[1].replace("\r\n", "")
#         compass_bearing = float(compass_string3)
#         print(compass_bearing)