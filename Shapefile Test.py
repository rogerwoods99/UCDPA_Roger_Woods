import matplotlib.pyplot as plt
import shapefile
#import geopandas as gpd

import numpy as np
from shapely import wkt
from shapely.geometry import Point # Point class
from shapely.geometry import shape # shape() is a function to convert geo objects through the interface
import pandas as pd
from shapely.geometry import shape
from shapely.ops import cascaded_union
#from planar import Polygon

# get Met data
filename="MetEireann 200.txt"
grDat=pd.read_csv(filename)
grDat["County"]=""

#print(grDat)
sf = shapefile.Reader("shapefiles/test/IRL_Counties")  # this only has one shape to search through

shapes=sf.shapes()
#print(sf.records())

i_rec=0
recs_to_plot=[]
for rec in sf.records():
  #  print(rec)
    recs_to_plot.append(i_rec)
#    if rec[-1]==21:
#        print(rec)
#        print(i_rec)
#        recs_to_plot.append(i_rec)
    i_rec=i_rec+1

print(recs_to_plot)
print(shapes[1].points)

fd=Polygon(shapes[1].points)
polies=[]
for rec in recs_to_plot:
    polies.append(shapes[rec].points)
CP_bound=cascaded_union(polies)
#print(CP_bound)

print(polies)




print(len(shapes))
print(dir(shapes[0]))   # 342 shapes

print(shapes[0].shapeType)
#print(shapes[0].bbox)
#print(shapes[0].parts)
#print(len(shapes[0].points))
#print(shapes[0].points[7])

point_to_check = (214000,278000) # an x,y tuple
all_shapes = sf.shapes() # get all the polygons
all_records = sf.records()

# search through each shape to find the one the point is in
for i in range(0,1):    # number of points to search through
    point_to_check = (grDat.loc[i,"east"], grDat.loc[i,"north"])
   # print(point_to_check)
    for d in range(26):   # number of objects to search through
        if Point(point_to_check).within(shape(shapes[d])):  # make a point and see if it's in the polygon
            name = all_records[d][3]  # get the second field of the corresponding record
            print(str(i) + " complete")
            grDat.loc[i,"County"]=name
           # print(i)
#            print("The point " +str(point_to_check) + " is in " + str(name))

# save result to csv
grDat.to_csv("Met Results.txt")

#for i in len(all_shapes):
#    boundary = all_shapes[i] # get a boundary polygon
#    if Point(point_to_check).within(shape(boundary)): # make a point and see if it's in the polygon
#       name = all_records[i][2] # get the second field of the corresponding record
#       print("The point is in" + str(name))


# plot the shapefile
plt.figure(figsize=(9, 11), dpi=80)
for shape in sf.shapeRecords():
    x = [i[0] for i in shape.shape.points[:]]
    y = [i[1] for i in shape.shape.points[:]]
    #print(x)
    plt.plot(x,y)
#plt.show()

plt.figure(figsize=(9, 11), dpi=80)
for shape in polies.shapeRecords():
    x = [i[0] for i in shape.shape.points[:]]
    y = [i[1] for i in shape.shape.points[:]]
    #print(x)
    plt.plot(x,y)
plt.show()


#poly = wkt.loads(shapes[0])
#poly = wkt.loads('POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))')
#pt = wkt.loads('POINT(20 20)')
#print(poly.distance(pt))  # 0.0
#print(poly.boundary.distance(pt))