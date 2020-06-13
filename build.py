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

#This function returns the hypothetical position of the point inside the cube that is seperated in 8 subspaces
#position refers to the subspace that the point belongs  
def find_position(point, meso_point):
    if meso_point[0] >= float(point[0]) and meso_point[1] >= float(point[1]) and meso_point[2] >= float(
            point[2]):
        position = 0
    elif meso_point[0] >= float(point[0]) and meso_point[1] >= float(point[1]) and meso_point[2] < float(
            point[2]):
        position = 1
    elif meso_point[0] >= float(point[0]) and meso_point[1] < float(point[1]) and meso_point[2] >= float(
            point[2]):
        position = 2
    elif meso_point[0] >= float(point[0]) and meso_point[1] < float(point[1]) and meso_point[2] < float(
            point[2]):
        position = 3
    elif meso_point[0] < float(point[0]) and meso_point[1] >= float(point[1]) and meso_point[2] >= float(
            point[2]):
        position = 4
    elif meso_point[0] < float(point[0]) and meso_point[1] >= float(point[1]) and meso_point[2] < float(
            point[2]):
        position = 5
    elif meso_point[0] < float(point[0]) and meso_point[1] < float(point[1]) and meso_point[2] >= float(
            point[2]):
        position = 6
    elif meso_point[0] < float(point[0]) and meso_point[1] < float(point[1]) and meso_point[2] < float(
            point[2]):
        position = 7
    return position


# --------------------------------------------------LIST-SEPERATOR-------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------
#In each ittaration we divede the points to two lists until we get 8 sublists that 
#each one refers to the corresponding subspaces
def list_separator(data, axis, point):
    # configure axis point
    if axis == 6:
        point_cord = 0
    elif axis == 7:
        point_cord = 1
    elif axis == 8:
        point_cord = 2
    else:
        oct_lists_temp.append(data)
        return
    # set columns names
    columns = ["Airport ID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", "Altitude", "Timezone",
               "DST", "Tz database time zone", "Type", "Source"]
    data.sort_values(by=[str(columns[axis])], inplace=True, ignore_index=True)
    pin = data.iloc[:, axis]
    pin = pin.to_numpy()
    a = point[point_cord]

    # divide dataframe into to sublists
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

# In this function we build the Kd tree by taking the dataset and dividing it recursively
# in two lists(that they represent the branches of the tree) separeted by their median point. Each time we separate we create a new node until 
# the lenght of the lists is 2  in wich case we create a right and left leaf.
def build_kd(data, axis, count, node, dir):
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
        nodes.append(Node("root", axis=axis, value=b, layout='sfdp'))
    # creation of node
    elif len(data) >= 2:
        nodes.append(Node('l' + str(len(nodes)), parent=node, axis=axis, value=b, dir=dir))

    count = count + 1

    # Calculate the axis that the next ittaration will run for(6 is x , 7 is y , 8 is z)
    if axis < 8:
        axis = axis + 1
    else:
        axis = 6

    # Call the recursing function for the next step
    # or create the leaf
    # We call the function for the left subtree(with pinl) 
    # and for the right (with pinr) 
    x = nodes[-1]
    if len(pinl) > 1:
        build_kd(pinl, axis, count, x, "left")
    elif len(pinl) == 1:
        nodes.append(Node('leaf ' + str(pinl.iloc[0, 0]), parent=x, dir="left", Airport_ID=pinl.iloc[0, 0],
                          Name=pinl.iloc[0, 1], City=pinl.iloc[0, 2], Country=pinl.iloc[0, 3], IATA=pinl.iloc[0, 4],
                          ICAO=pinl.iloc[0, 5],
                          Latitude=pinl.iloc[0, 6], Longitude=pinl.iloc[0, 7], Altitude=pinl.iloc[0, 8],
                          Timezone=pinl.iloc[0, 9],
                          DST=pinl.iloc[0, 10], Tz_database_time_zone=pinl.iloc[0, 11], Type=pinl.iloc[0, 12],
                          Source=pinl.iloc[0, 13]))

    if len(pinr) > 1:
        build_kd(pinr, axis, count, x, "right")
    elif len(pinr) == 1:
        nodes.append(Node('leaf_Right ' + str(pinr.iloc[0, 0]), parent=x, dir="right", Airport_ID=pinr.iloc[0, 0],
                          Name=pinr.iloc[0, 1], City=pinr.iloc[0, 2], Country=pinr.iloc[0, 3], IATA=pinr.iloc[0, 4],
                          ICAO=pinr.iloc[0, 5],
                          Latitude=pinr.iloc[0, 6], Longitude=pinr.iloc[0, 7], Altitude=pinr.iloc[0, 8],
                          Timezone=pinr.iloc[0, 9],
                          DST=pinr.iloc[0, 10], Tz_database_time_zone=pinr.iloc[0, 11], Type=pinr.iloc[0, 12],
                          Source=pinr.iloc[0, 13]))


