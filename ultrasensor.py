import sys
min_middledistance = 50
min_otherdistance = 50
class controller:
    def __init__(self):
        self.turn_deg = 0
    
    def turn_direction(self,dist_left, dist_middle, dist_right):
        if (dist_left > dist_right):
            self.turn_deg = -.8
        if (dist_right > dist_left):
            self.turn_deg = .8
        else:
            self.turn_deg = .8
    def run(self, dist_left, dist_middle, dist_right, turn):
        self.turn_deg = turn
        if dist_left == 0:
            dist_left = 1000
        if dist_middle == 0:
            dist_middle = 1000
        if dist_right == 0:
            dist_right = 1000

        if (dist_middle <= min_middledistance and dist_middle > 0):
            self.turn_direction(dist_left, dist_middle, dist_right)
        if (dist_middle >= min_middledistance and dist_middle > 0):
            if (dist_left <= min_otherdistance and dist_left > 0 and turn < 0):
                self.turn_deg = 0
            if (dist_right <= min_otherdistance and dist_right > 0 and turn > 0):
                self.turn_deg = 0
        print("DISTANCE:"+str(dist_left) + ' | ' + str(dist_middle) + ' | ' + str(dist_right))
        print("REAL TURN:___________" + str(self.turn_deg))
        sys.stdout.flush()
        # print("\33[2J")
        # print("\33[1A")
        return self.turn_deg

# test = ultrasensor_controller()
# test.run(3, 2, 1)
# print(test.turn)
        
        
