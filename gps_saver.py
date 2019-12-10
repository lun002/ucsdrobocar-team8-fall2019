import os.path

save_path = "gps_save/"
cnt = 1 
while (os.path.isfile(save_path + str(cnt))):
    cnt = cnt + 1
file_path = save_path + str(cnt) + ".txt"

class GPS_save:
    def writter(self,gps_location):
        with open(file_path, "a+") as myfile:
            myfile.write(str(gps_location) + "\n")

    def run(self, gps_location):
        self.writter(gps_location)



