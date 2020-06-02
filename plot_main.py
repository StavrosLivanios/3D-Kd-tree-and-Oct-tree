import ast
import os
import sys
import pandas as pd
from anytree.exporter import DictExporter
from anytree.exporter import DotExporter
from anytree.importer import DictImporter
from timeit import default_timer as timer
# imports for KD and OCT trees
from matplotlib import patches

#from build import build_kd, nodes, build_oct, nodes_oct,values_kd_x,values_kd_y,values_kd_z

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from anytree import Node

nodes = []
values_kd_x = []
values_kd_y = []
values_kd_z = []
nodes_oct = []
oct_lists_temp = []
counter_list = 0


# --------------------------------------------------LIST-SEPERATOR-------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------

def list_separator(data, axis, point):
    if axis == 6:
        point_cord = 0
    elif axis == 7:
        point_cord = 1
    elif axis == 8:
        point_cord = 2
    else:
        oct_lists_temp.append(data)
        return

    columns = ["Airport ID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", "Altitude", "Timezone",
               "DST", "Tz database time zone", "Type", "Source"]
    data.sort_values(by=[str(columns[axis])], inplace=True, ignore_index=True)
    pin = data.iloc[:, axis]
    pin = pin.to_numpy()
    a = point[point_cord]
    pinr = pd.DataFrame(columns=columns)
    pinl = pd.DataFrame(columns=columns)
    if len(pin) != 0:
        b = pin[min(range(len(pin)), key=lambda i: abs(pin[i] - a))]
        # spliting the data sheet to right and left
        index = data.where(data[str(columns[axis])] == b).last_valid_index()

        if float(data.iloc[index, axis]) <= point[point_cord]:
            pinr = data.iloc[index + 1:]
            pinl = data.iloc[:index + 1]
        else:
            index = data.where(data[str(columns[axis])] == b).last_valid_index()
            pinr = data.iloc[index:]
            pinl = data.iloc[:index]
    axis = axis + 1
    list_separator(pinl, axis, point)
    list_separator(pinr, axis, point)


# --------------------------------------------------KD-TREE-------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------

def kd_visual(data, axis, count, ax,cut_axis,low_x,high_x,low_y,high_y):

    #print( str(low_x) +" "+  str(high_x) +" "+  str(low_y) +" "+ str(high_y))

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
# -=======================================================
    # creation of root node of kd-tree
    if count == 0:
        plt.scatter(data.Latitude, data.Longitude)
        rect = patches.Rectangle((data.Latitude.min(), data.Longitude.min()), (data.Latitude.max() - data.Latitude.min()),  (data.Longitude.max()- data.Longitude.min()), linewidth=1, edgecolor='g', facecolor='none')
        ax.add_patch(rect)

        #rect = patches.Rectangle((data.Latitude.min() - 1, data.Longitude.min() - 2),(b - data.Latitude.min()) + 10, (data.Longitude.max() - data.Longitude.min()) + 10, linewidth=1, edgecolor='r',facecolor='none')



        ax.add_patch(rect)
        low_x = data.Latitude.min()
        high_x = data.Latitude.max()
        low_y = data.Longitude.min()
        high_y = data.Longitude.max()

        plt.plot([b, b], [low_y, high_y], "r",linewidth=3)

    else:

        if axis != 8:

            if cut_axis == "x":
                #rect = patches.Rectangle((low_x, low_y),(b - low_x),(high_y - low_y), linewidth=1, edgecolor='r',facecolor='none')
                plt.plot([b,b],[low_y,high_y],"r", linewidth=2-(count * 0.2))
                #ax.add_patch(rect)
            else:
                plt.plot([low_x, high_x], [b, b], "b", linewidth=2-(count * 0.2))
                #rect = patches.Rectangle((low_x, low_y), (high_x - low_x), (b - low_y), linewidth=1, edgecolor='b', facecolor='none')
                #ax.add_patch(rect)

            #low_x = data.Latitude.min()
            #high_x = data.Latitude.max()
            #low_y = data.Longitude.min()
            #high_y = data.Longitude.max()


    count = count + 1

    # Calculate the axis that the next ittaration will run for
    if axis < 7:
        axis = axis + 1
    else:
        axis = 6


    if cut_axis == "x":
        cut_axis = "y"
        if len(pinl) >1:
            kd_visual(pinl, axis, count, ax, cut_axis, low_x, b, low_y, high_y)

        if len(pinr) > 1:
            kd_visual(pinr, axis, count, ax, cut_axis, b, high_x, low_y, high_y)

    else:
        cut_axis = "x"
        if len(pinl) > 1:
            kd_visual(pinr, axis, count, ax, cut_axis, low_x, high_x, b, high_y)

        if len(pinr) > 1:
            kd_visual(pinl, axis, count, ax, cut_axis, low_x, high_x, low_y, b)

