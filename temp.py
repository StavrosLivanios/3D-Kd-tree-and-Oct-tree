# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd 
from sklearn.cluster import KMeans
import numpy as np

data = pd.read_csv("airports-extended.txt", sep=",", header=None)
data.columns = ["Airport ID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", "Altitude", "Timezone", "DST", "Tz database time zone", "Type", "Source"]

#data.head;
pin = data.iloc[:,7] 
pin=pin.to_numpy()
pin=pin.reshape(-1, 1)
#in2 = np.array(pin)
#pin=np.array(data)


kmeans = KMeans(n_clusters=1, random_state=0).fit(pin)
centers=kmeans.cluster_centers_
print("1")