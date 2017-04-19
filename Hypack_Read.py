# script to read hypack raw file and extract the POS position line containing easting, northing, and elevation (tide)
# writes data to a file comma separated in the format [902464.015,48713.648,3.452]
# mainly used to for comparing hypack RTK positions with post processed positions
import numpy as np

with open ("C:/HYPACK 2013/Projects/EDT_work/Raw/008_1331.RAW","rb") as f:
    X = []
    Y = []
    Z = []


    for line in f:
        line_count =+1
        if line.startswith("POS"):
            pos = line.split()
            X.append(pos[3])
            Y.append(pos[2])
            Z.append(pos[5])
    f.close()




b = np.column_stack((X,Y,Z))
c = b.astype(np.float)
np.savetxt("C:/HYPACK 2013/Projects/EDT_work/Raw/008_1331_testout.txt",c,delimiter=",",fmt='%1.3f')




