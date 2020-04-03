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
            child = nodes.children[0]
        elif round(float(nodes.value), 4) < round(float(point[axis]), 4):
            child = nodes.children[1]

        res = search(child, point)

    return res

