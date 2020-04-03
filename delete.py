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
                node.parent.parent._NodeMixin__children[0] = node.parent._NodeMixin__children[1]
            else:
                node.parent.parent._NodeMixin__children[1] = node.parent._NodeMixin__children[1]

        else:
            node.parent.children[0].dir = node.parent.dir
            temp_name = node.parent.children[0].name.split()
            if len(temp_name) == 2:
                node.parent.children[0].name = "leaf_" + node.parent.children[0].dir + " " + temp_name[1]
            if node.parent.dir == 'left':
                node.parent.parent._NodeMixin__children[0] = node.parent._NodeMixin__children[0]
            else:
                node.parent.parent._NodeMixin__children[1] = node.parent._NodeMixin__children[0]

    elif not node.siblings[0].is_leaf:
        del node.parent._NodeMixin__children[1]

    #del node
    return node
