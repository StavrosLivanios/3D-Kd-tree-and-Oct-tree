import pandas as pd
import numpy as np
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
import sys



def build_kn(data, axis, count, node, dir):
    # Find the median of the slice of datasheet and locate the closest point to it
    pin = data.iloc[:, axis]
    pin = pin.to_numpy()
    a = np.median(pin)
    b = pin[min(range(len(pin)), key=lambda i: abs(pin[i] - a))]

    if len(data) == 2:
        # nodes.append(Node('l' + str(len(nodes)), parent=node, axis=axis, value=, dir=dir))
        b = pin[0]


    # Create two new datasheets with the point that are lower or greater than the median point
    columns = ["Airport ID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", "Altitude", "Timezone",
               "DST", "Tz database time zone", "Type", "Source"]
    pinr = pd.DataFrame(columns=columns)
    pinl = pd.DataFrame(columns=columns)
    data.sort_values(by=[str(columns[axis])], inplace=True, ignore_index=True)
    # index = data.index[data[str(columns[axis])] == b].tolist()
    index = data.where(data[str(columns[axis])] == b).last_valid_index()
    pinr = data.iloc[index + 1:]
    pinl = data.iloc[:index + 1]

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

    # creation of root node of kd-tree
    if count == 0:
        nodes.append(Node("root", axis=axis, value=b))
    elif len(data) > 2:
        nodes.append(Node('l' + str(len(nodes)), parent=node, axis=axis, value=b, dir=dir))

    count = count + 1

    # Calculate the axis that the next ittaration will run for
    if axis < 8:
        axis = axis + 1
    else:
        axis = 6
    # print(a)
    # print(b)
    # print(pinl)
    # Call the recursing funchion for the next step
    x = nodes[-1]
    y=nodes[-1]




    if len(pinl) > 1:
        build_kn(pinl, axis, count, x , "left")
    elif len(pinl) == 1:
        nodes.append(Node('leaf' + str(len(nodes)), parent=node, dir="left"))
    if len(pinr) > 1:
        build_kn(pinr, axis, count, y , "right")
    elif len(pinr) == 1:
        nodes.append(Node('leaf' + str(len(nodes)), parent=node, dir="right"))

print("gea sou ")
sys.setrecursionlimit(13000)
count = 0
nodes = []
data = pd.read_csv("airports-extended.txt", sep=",", header=None)
data.columns = ["Airport ID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", "Altitude",
                "Timezone", "DST", "Tz database time zone", "Type", "Source"]
data.drop_duplicates(subset=("Latitude", "Longitude", "Altitude"), keep='first', inplace=True, ignore_index=True)
# print(len(data))
build_kn(data, 6, 0, "root", "root")


print("hello")
DotExporter(nodes[0]).to_dotfile("root.dot")
