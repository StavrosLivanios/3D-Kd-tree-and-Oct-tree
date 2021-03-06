from build import nodes, nodes_oct
from anytree import Node
from copy import copy

# This funchions creates a leaf
def insert_leaf(name, ins_data, dir, parent, max_id, type_of_tree):
    if type_of_tree == "kd":
        print("hello")
        res = Node(name, parent=parent, dir=dir, Airport_ID=max_id,
                   Name=ins_data[0], City=ins_data[1], Country=ins_data[2],
                   IATA=ins_data[3],
                   ICAO=ins_data[4],
                   Latitude=ins_data[5], Longitude=ins_data[6], Altitude=ins_data[7],
                   Timezone=ins_data[8],
                   DST=ins_data[9], Tz_database_time_zone=ins_data[10], Type=ins_data[11],
                   Source=ins_data[12])
        # this does the same for oct
    elif type_of_tree == "oct":
        res = Node(name, parent=parent, position=dir, Airport_ID=max_id,
                   Name=ins_data[0], City=ins_data[1], Country=ins_data[2],
                   IATA=ins_data[3],
                   ICAO=ins_data[4],
                   Latitude=ins_data[5], Longitude=ins_data[6], Altitude=ins_data[7],
                   Timezone=ins_data[8],
                   DST=ins_data[9], Tz_database_time_zone=ins_data[10], Type=ins_data[11],
                   Source=ins_data[12])
    return res

#this function finds the exact position of each list in the tree
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

#==========================================KD=================================================================
#=============================================================================================================

def insert_kd(node_root, point, ins_data, max_id):
    max_id = max_id + 1
    # insert is like search at the core so we search for the position to insert
    # if we find a leaf then either the point already exists or we have to create a new node and put both under it
    if node_root.is_leaf:
        # Checking if point already exist in tree
        if round(float(node_root.Latitude), 4) == round(float(point[0]), 4) and \
                round(float(node_root.Longitude), 4) == round(float(point[1]), 4) \
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

            # This if is just so the names are correct(leaf_left - leaf_right)
            # and have the right variables in the node
            if round(float(sibling_point[axis]), 4) >= round(point[axis], 4):
                node_root.dir = "right"
                node_root.name = "leaf_" + node_root.dir + " " + node_root.name.split()[1]
                nodes.append(insert_leaf('leaf_Left ' + str(max_id), ins_data, "left", node_root.parent, max_id, "kd"))
                temp = new_node._NodeMixin__children[1]
                new_node._NodeMixin__children[1] = new_node._NodeMixin__children[0]
                new_node._NodeMixin__children[0] = temp

            elif round(float(sibling_point[axis]), 4) < round(point[axis], 4):
                node_root.dir = "left"
                node_root.name = "leaf_" + node_root.dir + " " + node_root.name.split()[1]
                nodes.append(insert_leaf('leaf_right ' + str(max_id), ins_data, "right", node_root.parent, max_id, "kd"))
                if new_node.axis == 6:
                    new_node.value = node_root.Latitude
                elif new_node.axis == 7:
                    new_node.value = node_root.Longitude
                else:
                    new_node.value = node_root.Altitude

            res = new_node

    else:
        axis = node_root.depth % 3

        # We search for the postition toi put the node we want to insert
        # if the value of the x,y,or z is greater then we go to the right side of the tree
        if round(float(node_root.value), 4) >= round(float(point[axis]), 4):
            # If there is nothing on this side and we want to isnert a node we just create a new node here
            if len(node_root.children) == 0:
                new_leaf = insert_leaf('leaf_Left ' + str(max_id), ins_data, "left", node_root, max_id, "kd")
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

#==========================================OCT================================================================
#=============================================================================================================

def insert_oct(node_root, point, ins_data, max_id):
    max_id = max_id + 1
    position = find_position(point, [node_root.value_x, node_root.value_y, node_root.value_z])

    child = False
    # When visiting a node we search for nodes or leafs with the position that the leaf we want to insert should have(according to x,y,z values of the node we are visiting)
    # if the postion maches a node we follow and visit it. If its a leaf we check if it already exists.
    for i in node_root.children:
        if i.position == position:
            if not i.is_leaf:
                child = i
            else:
                if round(float(i.Latitude), 4) == round(float(point[0]), 4) and round(float(i.Longitude), 4) == round(float(point[1]), 4) and int(i.Altitude) == int(point[2]):
                    return False

    if child != False:
        res = insert_oct(child, point, ins_data, max_id)
        return res
    else:
    # If the node we want to insert the new leaf has 8 children then we must separete again the cube in 8 subspaces
        if len(node_root.children) >= 8:
            ins_node = insert_leaf('leaf ' + str(max_id), ins_data, position, node_root, max_id, "oct")
            nodes_oct.append(ins_node)
            res = ins_node

            split_leafs(node_root)
    # If the children are 7 or less we just add the new leaf
        else:
            nodes_oct.append(insert_leaf('leaf ' + str(max_id), ins_data, position, node_root, max_id, "oct"))
            res = nodes_oct[-1]
            node_root._NodeMixin__children.sort(key=lambda x: x.position)

    return res

