
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
#from pyproj import Proj, transform
from pyproj import Transformer
import numpy as np
import time
import requests
import json

# create DF to hold the results so that they can be merged with the initial values
ElevRes = pd.DataFrame(columns=['Latit', 'Longit', 'Elev'])

# function to create the url to pass to the website to get the elevation data
def CreateURL(w, url):
    for s in range(w):
        url=url + str(grDat.loc[y*100 + s,"Latit"]) + "," + str(grDat.loc[y*100 + s,"Longit"]) + "|"
    url = url[:-1]   # remove the final "|" character before passing back
    return url

# function to send the URL and then save the results to the output array
def SendURL(url, ElevRess):
    # send the request and then extract the data from the "results" record in the JSON file
    r = requests.get(url)
    json_data = r.json()
    newlist = pd.json_normalize(json_data, record_path=["results"])

    # filter the list to take coords and elevation
    elev = newlist.filter(["location.lat", "location.lng", "elevation"], axis=1)
    elev.rename(columns={"location.lat": "Latit", "location.lng": "Longit", "elevation": "Elev"}, inplace=True)

    # concat the results to new DF and then rename so that ready for next set of results
    ElevRes2 = pd.concat([ElevRess, elev], ignore_index=True)
    ElevRess = ElevRes2
    return ElevRess

# transform to and from Irish Grid and Lat Long
transformerToXY = Transformer.from_crs("epsg:4326", "epsg:29902")
transformerFromXY = Transformer.from_crs("epsg:29902", "epsg:4326")

######################
# load file and create DF

filename="MetEireannTemp.txt"
grDat=pd.read_csv(filename)

#print(grDat)

# convert the Easting and Northing column data to numpy arrays
ListEast=grDat["east"].to_numpy()
ListNorth=grDat["north"].to_numpy()

# convert the East and North data to latitude longitude
respArr=transformerFromXY.transform(ListEast,ListNorth)  # pass pts in dataframe

# create new dataframes of the results, rounded to 6 dp
newDFLat=np.around(pd.DataFrame(respArr[0]),decimals=6)
newDFLong=np.around(pd.DataFrame(respArr[1]),decimals=6)

# add these dataframes to the original DF. Also add the Elev column that will hold the elevation data at a later stage
grDat["Latit"]=newDFLat
grDat["Longit"]=newDFLong
grDat["Elev"]=0

# create the header for the URL to get elevation data for each point
urlhead='https://api.opentopodata.org/v1/eudem25m?locations='

# loop through the elements in the dataframe
# need to set up 2 nested loops so that can repeat the 100 requests

for y in range(842):   # 842 is the final number
    time.sleep(0.5)   # insert 0.5 second delay so that don't exceed the 1 per second URL request limit

    # get the complete URL using the CreateURL function
    url1 = CreateURL(100, urlhead)
    print(y)
    ElevRes = SendURL(url1, ElevRes)  # call the function to send URL and place data in dataframe

# call the function to get the last 91 values
# get the complete URL from the function
y=842
url1 = CreateURL(91, urlhead)
ElevRes = SendURL(url1, ElevRes)

print(ElevRes)

# merge the existing Met Eireann data with the new elevation information
grDat_new=grDat.merge(ElevRes, on=["Latit","Longit"], how="left")

# output to CSV for future analysis
grDat_new.to_csv("MetEireann out.txt")

