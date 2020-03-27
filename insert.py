
def insert_kn(nodes, point):
    if nodes.is_leaf:
        if float(nodes.Latitude) - float(point[0]) < 10**-6 and float(nodes.Longitude) - float(point[1])< 10**-6 and float(nodes.Altitude) - float(point[2])< 10**-6:
            # aporich logo idiou x kai y kai z
            res = nodes
        else:
            # prosuesh kombou kai 2 =fuloon
            res = False
    else:
        axis = nodes.depth % 3
        if float(nodes.value) >= float(point[axis]):
            if len(nodes.children) == 0:
                # prosuesh leaf apo to insert
                return
            child = nodes.children[0]
        elif float(nodes.value) < float(point[axis]):
            if len(nodes.children) == 1:
                #prosuesh leaf apo to insert
                return
            child = nodes.children[1]

        res = insert_kn(child, point)

    return  res