#===================================================================================================================================

# We use this function to create a new leaf
def create_leaf_insert(node_root,i,temp_meso_x,temp_meso_y,temp_meso_z):
    nodes_oct.append(
        Node('l' + str(len(nodes_oct)), parent=node_root, position=i, value_x=temp_meso_x,
             value_y=temp_meso_y,
             value_z=temp_meso_z, low_x=node_root.low_x, high_x=node_root.value_x,
             low_y=node_root.low_y, high_y=node_root.value_y,
             low_z=node_root.low_z,
             high_z=node_root.value_z))


# In this function we separate the 8 children of a node we want to add a new leaf 
# so that every child with the same postion will go under a new node representing 
# a subspace of the original cube we want to separate
def split_leafs(node_root):
    num_per_pos = [0, 0, 0, 0, 0, 0, 0, 0]
    # we count how many childs from every position we have (more than one means it needs to create a new node for that subaspace)
    for i in node_root.children:
        num_per_pos[i.position] = num_per_pos[i.position] + 1

    temp_childs = node_root._NodeMixin__children

    for i in range(8):
        if num_per_pos[i] > 1:
            if i == 0:
                temp_meso_x = (node_root.low_x + node_root.value_x) / 2
                temp_meso_y = (node_root.low_y + node_root.value_y) / 2
                temp_meso_z = (node_root.low_z + node_root.value_z) / 2
                create_leaf_insert(node_root, i, temp_meso_x, temp_meso_y, temp_meso_z)
                temp_parent = nodes_oct[-1]

            elif i == 2:
                temp_meso_x = (node_root.low_x + node_root.value_x) / 2
                temp_meso_y = (node_root.value_y + node_root.high_y) / 2
                temp_meso_z = (node_root.low_z + node_root.value_z) / 2
                create_leaf_insert(node_root, i, temp_meso_x, temp_meso_y, temp_meso_z)
                temp_parent = nodes_oct[-1]

            elif i == 4:
                temp_meso_x = (node_root.value_x + node_root.high_x) / 2
                temp_meso_y = (node_root.low_y + node_root.value_y) / 2
                temp_meso_z = (node_root.low_z + node_root.value_z) / 2
                create_leaf_insert(node_root,i,temp_meso_x,temp_meso_y,temp_meso_z)
                temp_parent = nodes_oct[-1]

            elif i == 6:
                temp_meso_x = (node_root.value_x + node_root.high_x) / 2
                temp_meso_y = (node_root.value_y + node_root.high_y) / 2
                temp_meso_z = (node_root.low_z + node_root.value_z) / 2
                create_leaf_insert(node_root, i, temp_meso_x, temp_meso_y, temp_meso_z)
                temp_parent = nodes_oct[-1]
            elif i == 1:
                temp_meso_x = (node_root.low_x + node_root.value_x) / 2
                temp_meso_y = (node_root.low_y + node_root.value_y) / 2
                temp_meso_z = (node_root.value_z + node_root.high_z) / 2
                create_leaf_insert(node_root,i,temp_meso_x,temp_meso_y,temp_meso_z)
                temp_parent = nodes_oct[-1]
            elif i == 3:
                temp_meso_x = (node_root.low_x + node_root.value_x) / 2
                temp_meso_y = (node_root.value_y + node_root.high_y) / 2
                temp_meso_z = (node_root.value_z + node_root.high_z) / 2
                create_leaf_insert(node_root, i, temp_meso_x, temp_meso_y, temp_meso_z)
                temp_parent = nodes_oct[-1]
            elif i == 5:
                temp_meso_x = (node_root.value_x + node_root.high_x) / 2
                temp_meso_y = (node_root.low_y + node_root.value_y) / 2
                temp_meso_z = (node_root.value_z + node_root.high_z) / 2
                create_leaf_insert(node_root, i, temp_meso_x, temp_meso_y, temp_meso_z)
                temp_parent = nodes_oct[-1]

            elif i == 7:
                temp_meso_x = (node_root.value_x + node_root.high_x) / 2
                temp_meso_y = (node_root.value_y + node_root.high_y) / 2
                temp_meso_z = (node_root.value_z + node_root.high_z) / 2
                create_leaf_insert(node_root, i, temp_meso_x, temp_meso_y, temp_meso_z)
                temp_parent = nodes_oct[-1]

            temp_childs_cp = copy(temp_childs)
            for j in temp_childs:
                if j.position == i:
                    if j.is_leaf == True:
                        j.position = find_position([j.Latitude, j.Longitude, j.Altitude],
                                                   [temp_parent.value_x, temp_parent.value_y, temp_parent.value_z])
                        j.parent = temp_parent
                        temp_childs_cp.remove(j)
            temp_childs = temp_childs_cp
            
            # If after the separation of the childs they are still more than 8 under a new node that means we need to 
            # keep dividing the subspace untill it fits the oct-tree critiria
            while len(temp_parent.children)>8:
                split_leafs(temp_parent)