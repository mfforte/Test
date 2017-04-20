# script to read hypack raw file and extract the POS position line containing easting, northing, and elevation (tide)
# writes data to a file comma separated in the format [902464.015,48713.648,3.452]
# mainly used to for comparing hypack RTK positions with post processed positions
import numpy as np
import os
from matplotlib import pyplot as plt

File_Dir ="C:/HYPACK 2013/Projects/EDT_work/Raw/"
file_outName = File_Dir + "XYZT_GPS.txt"

# create empty variables
X = []
Y = []
Z = []
g_Time = []

for filename in os.listdir(File_Dir):
    if filename.endswith(".RAW"):
        with open (File_Dir + filename,"rb") as f:
# read through hypack text file extracting X,Y,Z and appending
            for line in f:
                if line.startswith("POS"):
                    pos = line.split()
                    X.append(pos[3])
                    Y.append(pos[4])
                    Z.append(pos[5])

        # get the gps time from MSG line
                if line.startswith("MSG"):
                    gps_time = line.split()
                    gps_timet = gps_time[3].split(',')
                    g_Time.append(gps_timet[2])

f.close()


# numpy work - rearrange variables into column arrays
# change text format to float for file write

b = np.column_stack((X,Y,Z,g_Time))
c = b.astype(np.float)

# make plot to ensure validity
plt.plot(X,Y,'.')
plt.show()

# write file
np.savetxt(file_outName,c,delimiter=",",fmt='%1.3f')




