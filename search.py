import pandas as pd
import numpy as np
from anytree import Node, RenderTree


def search(nodes, point):
    if nodes.is_leaf:
        if float(nodes.Latitude) - float(point[0]) < 10**-6 and float(nodes.Longitude) - float(point[1])< 10**-6 and float(nodes.Altitude) - float(point[2])< 10**-6:
            res = nodes
        else:
            res = False
    else:
        axis = nodes.depth % 3
        if round(float(nodes.value), 4) >= round(float(point[axis]), 4):
            if len(nodes.children) == 0:
                return False
            child = nodes.children[0]
        elif round(float(nodes.value), 4) < round(float(point[axis]), 4):
            if len(nodes.children) == 1:
                return False
            child = nodes.children[1]

        res = search(child, point)

    return res


def search_oct(nodes, point):
    if nodes.is_leaf:
        if float(nodes.Latitude) - float(point[0]) < 10**-6 and float(nodes.Longitude) - float(point[1])< 10**-6 and float(nodes.Altitude) - float(point[2])< 10**-6:
            res = nodes
        else:
            res = False
    else:

        if nodes.value_x >= float(point[0]) and nodes.value_y >= float(point[1]) and nodes.value_z >= float(point[2]):
            position = 0
        elif nodes.value_x >= float(point[0]) and nodes.value_y >= float(point[1]) and nodes.value_z < float(point[2]):
            position = 1
        elif nodes.value_x >= float(point[0]) and nodes.value_y < float(point[1]) and nodes.value_z >= float(point[2]):
            position = 2
        elif nodes.value_x >= float(point[0]) and nodes.value_y < float(point[1]) and nodes.value_z < float(point[2]):
            position = 3
        elif nodes.value_x < float(point[0]) and nodes.value_y >= float(point[1]) and nodes.value_z >= float(point[2]):
            position = 4
        elif nodes.value_x < float(point[0]) and nodes.value_y >= float(point[1]) and nodes.value_z < float(point[2]):
            position = 5
        elif nodes.value_x < float(point[0]) and nodes.value_y < float(point[1]) and nodes.value_z >= float(point[2]):
            position = 6
        elif nodes.value_x < float(point[0]) and nodes.value_y < float(point[1]) and nodes.value_z < float(point[2]):
            position = 7

        if len(nodes.children) == 0:
            return False
        else:
            child = False
            for i in nodes.children:
                if i.position == position:
                    child = i

        if child != False:
            res = search_oct(child, point)
        else:
            res = False

    return res
