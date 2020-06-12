from search import search, search_oct

def find_max(node, axis_list, axis):
    # create node for each axis
    if node.is_leaf:
        if axis == 6:
            axis_list.append(node.Latitude)
        elif axis == 7:
            axis_list.append(node.Longitude)
        elif axis == 8:
            axis_list.append(node.Altitude)
    else:

        if len(node.children) == 1:
            find_max(node.children[0], axis_list, axis)
        elif len(node.children) == 2:
            find_max(node.children[0], axis_list, axis)
            find_max(node.children[1], axis_list, axis)

def delete_me_and_make_my_brother_the_father(node, direction):
    # find direction of node

    if direction == "left":
        temp_direction = 1
    elif direction == "right":
        temp_direction = 0
    # change position of a children node depending on its direction and whether it's parent has a brother node or not

    node.parent.children[temp_direction].dir = node.parent.dir
    temp_name = node.parent.children[temp_direction].name.split()
    if len(temp_name) == 2:
        node.parent.children[temp_direction].name = "leaf_" + node.parent.children[temp_direction].dir + " " + temp_name[1]
    if node.parent.dir == 'left':
        temp_child = node.parent.parent._NodeMixin__children
        temp_child[0] = node.parent._NodeMixin__children[temp_direction]
        node.parent.parent._NodeMixin__children = []
        node.parent._NodeMixin__children[temp_direction].parent = node.parent.parent
        node.parent.parent._NodeMixin__children = temp_child

    else:
        temp_child = node.parent.parent._NodeMixin__children
        if len(temp_child) == 2:
            temp_child[1] = node.parent._NodeMixin__children[temp_direction]
            node.parent.parent._NodeMixin__children = []
            node.parent._NodeMixin__children[temp_direction].parent = node.parent.parent
            node.parent.parent._NodeMixin__children = temp_child
        else:
            axis_list = []
            find_max(node.siblings[0], axis_list, node.parent.parent.axis)
            node.parent.parent.value = max(axis_list)
            node.siblings[0].dir = "left"
            # temp_child[0] = node.siblings[0]
            temp_child = []
            temp_child.append(node.siblings[0])
            node.parent.parent._NodeMixin__children = []
            node.siblings[0].parent = node.parent.parent
            node.parent.parent._NodeMixin__children = temp_child

def delete_left_and_transfer_the_right_subtree_to_the_left_side(node):
    axis_list = []
    find_max(node.siblings[0], axis_list, node.parent.axis)
    node.parent.value = max(axis_list)
    node.parent._NodeMixin__children[1].dir = "left"
    del node.parent._NodeMixin__children[0]


def delete_kd(node_root, point):

    node = search(node_root, point)
    if not node:
        return False
    # check if node have a brother and make his brother a parent node after nodes' deletion
    if len(node.siblings) == 0:
        node_to_delete = node.parent
        node.parent._NodeMixin__children = []
        while len(node_to_delete.children) == 0:
            if len(node_to_delete.siblings) == 0:
                node_to_delete_temp = node_to_delete
                node_to_delete = node_to_delete.parent
                node_to_delete_temp.parent._NodeMixin__children = []
            else:
                if node_to_delete.dir == "left":
                    delete_left_and_transfer_the_right_subtree_to_the_left_side(node_to_delete)
                else:
                    #if len(node_to_delete.parent._NodeMixin__children)==2:
                    del node_to_delete.parent._NodeMixin__children[1]
                node_to_delete = node_to_delete.parent
                node_to_delete_temp = node_to_delete.parent
    else:
        brother = node.siblings[0]
        if node.siblings[0].is_leaf:
            if node.dir == 'left':
                delete_me_and_make_my_brother_the_father(node, "left")
            else:
                delete_me_and_make_my_brother_the_father(node, "right")


        elif not node.siblings[0].is_leaf and node.siblings[0].dir == "right":
            delete_left_and_transfer_the_right_subtree_to_the_left_side(node)

        elif not node.siblings[0].is_leaf and node.siblings[0].dir == "left":
            del node.parent._NodeMixin__children[1]

    return node



def delete_oct(node_root, point):
    node = search_oct(node_root, point)
    if not node:
        return False
    # make the brother node a parent node after the node's deletion
    if len(node.parent._NodeMixin__children) == 2:

        node.siblings[0].position = node.parent.position
        ind = 0
        for i in node.parent.parent._NodeMixin__children:
            if node.parent.position == i.position:
                # node.parent.parent._NodeMixin__children[ind] = node.siblings[0]
                temp_child = node.parent.parent._NodeMixin__children
                temp_child[ind] = node.siblings[0]
                node.parent.parent._NodeMixin__children = []
                node.siblings[0].parent = node.parent.parent
                node.parent.parent._NodeMixin__children = temp_child
            ind = ind + 1
    elif len(node.parent._NodeMixin__children) == 1:
        node = node.parent
        while (node.parent._NodeMixin__children) == 1:
            node = node.parent
        for p in node.parent._NodeMixin__children:
            if node.name == p.name:
                del p


    else:
        ind = 0
        for i in node.parent._NodeMixin__children:
            if node.position == i.position:
                if i.is_leaf == True:
                    x = i.Latitude
                    y = i.Longitude
                    z = i.Altitude
                else:
                    x = i.value_x
                    y = i.value_y
                    z = i.value_z
                if round(float(x), 4) == round(float(point[0]), 4) and round(float(y), 4) == round(float(point[1]),4) and int(z) == int(point[2]):
                    del node.parent._NodeMixin__children[ind]
                    return node
            ind = ind + 1

    return node

