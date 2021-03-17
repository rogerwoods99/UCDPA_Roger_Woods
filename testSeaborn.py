import matplotlib.pyplot as plt
import shapefile
import numpy as np
from shapely import wkt
from shapely.geometry import Point # Point class
from shapely.geometry import shape # shape() is a function to convert geo objects through the interface
import pandas as pd
from matplotlib.ticker import MultipleLocator
import seaborn as sns

#print("Temperature: "+ str(4)+ chr(176)+ "C")
# get Met Eireann data which already has the elevation and county data included.
# Add a "County" column to store the county name per point
filename="MetEireann_maxT_County.txt"
grDat = pd.read_csv(filename)

filename2="MetEireannBasic_MinT.txt"
grDat2 = pd.read_csv(filename2)

# find the rows with NaN
grNaN= grDat[grDat.isna().any(axis=1)]
#print(grNaN)

#print(grDat.columns)
grDat.dropna(inplace=True)  # drop rows with NaN value
grDat.drop(grDat.columns[0:2], axis=1, inplace=True)  # drop the first 2 columns
grDat.drop(columns="Elev_x", axis=1, inplace=True)  # drop the Elev_x column
print(grDat)


##################################
# Use seaborn to plot area, ordering by size. Need to create DF in the first place
grDat_Gp = grDat.groupby("County")["County"].count().to_frame(name="Area")
grFinal= grDat_Gp.sort_values(by=["Area"], ascending=False)

grFinal.reset_index(inplace=True)
grList=grFinal["County"].tolist()
print(grList)

#sns.set_style("whitegrid")
#sns.set_palette("Purples")
sns.catplot(y=grDat["County"], kind="count", data=grDat,
            order=grList, palette=sns.color_palette('Reds', n_colors=26))
plt.show()

#################################
# use Seaborn to do a count plot. Much faster than matplotlib
sns.countplot(y=grDat["County"])
plt.show()

###########################
#sns.scatterplot(x=grDat["east"], y=grDat["north"], data=grDat, hue=grDat["Elev_y"])
#plt.show()


## testing colours by adding extra variable to pass to the function
def PlotMap(coordX, coordY, coordZ, labText, pltTit, Ucol):
    plt.figure(figsize=(9, 10), dpi=80)  # set the size of the image window. figsize x dpi gives the output size
    plt.scatter(coordX, coordY, 1, c=coordZ, cmap=Ucol)
    plt.xlabel("Easting")
    plt.ylabel("Northing")
    # Add title
    cbar = plt.colorbar()  # shows legend to the side
    cbar.set_label(labText)
    plt.grid(which="major", axis="both")
    plt.text(90000, 106000, "Carrauntoohil", color="white", ha="left", fontsize="x-large", fontweight="bold")
    plt.plot([80300, 90000], [84400, 106000], color="white")
    plt.title(pltTit)

# Plot the minimum temp data
PlotMap(grDat2["east"], grDat2["north"], grDat2["m1Tmin"],
        "temperature (" + chr(176) + "C)", "Ireland Minimum Temperature", "YlGnBu")
plt.show()

#########################################################
# Plot the maximum temp data
PlotMap(grDat["east"], grDat["north"], grDat["m1Tmax"],
        "temperature (" + chr(176) + "C)", "Ireland Maximum Temperature", "OrRd")
plt.show()
