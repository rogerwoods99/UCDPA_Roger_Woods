import matplotlib.pyplot as plt
import shapefile
import numpy as np
from shapely import wkt
from shapely.geometry import Point # Point class
from shapely.geometry import shape # shape() is a function to convert geo objects through the interface
import pandas as pd
from matplotlib.ticker import MultipleLocator
import seaborn as sns

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
sns.scatterplot(x=grDat["east"], y=grDat["north"], data=grDat, hue=grDat["Elev_y"])
plt.show()

