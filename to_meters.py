import math
import geopy.distance
Earth_radius = 6378 * 1000

def rad2deg (rad):
    deg = rad*180/math.pi
    return deg

def deg2rad (deg):
    rad = deg*math.pi/180
    return rad

def GetNextPoint(coord, distance, azimuth):
    radius_ratio = distance/Earth_radius
    bearing = deg2rad(azimuth)
    lat1 = deg2rad(coord[0])
    lon1 = deg2rad(coord[1])
    lat2_1 = math.sin(lat1)*math.cos(radius_ratio)
    lat2_2 = math.cos(lat1)*math.sin(radius_ratio)*math.cos(bearing)
    lat2 = math.asin(lat2_1 + lat2_2)
    lon2_1 = math.sin(bearing)*math.sin(radius_ratio)*math.cos(lat1)
    lon2_2 = math.cos(radius_ratio) - math.sin(lat1)*math.sin(lat2)
    lon2 = lon1 + math.atan2(lon2_1,lon2_2)
    lon2 = math.fmod((lon2+3*math.pi), 2*math.pi) - math.pi
    coord2 = (rad2deg(lat2),rad2deg(lon2))
    return coord2

def GetPointEast(coord, distance):
    return GetNextPoint(coord,distance,90)

def GetPointNorth(coord, distance):
    return GetNextPoint(coord,distance,0)

def Meter2GPS(latm,lonm):
    point = (0,0)
    pointE = GetPointEast(point,lonm)
    pointNE = GetPointNorth(pointE, latm)
    return pointNE
def GetDistanceMeters(coord1, coord2):
    dLat = deg2rad(coord2[0] - coord1[0])
    dLon = deg2rad(coord2[1] - coord1[1])
    a = math.sin(dLat/2)**2 + math.cos(deg2rad(coord1[0]))*math.cos(deg2rad(coord2[0]))* math.sin(dLon/2)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    return Earth_radius*c
def Lat2Meter(lat):
    # distance = geopy.distance.distance((lat,0),(0,0)).km*1000
    distance = GetDistanceMeters((lat,0),(0,0))
    if (lat<0):
        distance = distance*-1
    return distance
def Lon2Meter(lon):
    # distance = geopy.distance.distance((0,lon),(0,0)).km*1000
    distance = GetDistanceMeters((0,lon),(0,0))
    if (lon<0):
        distance = distance*-1
    return distance

# coord = (32.869117, -117.216555)
# print("Original point:")
# print(coord)
# lat_m = Lat2Meter(coord[0])
# lon_m = Lon2Meter(coord[1])
# new_coord = Meter2GPS(lat_m, lon_m)
# print("New point:")
# print(new_coord)




