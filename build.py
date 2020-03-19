import pandas as pd
import numpy as np


# import sys


def build_kn(data, axis, count):
    if len(data) < 2:
        return
    if not len(data):
        return
    pin = data.iloc[:, axis]
    pin = pin.to_numpy()
    # print(pin)

    a = np.median(pin)
    b = pin[min(range(len(pin)), key=lambda i: abs(pin[i] - a))]

    # pinr=[]
    # pinl=[]
    columns = ["Airport ID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", "Altitude", "Timezone",
               "DST", "Tz database time zone", "Type", "Source"]
    pinr = pd.DataFrame(columns=columns)
    pinl = pd.DataFrame(columns=columns)

    data.sort_values(by=[str(columns[axis])], inplace=True, ignore_index=True)
    index = data.index[data[str(columns[axis])] == b].tolist()
    #print(index)

    pinr = data.iloc[index[0]:]
    pinl = data.iloc[:index[0]]

    '''if len(pinr)==0 :
        return
    if len(pinl)==0:
        return'''

    '''count1 = 0
    count2 = 0
    for i in range(len(pin)):
        if pin[i] > a:
            pinr.loc[count1] = data.loc[i]
            count1 = count1 + 1
        else:
            pinl.loc[count2] = data.loc[i]
            count2 = count2 + 1'''

    # gia pion ajona ua ektelestei
    if axis < 8:
        axis = axis + 1
    else:
        axis = 6

    print(a)
    print(pinr)
    x = "count: " + str(count)
    #print(x)
    count = count + 1
    if len(pinl) > 2:
        build_kn(pinl, axis, count)
    if len(pinr) > 2:
        build_kn(pinr, axis, count)


print("gea sou ")
# sys.setrecursionlimit(3000)
count = 0
data = pd.read_csv("airports-extended.txt", sep=",", header=None)
data.columns = ["Airport ID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", "Altitude",
                "Timezone", "DST", "Tz database time zone", "Type", "Source"]
data.drop_duplicates(subset=("Latitude", "Longitude", "Altitude"), keep='first', inplace=True, ignore_index=True)
# print(len(data))
build_kn(data, 6, 0)
