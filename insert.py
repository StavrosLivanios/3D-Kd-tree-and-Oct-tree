from build import nodes, nodes_oct
from anytree import Node


# This funchions creates a leaf
def insert_leaf(name, ins_data, dir, parent, max_id, type_of_tree):
    if type_of_tree=="kd":
        res = Node(name, parent=parent, dir=dir, Airport_ID=max_id,
                   Name=ins_data[0], City=ins_data[1], Country=ins_data[2],
                   IATA=ins_data[3],
                   ICAO=ins_data[4],
                   Latitude=ins_data[5], Longitude=ins_data[6], Altitude=ins_data[7],
                   Timezone=ins_data[8],
                   DST=ins_data[9], Tz_database_time_zone=ins_data[10], Type=ins_data[11],
                   Source=ins_data[12])
    elif type_of_tree=="oct":
        res = Node(name, parent=parent, position=dir, Airport_ID=max_id,
                   Name=ins_data[0], City=ins_data[1], Country=ins_data[2],
                   IATA=ins_data[3],
                   ICAO=ins_data[4],
                   Latitude=ins_data[5], Longitude=ins_data[6], Altitude=ins_data[7],
                   Timezone=ins_data[8],
                   DST=ins_data[9], Tz_database_time_zone=ins_data[10], Type=ins_data[11],
                   Source=ins_data[12])
    return res


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


def insert_kd(node_root, point, ins_data, max_id):
    max_id = max_id + 1
    # insert is like search at the core so we search for the position to insert
    # if we find a leaf then either the point already exists or we have to vreate a new node and put both under it
    print(node_root)
    if node_root.is_leaf:
        # Checking if point already exist in tree
        if round(float(node_root.Latitude), 4) == round(float(point[0]), 4) and\
                round(float(node_root.Longitude), 4) == round(float(point[1]), 4)\
                and round(float(node_root.Altitude), 4) == round(float(point[2]), 4):
            print("The x,y,z axis you inputed is already in the tree")
            return False
        else:
            sibling_point = [node_root.Latitude, node_root.Longitude, node_root.Altitude]
            axis = node_root.parent.axis
            if axis == 6:
                axis = 1
                p_axis = 7
            elif axis == 7:
                axis = 2
                p_axis = 8
            else:
                axis = 0
                p_axis = 6

            if node_root.dir == "left":
                node_dir = 0
            else:
                node_dir = 1
            # Creating new node to be the father of the node we want to insert and the node that was here before
            # and making the previous node that was here his child
            new_node = Node('l' + str(len(nodes)), axis=p_axis, value=point[axis], dir=node_root.dir)
            nodes.append(new_node)
            old_parent = node_root.parent
            temp_childs = old_parent._NodeMixin__children
            node_root.parent = new_node
            new_node.parent = old_parent
            temp_childs[node_dir] = new_node
            old_parent._NodeMixin__children = temp_childs

            # This if is just so the names are correct(leaf_left - leaf_righ)
            # and have the right variables in the node
            if round(float(sibling_point[axis])) >= round(point[axis]):
                node_root.dir = "right"
                node_root.name = "leaf_" + node_root.dir + " " + node_root.name.split()[1]
                nodes.append(insert_leaf('leaf_Left ' + str(max_id), ins_data, "left", node_root.parent, max_id,"kd"))
                temp = new_node._NodeMixin__children[1]
                new_node._NodeMixin__children[1] = new_node._NodeMixin__children[0]
                new_node._NodeMixin__children[0] = temp

            elif round(float(sibling_point[axis])) < round(point[axis]):
                node_root.dir = "left"
                node_root.name = "leaf_" + node_root.dir + " " + node_root.name.split()[1]
                nodes.append(insert_leaf('leaf_right ' + str(max_id), ins_data, "right", node_root.parent, max_id,"kd"))

            res = new_node

    else:
        print("hello")
        axis = node_root.depth % 3

        # We search for the postition toi put the node we want to inser
        # if the value of the x,y,or z is greater than then we go to the right side of the tree
        if round(float(node_root.value), 4) >= round(float(point[axis]), 4):
            # If there is nothing on this side and we want to isnert a node we just create a new node here
            if len(node_root.children) == 0:
                new_leaf = insert_leaf('leaf_Left ' + str(max_id), ins_data, "left", node_root, max_id,"kd")
                nodes.append(new_leaf)
                node_root._NodeMixin__children[0] = new_leaf
                return node_root._NodeMixin__children[0]
            child = node_root.children[0]

        elif round(float(node_root.value), 4) < round(float(point[axis]), 4):
            if len(node_root.children) == 1:
                new_leaf = insert_leaf('leaf_right ' + str(max_id), ins_data, "right", node_root, max_id, "kd")
                nodes.append(new_leaf)
                node_root._NodeMixin__children[1] = new_leaf
                return node_root._NodeMixin__children[1]
            child = node_root.children[1]

        res = insert_kd(child, point, ins_data, max_id)

    return res


def insert_oct(node_root, point, ins_data, max_id):
    max_id = max_id + 1
    if node_root.is_leaf:

        # Checking if node with this cordinates already exists
        if round(float(node_root.Latitude), 4) == round(float(point[0]), 4) \
                and round(float(node_root.Longitude),4) == round(float(point[1]), 4) \
                and round(float(node_root.Altitude), 4) == round(float(point[2]), 4):
            print("The x,y,z axis you inputed is already in the tree")
            return False

        # If there is another node in the position we weant to put the node we make a new node and
        # and make the node we will create and the node taht was here its childrens
        else:

            meso_x = (point[0] + float(node_root.Latitude)) / 2
            meso_y = (point[1] + float(node_root.Longitude)) / 2
            meso_z = (point[2] + float(node_root.Altitude)) / 2

            new_node = Node('l' + str(len(nodes_oct)), parent=node_root.parent, position=node_root.position,
                            value_x=meso_x, value_y=meso_y, value_z=meso_z)
            nodes_oct.append(new_node)

            node_root.parent = new_node

            pos = find_position(point, [meso_x, meso_y, meso_z])
            new_child = insert_leaf('leaf ' + str(max_id), ins_data, pos, new_node, max_id, "oct")

            nodes_oct.append(new_child)
            node_root._NodeMixin__children.sort(key=lambda x: x.position)
            new_node._NodeMixin__children.sort(key=lambda x: x.position)
            res = new_node

    # If the position we want to put the new node is empty we just create it
    else:
        position = find_position(point, [node_root.value_x, node_root.value_y, node_root.value_z])

        child = False
        for i in node_root.children:
            if i.position == position:
                child = i

        if child != False:
            res = insert_oct(child, point, ins_data, max_id)
        else:
            nodes_oct.append(insert_leaf('leaf ' + str(max_id), ins_data, position, node_root, max_id, "oct"))
            res = nodes_oct[-1]
            node_root._NodeMixin__children.sort(key=lambda x: x.position)

    return res