# --------------------------------------------------OCT-TREE-------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------


def oct_visual(data, parent, low_x, high_x, low_y, high_y, low_z, high_z,count):
    count = count + 1
    if parent == "root":

        plt.scatter(data.Latitude, data.Longitude)
        rect = patches.Rectangle((data.Latitude.min(), data.Longitude.min()), (data.Latitude.max() - data.Latitude.min()),  (data.Longitude.max()- data.Longitude.min()), linewidth=1, edgecolor='g', facecolor='none')
        ax.add_patch(rect)

        low_x = data.Latitude.min()
        high_x = data.Latitude.max()
        low_y = data.Longitude.min()
        high_y = data.Longitude.max()

        min_x = data.min()["Latitude"]
        max_x = data.max()["Latitude"]
        meso_x = (min_x + max_x) / 2

        min_y = data.min()["Longitude"]
        max_y = data.max()["Longitude"]
        meso_y = (max_y + min_y) / 2

        min_z = data.min()["Altitude"]
        max_z = data.max()["Altitude"]
        meso_z = (max_z + min_z) / 2

        plt.plot([meso_x, meso_x], [low_y, high_y], "r", linewidth=3)
        plt.plot([low_x, high_x], [meso_y, meso_y], "b", linewidth=3)

    else:
        min_x = low_x
        max_x = high_x
        meso_x = (min_x + max_x) / 2

        min_y = low_y
        max_y = high_y
        meso_y = (max_y + min_y) / 2

        min_z = low_z
        max_z = high_z
        meso_z = (max_z + min_z) / 2

        plt.plot([meso_x, meso_x], [low_y, high_y], "r", linewidth=2-(count * 0.2))
        plt.plot([low_x, high_x], [meso_y, meso_y], "b", linewidth=2-(count * 0.2))

    global oct_lists_temp
    oct_lists_temp = []
    list_separator(data, 6, [meso_x, meso_y, meso_z])
    oct_lists = oct_lists_temp


    for i in range(8):

        if len(oct_lists[i]) > 8:
            if i == 0:
                oct_visual(oct_lists[i], "noroot", low_x, meso_x, low_y, meso_y, low_z, meso_z,count)
            elif i == 2:
                oct_visual(oct_lists[i], "noroot", low_x, meso_x, meso_y, high_y, low_z, meso_z,count)
            elif i == 4:
                oct_visual(oct_lists[i], "noroot", meso_x, high_x, low_y, meso_y, low_z, meso_z,count)
            elif i == 6:
                oct_visual(oct_lists[i], "noroot", meso_x, high_x, meso_y, high_y, low_z, meso_z,count)
            elif i == 1:
                oct_visual(oct_lists[i], "noroot", low_x, meso_x, low_y, meso_y, meso_z, high_z,count)
            elif i == 3:
                oct_visual(oct_lists[i], "noroot", low_x, meso_x, meso_y, high_y, meso_z, high_z,count)
            elif i == 5:
                oct_visual(oct_lists[i], "noroot", meso_x, high_x, low_y, meso_y, meso_z, high_z,count)
            elif i == 7:
                oct_visual(oct_lists[i], "noroot", meso_x, high_x, meso_y, high_y, meso_z, high_z,count)




data = pd.read_csv("airports-extended100.txt", sep=",", header=None)
data.columns = ["Airport ID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", "Altitude",
                "Timezone", "DST", "Tz database time zone", "Type", "Source"]
data.drop_duplicates(subset=("Latitude", "Longitude", "Altitude"), keep='first', inplace=True,
                     ignore_index=True)
fig, ax = plt.subplots(1)
kd_visual(data, 6, 0 , ax,"x",0,0,0,0)
plt.show()


fig, ax = plt.subplots(1)
oct_visual(data, "root",0 , 0, 0,0,0,0,0)
plt.show()

