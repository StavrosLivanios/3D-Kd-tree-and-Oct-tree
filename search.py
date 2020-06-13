from insert import find_position

 # Recursive function that is visiting nodes and compares the x,y or z value 
 # to decide if is going to move to the left or the right subtree. After it reaches a leaf 
 # it compares the values and retruns the node or false if the leaf was not the same.
def search(nodes, point):
    # find the point given by searching for each axis
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

# Check recurcively on the nodes you visit if their is a node with the same 
# position that the node you are searching for should have in this node.
# Follow it if its a node or check the value if it is a leaf.
def search_oct(nodes, point):
    # find the point given by searching for each axis

    position = find_position(point, [nodes.value_x, nodes.value_y, nodes.value_z])
    for i in nodes._NodeMixin__children:
        if i.position == position:
            if i.is_leaf:
                if round(float(i.Latitude), 4) == round(float(point[0]), 4) and round(float(i.Longitude), 4) == round(float(point[1]), 4) and int(i.Altitude) == int(point[2]):
                    return i
            else:
                res = search_oct(i, point)
                return res

    return False