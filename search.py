import pandas as pd
import numpy as np
from anytree import Node, RenderTree

def search_kn(nodes, point):
    if nodes.is_leaf:
        if float(nodes.Latitude) - float(point[0]) < 10**-6 and float(nodes.Longitude) - float(point[1])< 10**-6 and float(nodes.Altitude) - float(point[2])< 10**-6:
            res = nodes
        else:
            res = False
    else:
        axis = nodes.depth % 3
        if float(nodes.value) >= float(point[axis]):
            if len(nodes.children) == 0:
                return False
            child = nodes.children[0]
        elif float(nodes.value) < float(point[axis]):
            if len(nodes.children) == 1:
                return False
            child = nodes.children[1]

        res = search_kn(child, point)

    return res
