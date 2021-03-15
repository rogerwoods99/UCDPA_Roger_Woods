import matplotlib.pyplot as plt
import shapefile
import numpy as np
from shapely import wkt
from shapely.geometry import Point # Point class
from shapely.geometry import shape # shape() is a function to convert geo objects through the interface
import pandas as pd
from matplotlib.ticker import MultipleLocator

# get Met Eireann data which already has the elevation and county data included.
# Add a "County" column to store the county name per point
filename="MetEireann_maxT_County.txt"
grDat = pd.read_csv(filename)

# find the rows with NaN
grNaN= grDat[grDat.isna().any(axis=1)]
print(grNaN)

#print(grDat.columns)
grDat.dropna(inplace=True)  # drop rows with NaN value
grDat.drop(grDat.columns[0:2], axis=1, inplace=True)  # drop the first 2 columns
grDat.drop(columns="Elev_x", axis=1, inplace=True)  # drop the Elev_x column
print(grDat)

# Plot the elevation data
plt.figure(figsize=(9, 10), dpi=80)  # set the size of the image window. figsize x dpi gives the output size
plt.scatter(grDat["east"], grDat["north"], 1,c=grDat["Elev_y"],cmap="terrain")
plt.xlabel("x coord")
plt.ylabel("y coord")
# Add title
cbar=plt.colorbar()   # shows legend to the side
cbar.set_label("elevation (m)")
plt.title("Ireland Grid using c colour method")
plt.show()

########################
# CORRELATION OF ELEVATION AND MAX TEMP
# max temp plot
plt.figure(figsize=(9, 10), dpi=80)  # set the size of the image window. figsize x dpi gives the output size
plt.scatter(grDat["m1Tmax"], grDat["Elev_y"])
plt.xlabel("Max temp")
plt.ylabel("Elevation (m)")
plt.show()

##########################
# AREA OF COUNTIES
# Plot bar chart of the area of each county by the count of 1km squares
# need to create DF of the grouped results and then sort by the area so that plots from smallest to largest
grDat_Gp = grDat.groupby("County")["County"].count().to_frame(name="Area")
grFinal= grDat_Gp.sort_values(by=["Area"])
#grFinal["Size"]=0
grFinal.reset_index(inplace=True)   # reset the index so that can plot properly
print(grFinal)

# add numbers from 0 to 25
#for s in range(26):
    #print(s)
#    grFinal.iloc[s, 1]=s

# now make this the index
#print(grFinal.index)
#grFinal.set_index("Size", inplace=True)
#print(grFinal)

#grFinal.plot(kind="barh", figsize=(7, 8))
#plt.figure(figsize=(9, 10), dpi=80)
#plt.title("Area of Irish Counties (km)")
#plt.ylabel("County")
#plt.xlabel("Area (km2)")
#plt.show()



# what about a pivot table for this type of bar chart???
#print(sales.pivot_table(values="weekly_sales", index="department", columns="type",fill_value=0))
#print(grDat.pivot_table(values="County", index="County", fill_value=0))
#the above will take the weekly_sales data and use department as the index


# this is the best
fig, ax = plt.subplots()

fig.set_size_inches(9,7)


ax.barh(grFinal["County"], grFinal["Area"], zorder=2)  # zorder specifies the order of drawing
#ax.set_xticklabels(Rio.index)  #, rotation=45)
ax.set_xlabel("Area km2")
ax.set_ylabel("County")

ax.xaxis.set_minor_locator(MultipleLocator(200)) ### set minor tick mark size
ax.grid(True, which="minor", zorder=1)

ax.xaxis.set_major_locator(MultipleLocator(1000))  # set major tick mark size
ax.grid(True, axis="x", which="major", linewidth=2, zorder=1)



#ax.legend("Area")
fig.suptitle("Area of Irish Counties (km2)")
fig.tight_layout()   # removes white space around graph
#ax.legend()
plt.show()

## This is 2nd best

#plt.figure(figsize=(9, 10), dpi=80)  # set the size of the image window. figsize x dpi gives the output size
#plt.barh( grFinal["County"],grFinal["Area"], height=0.5)
#plt.xlabel("Area (km2)")
#plt.ylabel("County")
# Add title
#cbar=plt.colorbar()   # shows legend to the side
#cbar.set_label("elevation (m)")
#plt.title("Area of Irish Counties (km2)")
#plt.show()

#######################################################
# AVERAGE ELEVATION OF COUNTIES

grDat_El = grDat.groupby("County")["Elev_y"].mean().to_frame(name="ElevMean")
grElev= grDat_El.sort_values(by=["ElevMean"])
#grFinal["Size"]=0
grElev.reset_index(inplace=True)   # reset the index so that can plot properly
print(grElev)

grDat_El2 = grDat.groupby("County")[["Elev_y"]].mean()  # same as above but creates DF straight away. Keeps elev_y name
grElev2= grDat_El2.sort_values(by=["Elev_y"])
grElev2.reset_index(inplace=True)
#grFinal["Size"]=0
#grElev.reset_index(inplace=True)   # reset the index so that can plot properly
print(grElev2)


# try multiple agg functions

# dogs.groupby("color")["weight].agg([min, max, sum])

# create mean, min, max and stdev of the county elevation and plot with error bars
grDat_El3 = grDat.groupby("County")["Elev_y"].agg([np.mean, min, max, np.std])
grDat_El3.reset_index(inplace=True)
grElev3=grDat_El3.sort_values(["mean"])
print(grDat_El3)
#grElev3= grDat_El3.sort_values(by=["Elev_y"])
#grElev3.reset_index(inplace=True)
#grFinal["Size"]=0
#grElev.reset_index(inplace=True)   # reset the index so that can plot properly
#print(grElev3)



fig, ax = plt.subplots()
fig.set_size_inches(9,7)
ax.errorbar(grElev3["mean"], grElev3["County"], xerr=grElev3["std"],
            ecolor="red", capsize=5, linewidth=4, elinewidth=1, fmt="bo")

#spacing = 20 # This can be your user specified spacing.
#minorLocator = MultipleLocator(spacing)
#ax.plot(9 * np.random.rand(10))
# Set minor tick locations.
#ax.yaxis.set_minor_locator(minorLocator)
ax.xaxis.set_minor_locator(MultipleLocator(20))
ax.grid(True, which="minor")

ax.xaxis.set_major_locator(MultipleLocator(100))
#ax.xaxis.set_major_formatter("{x:.0f}")
ax.grid(True, axis="x", which="major", linewidth=2)
ax.grid(True, axis="y", which="major", linewidth=1)


#ax.set_xticklabels(Rio.index)  #, rotation=45)
ax.set_xlabel("Average elevation (m)")
ax.set_ylabel("County")
#ax.legend("Area")
fig.suptitle("Average elevation of Irish counties (m)")
fig.tight_layout()   # removes white space around graph
#ax.legend()
plt.show()