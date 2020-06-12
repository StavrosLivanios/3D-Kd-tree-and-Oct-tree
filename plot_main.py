
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


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

def kd_visual(data, axis, count, ax,cut_axis,low_x,high_x,low_y,high_y,low_z,high_z):
    if len(data) == 0 :
        return
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
        ax.scatter3D(data.Latitude, data.Longitude, data.Altitude, 'gray')

        low_x = data.Latitude.min()
        high_x = data.Latitude.max()
        low_y = data.Longitude.min()
        high_y = data.Longitude.max()
        low_z = data.Altitude.min()
        high_z = data.Altitude.max()

        ax.plot3D((b, b), (low_y, high_y), (low_z, high_z), 'red', linewidth=3)

    else:


            if cut_axis == "x":
                ax.plot3D((b, b), (low_y, high_y), (low_z, high_z), 'red', linewidth=2-(count * 0.2))
            elif cut_axis == "y":
                ax.plot3D((low_x, high_x), (b, b), (low_z, high_z), 'blue', linewidth=2-(count * 0.2))
            else:
                ax.plot3D((low_x, high_x), (low_y, high_y), (b, b), 'green', linewidth=2-(count * 0.2))

    count = count + 1
    # Calculate the axis that the next ittaration will run for
    if axis < 8:
        axis = axis + 1
    else:
        axis = 6

    if cut_axis == "x":
        cut_axis = "y"
        if len(pinl) >1:
            kd_visual(pinl, axis, count, ax, cut_axis, low_x, b, low_y, high_y,low_z,high_z)

        if len(pinr) > 1:
            kd_visual(pinr, axis, count, ax, cut_axis, b, high_x, low_y, high_y,low_z,high_z)

    elif cut_axis=="y":
        cut_axis = "z"
        if len(pinl) > 1:
            kd_visual(pinr, axis, count, ax, cut_axis, low_x, high_x, b, high_y,low_z,high_z)

        if len(pinr) > 1:
            kd_visual(pinl, axis, count, ax, cut_axis, low_x, high_x, low_y, b,low_z,high_z)

    elif cut_axis == "z":
        cut_axis = "x"
        if len(pinl) > 1:
            kd_visual(pinr, axis, count, ax, cut_axis, low_x, high_x, low_y, high_y,b,high_z)

        if len(pinr) > 1:
            kd_visual(pinl, axis, count, ax, cut_axis, low_x, high_x, low_y, high_y,low_z,b)
# --------------------------------------------------OCT-TREE-------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------


def oct_visual(data, parent, low_x, high_x, low_y, high_y, low_z, high_z,count,ax):
    count = count + 1
    if parent == "root":
        ax.scatter3D(data.Latitude, data.Longitude, data.Altitude, 'gray')
        #ax.plot3D((data.Latitude.min(), data.Longitude.min(),  data.Latitude.min()), (data.Latitude.min(), data.Longitude.max(),  data.Latitude.max()), 'gray')

        #plt.scatter(data.Latitude, data.Longitude)
        #rect = patches.Rectangle((data.Latitude.min(), data.Longitude.min()), (data.Latitude.max() - data.Latitude.min()),  (data.Longitude.max()- data.Longitude.min()), linewidth=1, edgecolor='g', facecolor='none')
        #ax.add_patch(rect)

        low_x = data.Latitude.min()
        high_x = data.Latitude.max()
        low_y = data.Longitude.min()
        high_y = data.Longitude.max()
        low_z = data.Altitude.min()
        high_z = data.Altitude.max()

        min_x = data.min()["Latitude"]
        max_x = data.max()["Latitude"]
        meso_x = (min_x + max_x) / 2

        min_y = data.min()["Longitude"]
        max_y = data.max()["Longitude"]
        meso_y = (max_y + min_y) / 2

        min_z = data.min()["Altitude"]
        max_z = data.max()["Altitude"]
        meso_z = (max_z + min_z) / 2

        ax.plot3D((meso_x, meso_x),(low_y, high_y), (low_z, high_z), 'red',linewidth=3)
        ax.plot3D((low_x, high_x),(meso_y, meso_y), (meso_z, meso_z), 'blue',linewidth=3)
        ax.plot3D((low_x, high_x), (low_y, high_y), (meso_z, meso_z), 'green',linewidth=3)
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

        ax.plot3D((meso_x, meso_x), (low_y, high_y), (low_z, high_z), 'red', linewidth=2.5-(count * 0.3))
        ax.plot3D((low_x, high_x), (meso_y, meso_y), (meso_z, meso_z), 'blue', linewidth=2.5-(count * 0.3))
        ax.plot3D((low_x, high_x), (low_y, high_y), (meso_z, meso_z), 'green', linewidth=2.5-(count * 0.3))

    global oct_lists_temp
    oct_lists_temp = []
    list_separator(data, 6, [meso_x, meso_y, meso_z])
    oct_lists = oct_lists_temp

    draw = 0
    for i in range(8):

        if len(oct_lists[i]) > 8:
            if i == 0:
                oct_visual(oct_lists[i], "noroot", low_x, meso_x, low_y, meso_y, low_z, meso_z,count,ax)
            elif i == 2:
                oct_visual(oct_lists[i], "noroot", low_x, meso_x, meso_y, high_y, low_z, meso_z,count,ax)
            elif i == 4:
                oct_visual(oct_lists[i], "noroot", meso_x, high_x, low_y, meso_y, low_z, meso_z,count,ax)
            elif i == 6:
                oct_visual(oct_lists[i], "noroot", meso_x, high_x, meso_y, high_y, low_z, meso_z,count,ax)
            elif i == 1:
                oct_visual(oct_lists[i], "noroot", low_x, meso_x, low_y, meso_y, meso_z, high_z,count,ax)
            elif i == 3:
                oct_visual(oct_lists[i], "noroot", low_x, meso_x, meso_y, high_y, meso_z, high_z,count,ax)
            elif i == 5:
                oct_visual(oct_lists[i], "noroot", meso_x, high_x, low_y, meso_y, meso_z, high_z,count,ax)
            elif i == 7:
                oct_visual(oct_lists[i], "noroot", meso_x, high_x, meso_y, high_y, meso_z, high_z,count,ax)

