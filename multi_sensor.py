import numpy as np
import matplotlib.pyplot as plt
# from scipy.stats import norm
# from sympy import Symbol, Matrix
# from sympy.interactive import printing

import math
import geopy.distance
import serial
import pynmea2
import to_meters as tm
import time

def plot_measurements():
    fig = plt.figure(figsize=(16,9))
    plt.subplot(211)
    plt.step(range(m),mpx, label='$x$')
    plt.step(range(m),mpy, label='$y$')
    plt.ylabel(r'Position $m$')
    plt.title('Measurements')
    plt.ylim([-10, 10])
    plt.legend(loc='best',prop={'size':18})

    plt.subplot(212)
    plt.step(range(m),mx, label='$a_x$')
    plt.step(range(m),my, label='$a_y$')
    plt.ylabel(r'Acceleration $m/s^2$')
    plt.ylim([-1, 1])
    plt.legend(loc='best',prop={'size':18})

def savestates(x, Z, P, K):
    xt.append(float(x[0]))
    yt.append(float(x[1]))
    dxt.append(float(x[2]))
    dyt.append(float(x[3]))
    ddxt.append(float(x[4]))
    ddyt.append(float(x[5]))
    Zx.append(float(Z[0]))
    Zy.append(float(Z[1]))
    Px.append(float(P[0,0]))
    Py.append(float(P[1,1]))
    Pdx.append(float(P[2,2]))
    Pdy.append(float(P[3,3]))
    Pddx.append(float(P[4,4]))
    Pddy.append(float(P[5,5]))
    Kx.append(float(K[0,0]))
    Ky.append(float(K[1,0]))
    Kdx.append(float(K[2,0]))
    Kdy.append(float(K[3,0]))
    Kddx.append(float(K[4,0]))
    Kddy.append(float(K[5,0]))

def plot_P():
    fig = plt.figure(figsize=(16,9))
    plt.subplot(211)
    plt.plot(range(cnt),Px, label='$x$')
    plt.plot(range(cnt),Py, label='$y$')
    plt.title('Uncertainty (Elements from Matrix $P$)')
    plt.legend(loc='best',prop={'size':22})
    plt.subplot(212)
    plt.plot(range(cnt),Zx, label='$x$')
    plt.plot(range(cnt),Zy, label='$y$')
    plt.xlabel('Filter Step')
    plt.ylabel('')
    plt.legend(loc='best',prop={'size':22})

def plot_K_xy():
    fig = plt.figure(figsize=(16,9))
    plt.plot(range(cnt),Kx, label='Kalman Gain for $x$')
    plt.plot(range(cnt),Ky, label='Kalman Gain for $y$')
    #plt.plot(range(len(measurements[0])),Kdx, label='Kalman Gain for $\dot x$')
    #plt.plot(range(len(measurements[0])),Kdy, label='Kalman Gain for $\dot y$')
    #plt.plot(range(len(measurements[0])),Kddx, label='Kalman Gain for $\ddot x$')
    #plt.plot(range(len(measurements[0])),Kddy, label='Kalman Gain for $\ddot y$')

    plt.xlabel('Filter Step for x and y')
    plt.ylabel('')
    plt.title('Kalman Gain (the lower, the more the measurement fullfill the prediction)')
    plt.legend(loc='best',prop={'size':18})

xt = []
yt = []
x_gps = []
y_gps = []
dxt= []
dyt= []
ddxt=[]
ddyt=[]
Zx = []
Zy = []
Px = []
Py = []
Pdx= []
Pdy= []
Pddx=[]
Pddy=[]
Kx = []
Ky = []
Kdx= []
Kdy= []
Kddx=[]
Kddy=[]


class Kalman_Filter:
    def __init__(self):
        # self.px = 0
        # self.py = 0
        self.x = np.matrix([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]).T
        self.n = self.x.size # States
        self.P = np.diag([100.0, 100.0, 10.0, 10.0, 1.0, 1.0])
        self.new_coord = (0,0)
        self.prevtime = time.time()
        
    def filter(self, coord, compass_bearing, accel_x, accel_y):
        dt = time.time() - self.prevtime
        print("time:" + str(dt))
        print("HELLOOOOOOO" + str(coord))
        self.A = np.matrix([[1.0, 0.0, dt, 0.0, 1/2.0*dt**2, 0.0],
                    [0.0, 1.0, 0.0, dt, 0.0, 1/2.0*dt**2],
                    [0.0, 0.0, 1.0, 0.0, dt, 0.0],
                    [0.0, 0.0, 0.0, 1.0, 0.0, dt],
                    [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]])

        self.H = np.matrix([[1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]])
        # sa = 0.001
        sa = .001
        self.G = np.matrix([[1/2.0*dt**2],
                    [1/2.0*dt**2],
                    [dt],
                    [dt],
                    [1.0],
                    [1.0]])
        self.Q = self.G*self.G.T*sa**2
        self.I = np.eye(self.n)
        ra = 10.0**2   # Noise of Acceleration Measurement
        rp = 100.0**2  # Noise of Position Measurement
        ra = (.00334365)**2
        rp = .00001
        self.R = np.matrix([[rp, 0.0, 0.0, 0.0],
                    [0.0, rp, 0.0, 0.0],
                    [0.0, 0.0, ra, 0.0],
                    [0.0, 0.0, 0.0, ra]])
                    
        self.py= tm.Lat2Meter(coord[0])
        self.px= tm.Lon2Meter(coord[1])

        theta = tm.deg2rad(compass_bearing)
        self.ax = accel_x*math.cos(theta) - accel_y*math.cos(math.pi/2 - theta)
        self.ay = accel_x*math.sin(theta) + accel_y*math.sin(math.pi/2 - theta)

        self.measurements = np.matrix([self.px,self.py,self.ax,self.ay])
        print("measurements:" + str(self.measurements))
        
        self.x = self.A*self.x   
        self.P = self.A*self.P*self.A.T + self.Q  

        if self.Kalman_bool:      
            self.S = self.H*self.P*self.H.T + self.R
            self.K = (self.P*self.H.T) * np.linalg.pinv(self.S)        
            self.Z = np.transpose(self.measurements)
            self.y = self.Z - (self.H*self.x)                            # Innovation or Residual
            self.x = self.x + (self.K*self.y)              
            self.P = (self.I - (self.K*self.H))*self.P
            # self.Kalman_bool = False
            print("yes")
        else:
            print("no")      
        self.new_coord = tm.Meter2GPS(self.x[1], self.x[0])
        print("Kalman:" + str(self.new_coord))
        self.prevtime = time.time()

        # savestates(x, Z, P, K)
        # gps.kalman = False
    
    def run(self, coord,compass_bearing, accel_x, accel_y, Kalman_bool):
        self.Kalman_bool = Kalman_bool
        self.filter(coord, compass_bearing, accel_x, accel_y)
        print(self.Kalman_bool)
        return self.new_coord, self.Kalman_bool
        

# print("done")
# plot_P()
# plot_K_xy()
# plt.show()