# --------------------------------------------------OCT-TREE-------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------
# In this function we build the Oct tree by taking the dataset and dividing it recursively
# in eight lists(that they represent the subspaces of the cube) separeted by their middle points(x,y,z). Each time we separate we create a new node until 
# the lenght of the lists is 8 or less  in wich case we create leafs.
def build_oct(data, parent, low_x, high_x, low_y, high_y, low_z, high_z, i ,meso_x,meso_y,meso_z):
    # find middle value of  axis' edges
    # and initialize the edges of the first cube
    if parent == "root":
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
        
        # create node root
        nodes_oct.append(
            Node("root", value_x=meso_x, value_y=meso_y, value_z=meso_z, layout='sfdp', low_x=low_x, high_x=high_x,
                 low_y=low_y, high_y=high_y, low_z=low_z, high_z=high_z))
        parent = nodes_oct[-1]


    #If the lenght of the list is 8 or less we create the leafs
    if (len(data) <= 8) and (len(data) > 0):
        for j in range(len(data)):
            pos = find_position([float(data.iloc[j, 6]), float(data.iloc[j, 7]), float(data.iloc[j, 8])],[parent.value_x, parent.value_y, parent.value_z])
            nodes_oct.append(Node('leaf ' + str(data.iloc[j, 0]), parent=parent, position=pos,
                                  Airport_ID=data.iloc[j, 0],
                                  Name=data.iloc[j, 1], City=data.iloc[j, 2],
                                  Country=data.iloc[j, 3], IATA=data.iloc[j, 4],
                                  ICAO=data.iloc[j, 5],
                                  Latitude=data.iloc[j, 6], Longitude=data.iloc[j, 7],
                                  Altitude=data.iloc[j, 8],
                                  Timezone=data.iloc[j, 9],
                                  DST=data.iloc[j, 10], Tz_database_time_zone=data.iloc[j, 11],
                                  Type=data.iloc[j, 12],
                                  Source=data.iloc[j, 13]))
                                  
    # call list separator to seperate the cube to the 8 subspaces
    elif len(data) > 8:
        global oct_lists_temp
        oct_lists_temp = []
        list_separator(data, 6, [parent.value_x, parent.value_y, parent.value_z])
        oct_lists = oct_lists_temp

        #For each list returned from list_separator we calculate the new subcube dimensions 
        #and we create the node that will represent it. We call the build_oct function with the new dimensions of the new subspace.
        for k in range(8):
        
        # subspace -->  0:front lower left  (k==0) | 1:back lower left  (k==1)
        #               2:front upper left  (k==2) | 3:back upper left  (k==3)
        #               4:front lower right (k==4) | 5:back lower right (k==5)
        #               6:front upper right (k==6) | 7:back upper right (k==7)
        
            if len(oct_lists[k]) > 1:
                if k == 0:
                    temp_meso_x = (low_x + meso_x) / 2
                    temp_meso_y = (low_y + meso_y) / 2
                    temp_meso_z = (low_z + meso_z) / 2
                    nodes_oct.append(
                        Node('l' + str(len(nodes_oct)), parent=parent, position=k, value_x=temp_meso_x,
                             value_y=temp_meso_y,
                             value_z=temp_meso_z, low_x=low_x, high_x=meso_x, low_y=low_y, high_y=meso_y, low_z=low_z,
                             high_z=meso_z))
                    build_oct(oct_lists[k], nodes_oct[-1], low_x, meso_x, low_y, meso_y, low_z, meso_z, k, temp_meso_x,
                              temp_meso_y, temp_meso_z)
                elif k == 2:
                    temp_meso_x = (low_x + meso_x) / 2
                    temp_meso_y = (meso_y + high_y) / 2
                    temp_meso_z = (low_z + meso_z) / 2
                    nodes_oct.append(
                        Node('l' + str(len(nodes_oct)), parent=parent, position=k, value_x=temp_meso_x,
                             value_y=temp_meso_y,
                             value_z=temp_meso_z, low_x=low_x, high_x=meso_x, low_y=meso_y, high_y=high_y, low_z=low_z,
                             high_z=meso_z))
                    build_oct(oct_lists[k], nodes_oct[-1], low_x, meso_x, meso_y, high_y, low_z, meso_z, k, temp_meso_x,
                              temp_meso_y, temp_meso_z)
                elif k == 4:
                    temp_meso_x = (meso_x + high_x) / 2
                    temp_meso_y = (low_y + meso_y) / 2
                    temp_meso_z = (low_z + meso_z) / 2
                    nodes_oct.append(
                        Node('l' + str(len(nodes_oct)), parent=parent, position=k, value_x=temp_meso_x,
                             value_y=temp_meso_y,
                             value_z=temp_meso_z, low_x=meso_x, high_x=high_x, low_y=low_y, high_y=meso_y, low_z=low_z,
                             high_z=meso_z))
                    build_oct(oct_lists[k], nodes_oct[-1], meso_x, high_x, low_y, meso_y, low_z, meso_z, k, temp_meso_x,
                              temp_meso_y, temp_meso_z)
                elif k == 6:
                    temp_meso_x = (meso_x + high_x) / 2
                    temp_meso_y = (meso_y + high_y) / 2
                    temp_meso_z = (low_z + meso_z) / 2
                    nodes_oct.append(
                        Node('l' + str(len(nodes_oct)), parent=parent, position=k, value_x=temp_meso_x,
                             value_y=temp_meso_y,
                             value_z=temp_meso_z, low_x=meso_x, high_x=high_x, low_y=meso_y, high_y=high_y, low_z=low_z,
                             high_z=meso_z))
                    build_oct(oct_lists[k], nodes_oct[-1], meso_x, high_x, meso_y, high_y, low_z, meso_z, k,
                              temp_meso_x, temp_meso_y, temp_meso_z)
                elif k == 1:
                    temp_meso_x = (low_x + meso_x) / 2
                    temp_meso_y = (low_y + meso_y) / 2
                    temp_meso_z = (meso_z + high_z) / 2
                    nodes_oct.append(
                        Node('l' + str(len(nodes_oct)), parent=parent, position=k, value_x=temp_meso_x,
                             value_y=temp_meso_y,
                             value_z=temp_meso_z, low_x=low_x, high_x=meso_x, low_y=low_y, high_y=meso_y, low_z=meso_z,
                             high_z=high_z))
                    build_oct(oct_lists[k], nodes_oct[-1], low_x, meso_x, low_y, meso_y, meso_z, high_z, k, temp_meso_x,
                              temp_meso_y, temp_meso_z)
                elif k == 3:
                    temp_meso_x = (low_x + meso_x) / 2
                    temp_meso_y = (meso_y + high_y) / 2
                    temp_meso_z = (meso_z + high_z) / 2
                    nodes_oct.append(
                        Node('l' + str(len(nodes_oct)), parent=parent, position=k, value_x=temp_meso_x,
                             value_y=temp_meso_y,
                             value_z=temp_meso_z, low_x=low_x, high_x=meso_x, low_y=meso_y, high_y=high_y, low_z=meso_z,
                             high_z=high_z))
                    build_oct(oct_lists[k], nodes_oct[-1], low_x, meso_x, meso_y, high_y, meso_z, high_z, k,
                              temp_meso_x, temp_meso_y, temp_meso_z)
                elif k == 5:
                    temp_meso_x = (meso_x + high_x) / 2
                    temp_meso_y = (low_y + meso_y) / 2
                    temp_meso_z = (meso_z + high_z) / 2
                    nodes_oct.append(
                        Node('l' + str(len(nodes_oct)), parent=parent, position=k, value_x=temp_meso_x,
                             value_y=temp_meso_y,
                             value_z=temp_meso_z, low_x=meso_x, high_x=high_x, low_y=low_y, high_y=meso_y, low_z=meso_z,
                             high_z=high_z))
                    build_oct(oct_lists[k], nodes_oct[-1], meso_x, high_x, low_y, meso_y, meso_z, high_z, k,
                              temp_meso_x, temp_meso_y, temp_meso_z)
                elif k == 7:
                    temp_meso_x = (meso_x + high_x) / 2
                    temp_meso_y = (meso_y + high_y) / 2
                    temp_meso_z = (meso_z + high_z) / 2
                    nodes_oct.append(
                        Node('l' + str(len(nodes_oct)), parent=parent, position=k, value_x=temp_meso_x,
                             value_y=temp_meso_y,
                             value_z=temp_meso_z, low_x=meso_x, high_x=high_x, low_y=meso_y, high_y=high_y,
                             low_z=meso_z,
                             high_z=high_z))
                    build_oct(oct_lists[k], nodes_oct[-1], meso_x, high_x, meso_y, high_y, meso_z, high_z, k,
                              temp_meso_x, temp_meso_y, temp_meso_z)

            elif len(oct_lists[k]) == 1:
                nodes_oct.append(Node('leaf ' + str(oct_lists[k].iloc[0, 0]), parent=parent, position=k,
                                      Airport_ID=oct_lists[k].iloc[0, 0],
                                      Name=oct_lists[k].iloc[0, 1], City=oct_lists[k].iloc[0, 2],
                                      Country=oct_lists[k].iloc[0, 3], IATA=oct_lists[k].iloc[0, 4],
                                      ICAO=oct_lists[k].iloc[0, 5],
                                      Latitude=oct_lists[k].iloc[0, 6], Longitude=oct_lists[k].iloc[0, 7],
                                      Altitude=oct_lists[k].iloc[0, 8],
                                      Timezone=oct_lists[k].iloc[0, 9],
                                      DST=oct_lists[k].iloc[0, 10], Tz_database_time_zone=oct_lists[k].iloc[0, 11],
                                      Type=oct_lists[k].iloc[0, 12],
                                      Source=oct_lists[k].iloc[0, 13]))











