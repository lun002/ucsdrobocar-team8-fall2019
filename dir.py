
import math
import geopy.distance

coordinate_list = [(32.881139, -117.236232)]
pop_distance = 1
straight_angle = 5

class initiate_variable:
    def __init__(self):
        self.angle = 0
        self.Kalman_bool = True
        self.running = True
    
    def run(self):
        if (self.running == True):
            self.running = False
            print("init is running")
            return self.angle, self.Kalman_bool

class compass_bearing_calc:
    def __init__(self):
        self.coord1 = None
        self.coord2 = None
        self.compass_bearing = None
        self.running = True

    def calc_compass(self, pointA, pointB):
        """
        Calculates the bearing between two points.
        The formulae used is the following:
            θ = atan2(sin(Δlong).cos(lat2),
                    cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
        input: 
            pointA: (tuple) latitude,longitude
            pointB: (tuple) latitude,longitude
        output:
            compass_bearing: (float) compass bearing in degrees
        """
        if (type(pointA) != tuple) or (type(pointB) != tuple):
            raise TypeError("Only tuples are supported as arguments")
        lat1 = math.radians(pointA[0])
        lat2 = math.radians(pointB[0])
        diffLong = math.radians(pointB[1] - pointA[1])

        x = math.sin(diffLong) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
                * math.cos(lat2) * math.cos(diffLong))

        initial_bearing = math.atan2(x, y)
        initial_bearing = math.degrees(initial_bearing)
        self.compass_bearing = (initial_bearing + 360) % 360
    
    def run(self, coord1, gps_list):
        self.calc_compass(coord1, gps_list[0])
        return self.compass_bearing

class turn_direction_calc():
    def __init__(self):
        self.current_bearing = 0
        self.needed_bearing = 0
        self.turn = ""
        self.running = True
        self.turn_deg = 0

    def turn_direction(self, current_bearing, needed_bearing):
        """
        Calculates the necessary turn between two compass bearings
        input:
            current_bearing: (float) compass bearing measured by sensor in degrees
            needed_bearing: (float) compass bearing of desired location in degrees
        output:
            turn: (string) left, right, or straight manuevar
        """
        error = current_bearing - needed_bearing
        print("current bearing:" + str(current_bearing))
        print(needed_bearing)
        print("error:" + str(error))
        if (abs(error) <= straight_angle):
            turn = "straight"
            turn_deg = 0
        else:
            if (error >= -180 and error <= 0):
                turn = "right"
                self.turn_deg = abs(error)/180
            if (error >=180):
                turn = "right"
                self.turn_deg = (error+2*(180-error))/180
            if (error < -180):
                turn = "left"
                self.turn_deg = -(abs(error)+2*(180-abs(error)))/180
            if (error>=0 and error<180):
                turn = "left"
                self.turn_deg = -abs(error)/180
            # if (current_bearing == needed_bearing):
            #     turn = "straight"
        self.turn = turn
    
    def run(self, c1, c2):
        self.current_bearing = c1
        self.needed_bearing = c2
        print("Turn:" + str(self.turn_deg))
        self.turn_direction(self.current_bearing, self.needed_bearing)
        return self.turn, self.turn_deg

class steering_adjuster():
    def __init__(self):
        self.input_steering = 0
        self.output_steering = 0
        self.turn_direction = "straight"
    
    def adjust_steering(self):
        if (self.turn_direction == "left" and self.input_steering > -.9):
            self.output_steering = self.input_steering - .1
        if (self.turn_direction == "right" and self.input_steering < .9):
            self.output_steering = self.input_steering + .1
        if (self.turn_direction == "straight"):
            self.output_steering = 0
    
    def run(self, input_steering, turn_direction):
        print('turn_direction:'+str(turn_direction))
        print('input_steering:'+str(input_steering))
        self.input_steering = input_steering
        self.turn_direction = turn_direction
        self.adjust_steering()
        return self.output_steering
            
class gps_list():
    def __init__(self):
        self.list = coordinate_list
    
    def check_position(self, coord1):
        if (self.list != None):
            distance = geopy.distance.distance(coord1, self.list[0]).m
            print("distance = " + str(distance))
            if (distance < pop_distance):
                self.list.pop(0)
    
    def run(self, coord1):
        self.check_position(coord1)
        return self.list
            

# test
# ---------------------------

# lat1 = 32.881146
# lon1 = -117.233513
# lat2 = 32.881329
# lon2 = -117.233370
# current_bearing = 100
# compass = compass_bearing_calc()
# compass.run(lat1, lon1, coordinate_list)
# print(compass.compass_bearing)
# turn_class = turn_direction_calc()
# turn_class.run(current_bearing, compass.compass_bearing) 
# print(turn_class.turn)
# my_gps_list = gps_list()
# a = my_gps_list.run(lat1,lon1)
# print(a)
