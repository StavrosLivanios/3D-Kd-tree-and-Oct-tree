from insert import find_position

def search(nodes, point):
    if nodes.is_leaf:
        if round(float(nodes.Latitude), 4) == round(float(point[0]), 4) and round(float(nodes.Longitude), 4) == round(float(point[1]), 4) and round(float(nodes.Altitude), 4) == round(float(point[2]), 4):
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
        if round(float(nodes.Latitude), 4) == round(float(point[0]), 4) and round(float(nodes.Longitude), 4) == round(float(point[1]), 4) and round(float(nodes.Altitude), 4) == round(float(point[2]), 4):
            res = nodes
        else:
            res = False
    else:
        position = find_position(point, [nodes.value_x, nodes.value_y, nodes.value_z])

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
