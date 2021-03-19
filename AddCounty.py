import matplotlib.pyplot as plt
import shapefile
import numpy as np
from shapely import wkt
from shapely.geometry import Point # Point class
from shapely.geometry import shape # shape() is a function to convert geo objects through the interface
import pandas as pd

# get Met Eireann data which already has the elevation data included.
# Add a "County" column to store the county name per point
filename="MetEireann_maxT with Elev.txt"
grDat = pd.read_csv(filename)
grDat["County"]=""

# load shapefile of IRL counties
sf = shapefile.Reader("shapefiles/test/IRL_Counties")  # this has 26 separate polygons to represent the 26 counties

shapes=sf.shapes()

#print(len(shapes))
#print(shapes[0])   # 342 shapes

all_shapes = sf.shapes() # get all the polygons
all_records = sf.records()

# search through each shape to find the one the point is in.
# The point data is for all of IRL, hence 14,000 odd dots not part of the Republic of Ireland and have no "County" result

for i in range(0,84291):    # number of points to search through
    point_to_check = (grDat.loc[i,"east"], grDat.loc[i,"north"])   # get the east and north values

    for d in range(26):   # loop through the 26 county polygons
        if Point(point_to_check).within(shape(shapes[d])):  # make a point and see if it's in the polygon
            name = all_records[d][3]  # get the third field of the corresponding record which is the county name
            grDat.loc[i,"County"]=name
    print(str(i) + " complete")   # this gives the user an idea of far the process has got

# save result to csv
grDat.to_csv("MetEireann_maxT_County.txt")

# plot the shapefile DO I NEED TO DO THIS?
plt.figure(figsize=(9, 11), dpi=80)
for shape in sf.shapeRecords():
    x = [i[0] for i in shape.shape.points[:]]
    y = [i[1] for i in shape.shape.points[:]]
    #print(x)
    plt.plot(x,y)
#plt.show()