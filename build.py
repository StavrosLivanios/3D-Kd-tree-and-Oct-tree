import pandas as pd
import numpy as np
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
import sys


def build_kn(data, axis, count, node, dir):
    # sort the array by the axis that we use
    # and take an array only with the axis we will use
    # and transform them in the state we need
    columns = ["Airport ID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", "Altitude", "Timezone",
               "DST", "Tz database time zone", "Type", "Source"]
    data.sort_values(by=[str(columns[axis])], inplace=True, ignore_index=True)
    pin = data.iloc[:, axis]
    pin = pin.to_numpy()

    # Find the median of the slice of datasheet and locate the closest point to it
    a = np.median(pin)
    b = pin[min(range(len(pin)), key=lambda i: abs(pin[i] - a))]

    # hadling for size 2 data
    if len(pin) == 2:
        b = pin[0]

    # spliting the data sheet to right and left
    pinr = pd.DataFrame(columns=columns)
    pinl = pd.DataFrame(columns=columns)
    index = data.where(data[str(columns[axis])] == b).last_valid_index()
    pinr = data.iloc[index + 1:]
    pinl = data.iloc[:index + 1]

    # creation of root node of kd-tree
    if count == 0:
        nodes.append(Node("root", axis=axis, value=b))
    # creation of nodes
    elif len(data) >= 2:
        nodes.append(Node('l' + str(len(nodes)), parent=node, axis=axis, value=b, dir=dir))

    count = count + 1

    # Calculate the axis that the next ittaration will run for
    if axis < 8:
        axis = axis + 1
    else:
        axis = 6

    # Call the recursing funchion for the next step
    # or creqate the leaf
    x = nodes[-1]
    if len(pinl) > 1:
        build_kn(pinl, axis, count, x, "left")
    elif len(pinl) == 1:
        nodes.append(Node('leaf_Left ' + str(pinl.iloc[0, 0]), parent=x, dir="left", Airport_ID=pinl.iloc[0, 0],
                          Name=pinl.iloc[0, 1], City=pinl.iloc[0, 2], Country=pinl.iloc[0, 3], IATA=pinl.iloc[0, 4],
                          ICAO=pinl.iloc[0, 5],
                          Latitude=pinl.iloc[0, 6], Longitude=pinl.iloc[0, 7], Altitude=pinl.iloc[0, 8],
                          Timezone=pinl.iloc[0, 9],
                          DST=pinl.iloc[0, 10], Tz_database_time_zone=pinl.iloc[0, 11], Type=pinl.iloc[0, 12],
                          Source=pinl.iloc[0, 13]))

    if len(pinr) > 1:
        build_kn(pinr, axis, count, x, "right")
    elif len(pinr) == 1:
        nodes.append(Node('leaf_Right ' + str(pinr.iloc[0, 0]), parent=x, dir="right", Airport_ID=pinr.iloc[0, 0],
                          Name=pinr.iloc[0, 1], City=pinr.iloc[0, 2], Country=pinr.iloc[0, 3], IATA=pinr.iloc[0, 4],
                          ICAO=pinr.iloc[0, 5],
                          Latitude=pinr.iloc[0, 6], Longitude=pinr.iloc[0, 7], Altitude=pinr.iloc[0, 8],
                          Timezone=pinr.iloc[0, 9],
                          DST=pinr.iloc[0, 10], Tz_database_time_zone=pinr.iloc[0, 11], Type=pinr.iloc[0, 12],
                          Source=pinr.iloc[0, 13]))



sys.setrecursionlimit(13000)
nodes = []
data = pd.read_csv("airports-extended.txt", sep=",", header=None)
data.columns = ["Airport ID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", "Altitude",
                "Timezone", "DST", "Tz database time zone", "Type", "Source"]
data.drop_duplicates(subset=("Latitude", "Longitude", "Altitude"), keep='first', inplace=True, ignore_index=True)
build_kn(data, 6, 0, "root", "root")
print("hello")
DotExporter(nodes[0]).to_dotfile("root.dot")
