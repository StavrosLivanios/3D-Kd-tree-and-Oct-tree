import pandas as pd
import numpy as np


def build_kn(data,axis):
    pin = data.iloc[:,axis]
    pin=pin.to_numpy()
    a = np.median(pin)
    b=pin[min(range(len(pin)), key = lambda i: abs(pin[i]-a))]
    #pinr=[]
    #pinl=[]
    columns = ["Airport ID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", "Altitude", "Timezone","DST", "Tz database time zone", "Type", "Source"]
    pinr = pd.DataFrame(columns=columns)
    pinl = pd.DataFrame(columns=columns)
    count1=0
    count2=0
    for i in range(len(pin)):
        if pin[i]>=a :
             pinr.loc[count1]=data.loc[i]
             count1=count1+1
        else:
             pinl.loc[count2]=data.loc[i]
             count2=count2+1
    if axis<8:
        axis=axis+1
    else:
        axis=6

    print(b)
    if len(pinr)>0 :
        build_kn(pinl,axis)
    if len(pinl) > 0:
        build_kn(pinr,axis)

print("gea sou ")



data = pd.read_csv("airports-extended.txt", sep=",", header=None)
data.columns = ["Airport ID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", "Altitude", "Timezone", "DST", "Tz database time zone", "Type", "Source"]
build_kn(data,6)