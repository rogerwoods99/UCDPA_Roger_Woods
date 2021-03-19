import matplotlib.pyplot as plt
import shapefile
import numpy as np
from shapely import wkt
from shapely.geometry import Point # Point class
from shapely.geometry import shape # shape() is a function to convert geo objects through the interface
import pandas as pd
from matplotlib.ticker import MultipleLocator
import seaborn as sns
import matplotlib.colors as colors

# get Met Eireann data which already has the elevation and county data included.
# Add a "County" column to store the county name per point
filename="MetEireann_maxT_County.txt"
grDat = pd.read_csv(filename)

# find the rows with NaN
grNaN= grDat[grDat.isna().any(axis=1)]
#print(grNaN)

#print(grDat.columns)
grDat.dropna(inplace=True)  # drop rows with NaN value
grDat.drop(grDat.columns[0:2], axis=1, inplace=True)  # drop the first 2 columns
grDat.drop(columns="Elev_x", axis=1, inplace=True)  # drop the Elev_x column
#print(grDat)

##############################
# Merge the data from the Min Temp, Max rain and Min rain files

# get Met Eireann min temp data as DF.
filename="MetEireannBasic_MinT.txt"
MetTMin = pd.read_csv(filename)
#print(MetTMin)

# merge this DF with the main DF so that we have the min, max temperature, elevation and county for each
# of the 69,862 points
MetTMaxMin=grDat.merge(MetTMin, on=["east","north"], how="left", suffixes=("_Tmax", "_Tmin"))
#print(MetTMaxMin.columns)

# get Met Eireann rain data as DF.
filename="MetEireannBasic_R.txt"
MetR = pd.read_csv(filename)

# merge this rainfall DF with the main DF so that we have the min, max temperature, rainfall,
# elevation and county for each of the 69,862 points
MetTMaxMinR=MetTMaxMin.merge(MetR, on=["east","north"], how="left")
#print(MetTMaxMinR.columns)

#print(MetTMaxMinR)

#######################################
# Calculate the min of the minT values and the max of the maxT values

# minimum of minT
colMin = MetTMaxMinR.loc[:, "m1Tmin":"m12Tmin"]
MetTMaxMinR["minT"]= colMin.min(axis=1)

# maximum of maxT
colMax = MetTMaxMinR.loc[:, "m1Tmax":"m12Tmax"]
MetTMaxMinR["maxT"]= colMax.max(axis=1)

print(MetTMaxMinR.columns)

# save result to txt file
MetTMaxMinR.to_csv("minTcol.txt")
################################################

##############################################################
##  DEFINE FUCNTION TO PLOT DATA AS POINTS ON XY IRELAND GRID

#def PlotMapOld(coordX, coordY, coordZ, labText, pltTit):
#    plt.figure(figsize=(9, 10), dpi=80)  # set the size of the image window. figsize x dpi gives the output size
#    plt.scatter(coordX, coordY, 1, c=coordZ, cmap="terrain")
#    plt.xlabel("Easting")
#    plt.ylabel("Northing")
#    # Add title
#    cbar = plt.colorbar()  # shows legend to the side
#    cbar.set_label(labText)
#    plt.grid(which="major", axis="both")
#    plt.text(90000, 106000, "Carrauntoohil", color="white", ha="left", fontsize="x-large", fontweight="bold")
#    plt.plot([80300, 90000], [84400, 106000], color="white")
#    plt.title(pltTit)

def PlotMap(coordX, coordY, coordZ, labText, pltTit, Ucol):
    plt.figure(figsize=(9, 10), dpi=80)  # set the size of the image window. figsize x dpi gives the output size
    plt.scatter(coordX, coordY, 1, c=coordZ, cmap=Ucol)
    plt.xlabel("Easting", fontsize=12)
    plt.ylabel("Northing", fontsize=12)
    # Add title
    cbar = plt.colorbar()  # shows legend to the side
    cbar.set_label(labText, fontsize=12)
    plt.grid(which="major", axis="both")
    plt.text(90000, 106000, "Carrauntoohil", color="white", ha="left", fontsize="x-large", fontweight="bold")
    plt.plot([80300, 90000], [84400, 106000], color="white")
    plt.title(pltTit, fontsize=14)
    plt.tight_layout()

