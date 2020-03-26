from anytree.exporter import DotExporter
from search import search_kn
from anytree import Node, RenderTree


def delete(nodes, point):
    node = search_kn(nodes, point)

    if node.siblings:
        if node.dir == 'left':
            node.parent.children[1].dir = node.parent.dir
            if node.parent.dir == 'left':
                x=node.parent.chidren[1]
                node.parent.parent.children[0] = x
            else:
                node.parent.parent.children[1] = node.parent.chidren[1]
            #parent = parent.children[1]
            #parent.children[1] = None
        else:
            node.parent.children[0].dir = node.parent.dir
            if node.parent.dir == 'left':
                node.parent.parent.children[0] = node.parent.chidren[1]
            else:
                node.parent.parent.children[1] = node.parent.chidren[1]
    del node

    # create files with the tree created
    DotExporter(nodes[0]).to_dotfile("root2.dot")
    DotExporter(nodes[0]).to_picture("root2.png")
