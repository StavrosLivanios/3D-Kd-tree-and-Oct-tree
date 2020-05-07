from search import search, search_oct


def find_max(node, axis_list, axis):
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

# =============================Delete_kd===============================================
# =====================================================================================

def delete_kd(node_root, point):
    node = search(node_root, point)
    if not node:
        return False

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
                    axis_list = []
                    find_max(node_to_delete.siblings[0], axis_list, node_to_delete.parent.axis)
                    node_to_delete.parent.value = max(axis_list)
                    node_to_delete.siblings[0].dir = "left"
                    del node_to_delete.parent._NodeMixin__children[0]
                else:
                    #if len(node_to_delete.parent._NodeMixin__children)==2:
                    del node_to_delete.parent._NodeMixin__children[1]
                node_to_delete = node_to_delete.parent
                node_to_delete_temp = node_to_delete.parent
    else:
        brother = node.siblings[0]
        if node.siblings[0].is_leaf:
            if node.dir == 'left':
                node.parent.children[1].dir = node.parent.dir
                temp_name = node.parent.children[1].name.split()
                if len(temp_name) == 2:
                    node.parent.children[1].name = "leaf_" + node.parent.children[1].dir + " " + temp_name[1]
                if node.parent.dir == 'left':
                    temp_child = node.parent.parent._NodeMixin__children
                    temp_child[0] = node.parent._NodeMixin__children[1]
                    node.parent.parent._NodeMixin__children = []
                    node.parent._NodeMixin__children[1].parent = node.parent.parent
                    node.parent.parent._NodeMixin__children = temp_child

                else:
                    temp_child = node.parent.parent._NodeMixin__children
                    if len(temp_child)==2:
                        temp_child[1] = node.parent._NodeMixin__children[1]
                        node.parent.parent._NodeMixin__children = []
                        node.parent._NodeMixin__children[1].parent = node.parent.parent
                        node.parent.parent._NodeMixin__children = temp_child
                    else:
                        axis_list = []
                        find_max(node.siblings[0], axis_list, node.parent.parent.axis)
                        node.parent.parent.value = max(axis_list)
                        node.siblings[0].dir = "left"
                        #temp_child[0] = node.siblings[0]
                        temp_child = []
                        temp_child.append(node.siblings[0])
                        node.parent.parent._NodeMixin__children = []
                        node.siblings[0].parent = node.parent.parent
                        node.parent.parent._NodeMixin__children = temp_child


            else:
                node.parent.children[0].dir = node.parent.dir
                temp_name = node.parent.children[0].name.split()
                if len(temp_name) == 2:
                    node.parent.children[0].name = "leaf_" + node.parent.children[0].dir + " " + temp_name[1]
                if node.parent.dir == 'left':
                    temp_child = node.parent.parent._NodeMixin__children
                    temp_child[0] = node.parent._NodeMixin__children[0]
                    node.parent.parent._NodeMixin__children = []
                    node.parent._NodeMixin__children[0].parent = node.parent.parent
                    node.parent.parent._NodeMixin__children = temp_child
                else:
                    temp_child = node.parent.parent._NodeMixin__children
                    if len(temp_child)==2:
                        temp_child[1] = node.parent._NodeMixin__children[0]
                        node.parent.parent._NodeMixin__children = []
                        node.parent._NodeMixin__children[0].parent = node.parent.parent
                        node.parent.parent._NodeMixin__children = temp_child
                    else:
                        axis_list = []
                        find_max(node.siblings[0], axis_list, node.parent.parent.axis)
                        node.parent.parent.value = max(axis_list)
                        node.siblings[0].dir = "left"
                        #temp_child[0] = node.siblings[0]
                        temp_child = []
                        temp_child.append(node.siblings[0])
                        node.parent.parent._NodeMixin__children = []
                        node.siblings[0].parent = node.parent.parent
                        node.parent.parent._NodeMixin__children = temp_child


        elif not node.siblings[0].is_leaf and node.siblings[0].dir == "right":
            axis_list = []
            find_max(node.siblings[0], axis_list, node.parent.axis)
            node.parent.value = max(axis_list)
            node.parent._NodeMixin__children[1].dir = "left"
            del node.parent._NodeMixin__children[0]

        elif not node.siblings[0].is_leaf and node.siblings[0].dir == "left":
            del node.parent._NodeMixin__children[1]

        while len(brother.siblings) == 0 and brother.is_leaf == True:
            if brother.parent.dir == 'left':
                brother.dir = brother.parent.dir
                temp_child = brother.parent.parent._NodeMixin__children
                temp_child[0] = brother
                brother.parent.parent._NodeMixin__children = []
                brother = brother.parent.parent
                brother.parent.parent._NodeMixin__children = temp_child
            else:
                brother.dir = brother.parent.dir
                temp_child = brother.parent.parent._NodeMixin__children
                temp_child[1] = brother
                brother.parent.parent._NodeMixin__children = []
                brother.parent = brother.parent.parent
                brother.parent.parent._NodeMixin__children = temp_child

    return node


# =============================Delete_oct==============================================
# =====================================================================================

def delete_oct(node_root, point):
    node = search_oct(node_root, point)
    if not node:
        return False

    if len(node.parent._NodeMixin__children) == 2:

        node.siblings[0].position = node.parent.position

        ind = 0
        for i in node.parent.parent._NodeMixin__children:
            if node.parent.position == i.position:
                node.parent.parent._NodeMixin__children[ind] = node.siblings[0]
            ind = ind + 1

    else:
        ind = 0
        for i in node.parent._NodeMixin__children:
            if node.position == i.position:
                del node.parent._NodeMixin__children[ind]
                return node
            ind = ind + 1

    return node