################### Function to truncate color map ###################
def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    '''truncate_colormap(cmapIn='jet', minval=0.0, maxval=1.0, n=100)'''
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap

#########################################################
# Plot the rainfall data

cmap = plt.get_cmap("YlGnBu")    #YlGnBu 0.2, 1.0
cmap_mod = truncate_colormap(cmap, minval=.2, maxval=1.0)

#PlotMap(MetTMaxMinR["east"], MetTMaxMinR["north"], MetTMaxMinR["ANN"],
#        "Annual Rainfall (mm)", "Ireland Rainfall data", "viridis")
#plt.show()

PlotMap(MetTMaxMinR["east"], MetTMaxMinR["north"], MetTMaxMinR["ANN"],
        "Annual Rainfall (mm)", "Ireland Rainfall data", cmap_mod)
plt.show()


#########################################################
# Plot the elevation data

# Save the value of one data point so that can put in an artificially low value
# so that the color scheme works better
# Don't use this, the cmap modification works best

#tv = MetTMaxMinR.loc[0,"Elev_y"]
#MetTMaxMinR.loc[0,"Elev_y"] = -300
#PlotMap(MetTMaxMinR["east"], MetTMaxMinR["north"], MetTMaxMinR["Elev_y"],
#        "elevation (m)", "Ireland Terrain Height (m)", "terrain")
#plt.show()
#MetTMaxMinR.loc[0,"Elev_y"]= tv






cmap = plt.get_cmap("terrain")
cmap_mod = truncate_colormap(cmap, minval=.2, maxval=.95)

PlotMap(MetTMaxMinR["east"], MetTMaxMinR["north"], MetTMaxMinR["Elev_y"],
        "Elevation (m)", "Ireland Terrain Height", cmap_mod)
plt.show()


#########################################################
# Plot the minimum temp data
PlotMap(MetTMaxMinR["east"], MetTMaxMinR["north"], MetTMaxMinR["minT"],
        "Temperature (" + chr(176) + "C)", "Ireland Minimum Temperature", "winter")
plt.show()

#########################################################
# Plot the maximum temp data

cmap = plt.get_cmap("hot_r")    #YlGnBu 0.2, 1.0
cmap_mod = truncate_colormap(cmap, minval=.1, maxval=0.6)

PlotMap(MetTMaxMinR["east"], MetTMaxMinR["north"], MetTMaxMinR["maxT"],
        "Temperature (" + chr(176) + "C)", "Ireland Maximum Temperature", cmap_mod)  # RdYlGn_r
plt.show()

#################################################################
# DEFINE FUNCTION TO PLOT CORRELATION VERSUS TEMPERATURE OR RAINFALL

def PlotCorr(coordX, coordY, xLab, yLab, pltTit):
    plt.figure(figsize=(9, 10), dpi=80)  # set the size of the image window. figsize x dpi gives the output size
    plt.scatter(coordX, coordY)
    plt.xlabel(xLab, fontsize=12)
    plt.ylabel(yLab, fontsize=12)
    # Add title
#    cbar = plt.colorbar()  # shows legend to the side
#    cbar.set_label(labText, fontsize=12)
    plt.grid(which="major", axis="both")
    plt.title(pltTit, fontsize=14)
    plt.tight_layout()

########################
# CORRELATION OF ELEVATION AND MAX TEMP
PlotCorr(MetTMaxMinR["maxT"], MetTMaxMinR["Elev_y"], "Max temp (" + chr(176) + "C)",
         "Elevation (m)", "Correlation of Elevation and Maximum Temperature")
plt.show()

########################
# CORRELATION OF ELEVATION AND MIN TEMP
PlotCorr(MetTMaxMinR["minT"], MetTMaxMinR["Elev_y"], "Min temp (" + chr(176) + "C)",
         "Elevation (m)", "Correlation of Elevation and Minimum Temperature")
