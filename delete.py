from anytree.exporter import DotExporter
from search import search
from build import nodes
from anytree import Node, RenderTree


def delete_kd(node_root, point):
    node = search(node_root, point)

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
                print()
            else:
                temp_child = node.parent.parent._NodeMixin__children
                temp_child[1] = node.parent._NodeMixin__children[1]
                node.parent.parent._NodeMixin__children = []
                node.parent._NodeMixin__children[1].parent = node.parent.parent
                node.parent.parent._NodeMixin__children = temp_child

                print()

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
                temp_child[1] = node.parent._NodeMixin__children[0]
                node.parent.parent._NodeMixin__children = []
                node.parent._NodeMixin__children[0].parent = node.parent.parent
                node.parent.parent._NodeMixin__children = temp_child

    elif not node.siblings[0].is_leaf:
        axis_list = []
        find_max(node.siblings[0], axis_list, node.parent.axis)
        node.parent.value = max(axis_list)
        node.parent._NodeMixin__children[1].dir = "left"
        del node.parent._NodeMixin__children[0]

    elif not node.siblings[0].is_leaf:
        del node.parent._NodeMixin__children[1]

    #del node
    return node

def find_max(node,axis_list,axis):
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
