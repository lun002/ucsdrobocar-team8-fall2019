import gmplot

coordinate_location = "/home/luan/projects/d3/gps_save/12_6/49.txt"
save_location = "/home/luan/projects/d3/map/"
lat_list = []
lon_list = []
with open(coordinate_location) as f:
    lines = f.readlines()
for i in lines:
    string = i.replace('\n', '')
    string = string.replace('(','')
    string = string.replace(')','')
    coord = string.split(',')
    lat_list.append(float(coord[0]))
    lon_list.append(float(coord[1]))

gmap = gmplot.GoogleMapPlotter(lat_list[0], lon_list[0],20)
gmap.scatter(lat_list, lon_list, '# FF0000', size = .5, marker = False )
gmap.plot(lat_list, lon_list, 'cornflowerblue', edge_width = 2.5)
gmap.apikey = " AIzaSyD6mC7oswdPVXu8vD1siD4bifw7N-1Mano "
gmap.draw(save_location + "1")




