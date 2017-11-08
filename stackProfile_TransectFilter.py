import numpy as np
from matplotlib import pyplot as plt
import arcpy
# M.Forte - July 2017
# Script to build profiles, filter and save for AcuSea Model
# script to take in numpy output from arcpy stackprofile tool
# Script performs:
# 1. filters out elevations above 0 starting with the offshore end and working shoreward
# 2. Adds distance to each profile based on the elevation filtered profile - user defined based on DEM resolution

## Expects columns in numpy file:

## ESRI work - needs:
# 1. DEM - geotiff
# 2. Profiles - generated from GRASS

transects = "C:/Temp/GIS_process/NCtransects.shp"
DEM = "C:/Temp/GIS_process/NC_DEM_StatePlane.tif"
profile_table = "C:/Temp/GIS_process/profile_values.dbf"
Profiles_Numpy = "C:/Temp/GIS_process/Profiles_Numpy_Final"
transects_azimuth = "C:/Temp/GIS_process/NCtransects_azimuth.shp"
startpts_azimuths_numpy = "C:/Temp/GIS_process/Azimuths_Numpy"
arcpy.env.overwriteOutput=True
arcpy.CheckOutExtension("3D")


arcpy.StackProfile_3d(transects,DEM,profile_table)


arr = arcpy.da.TableToNumPyArray(profile_table,('LINE_ID','FIRST_DIST','FIRST_Z'))

# Build start and endpoints of transects for azimuth calculation
# will need to add each field start x and start y with below expressions - use 0.0,True for start point and 1.0 for endpoint
arcpy.AddField_management(transects,"Start_X","DOUBLE")
arcpy.AddField_management(transects,"Start_Y","DOUBLE")
arcpy.AddField_management(transects,"End_X","DOUBLE")
arcpy.AddField_management(transects,"End_Y","DOUBLE")

arcpy.CalculateField_management(transects,"Start_X","!Shape!.positionAlongLine(0.0,True).firstPoint.X","PYTHON")
arcpy.CalculateField_management(transects,"Start_Y","!Shape!.positionAlongLine(0.0,True).firstPoint.Y","PYTHON")
arcpy.CalculateField_management(transects,"End_X","!Shape!.positionAlongLine(1.0,True).firstPoint.X","PYTHON")
arcpy.CalculateField_management(transects,"End_Y","!Shape!.positionAlongLine(1.0,True).firstPoint.Y","PYTHON")

#reproject file to NAD 83 Geographic
arcpy.Project_management(transects,transects_azimuth,6318)

arcpy.AddField_management(transects_azimuth,"Long_Start","DOUBLE")
arcpy.AddField_management(transects_azimuth,"Lat_Start","DOUBLE")
arcpy.AddField_management(transects_azimuth,"Long_End","DOUBLE")
arcpy.AddField_management(transects_azimuth,"Lat_End","DOUBLE")

arcpy.CalculateField_management(transects_azimuth,"Long_Start","!Shape!.positionAlongLine(0.0,True).firstPoint.X","PYTHON")
arcpy.CalculateField_management(transects_azimuth,"Lat_Start","!Shape!.positionAlongLine(0.0,True).firstPoint.Y","PYTHON")
arcpy.CalculateField_management(transects_azimuth,"Long_End","!Shape!.positionAlongLine(1.0,True).firstPoint.X","PYTHON")
arcpy.CalculateField_management(transects_azimuth,"Lat_End","!Shape!.positionAlongLine(1.0,True).firstPoint.Y","PYTHON")

az_array = arcpy.da.TableToNumPyArray(transects_azimuth,('cat','Long_Start','Lat_Start','Long_End','Lat_End'))

# remove text headers
c = arr.astype(object)
# arrange array in columns calling vstack
vstack = np.vstack(c)
# find last profile line number for counter
lineNo = max(vstack[:,0])


# invert file so that deepest depths begin profile - this accounts for profiles extending over
# over dune and then into estuary
vstackflip = vstack[::-1]
# convert numpy array to list
profi = list(vstackflip)
# setup empty list variable
# begin loop removing elevations <=0
tempList = []
for line in profi:
    if line[2]<=0:
        tempList.append(line)

# file setup for second loop adding re-calculated distance [ Distance variable = grid cell resolution used during
# profile extraction
nplist = np.array(tempList)
nplist = nplist[::-1]
nplist = list(nplist)
lineCount = 0
Distance = 0
newList = []
# loop that adds the new distance to profile starting at elevation = ~0
for row in nplist:
    if row[0] == lineCount:
        row = list(row)
        row.insert(1,Distance)
        x = row
        Distance += 7
        newList.append(x)
    else:
        lineCount += 1
        Distance = 0

#Bulk Plotting for quick look
#build x and y from list
x_list = [l[1] for l in newList]
y_list = [l[3] for l in newList]
plt.plot(x_list, y_list, '.')

np.save(Profiles_Numpy,newList)
np.save(startpts_azimuths_numpy,az_array)
# need line to save numpy array to txt for matlab
# np.savetxt(azimuths_mat,)