plt.show()

########################
# CORRELATION OF ELEVATION AND RAINFALL
PlotCorr(MetTMaxMinR["ANN"], MetTMaxMinR["Elev_y"], "Annual Rainfall (mm)",
         "Elevation (m)", "Correlation of Elevation and Annual Rainfall")
plt.show()

##########################
# PLOT AREA OF COUNTIES
# Plot bar chart of the area of each county by the count of 1km squares

##################################
# Use seaborn to plot area, ordering by size. Need to create DF in the first place
grDat_Gp = MetTMaxMinR.groupby("County")["County"].count().to_frame(name="Area")
grFinal= grDat_Gp.sort_values(by=["Area"], ascending=False)

grFinal.reset_index(inplace=True)
grList=grFinal["County"].tolist()
print(grList)

sns.set_style("dark")
sns.catplot(y=grDat["County"], kind="count", data=grDat,
            order=grList, palette=sns.color_palette('viridis', n_colors=26),
            height=8, zorder=2)
#plt.figure(figsize=(9, 10), dpi=80)
plt.xlabel("County Area (km\u00b2)", fontsize=11)
plt.ylabel("County Name", fontsize=11)
plt.grid(which="major", axis="both", zorder=1)
plt.title("Comparison of Area of Irish Counties", fontsize=14)
plt.tight_layout()
plt.show()

## end of Seaborn
###############################

# need to create DF of the grouped results and then sort by the area so that plots from smallest to largest
#]grDat_Gp = MetTMaxMinR.groupby("County")["County"].count().to_frame(name="Area")
#]grFinal= grDat_Gp.sort_values(by=["Area"])
#grFinal["Size"]=0
#]grFinal.reset_index(inplace=True)   # reset the index so that can plot properly
#]print(grFinal)

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

# this is the best
#]fig, ax = plt.subplots()
#]fig.set_size_inches(9,7)
#]ax.barh(grFinal["County"], grFinal["Area"], zorder=2)  # zorder specifies the order of drawing
#]ax.set_xlabel("Area km\u00b2")
#]ax.set_ylabel("County")
#]ax.xaxis.set_minor_locator(MultipleLocator(200)) ### set minor tick mark size
#]ax.grid(True, which="minor", zorder=1)
#]ax.xaxis.set_major_locator(MultipleLocator(1000))  # set major tick mark size
#]ax.grid(True, axis="x", which="major", linewidth=2, zorder=1)
#]fig.suptitle("Area of Irish Counties (km\u00b2)")
#]fig.tight_layout()   # removes white space around graph
#]plt.show()

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

#]grDat_El = grDat.groupby("County")["Elev_y"].mean().to_frame(name="ElevMean")
#]grElev= grDat_El.sort_values(by=["ElevMean"])
#]grElev.reset_index(inplace=True)   # reset the index so that can plot properly
#]print(grElev)

#]grDat_El2 = grDat.groupby("County")[["Elev_y"]].mean()  # same as above but creates DF straight away. Keeps elev_y name
#]grElev2= grDat_El2.sort_values(by=["Elev_y"])
#]grElev2.reset_index(inplace=True)
#grFinal["Size"]=0
#grElev.reset_index(inplace=True)   # reset the index so that can plot properly
#]print(grElev2)


# create mean, min, max and stdev of the county elevation and plot with error bars
grDat_El3 = grDat.groupby("County")["Elev_y"].agg([np.mean, min, max, np.std])
grDat_El3.reset_index(inplace=True)
grElev3=grDat_El3.sort_values(["mean"])
print(grDat_El3)

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
ax.grid(True, axis="x", which="major", linewidth=2)
ax.grid(True, axis="y", which="major", linewidth=1)
ax.set_xlabel("Average elevation (m)")
ax.set_ylabel("County")
fig.suptitle("Average elevation of Irish counties with Standard Deviation")
fig.tight_layout()   # removes white space around graph
plt.show()