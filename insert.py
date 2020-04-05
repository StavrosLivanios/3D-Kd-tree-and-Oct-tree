from build import nodes
from anytree import Node


def insert_kd(node_root, point, ins_data, max_id):
    max_id = max_id + 1
    if node_root.is_leaf:
        if float(node_root.Latitude) - float(point[0]) < 10 ** -6 and float(node_root.Longitude) - float(
                point[1]) < 10 ** -6 and float(node_root.Altitude) - float(point[2]) < 10 ** -6:
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

            if round(float(sibling_point[axis])) >= round(point[axis]):
                new_node = Node('l' + str(len(nodes)), axis=p_axis, value=point[axis], dir=node_root.dir)
                nodes.append(new_node)
                old_parent = node_root.parent
                temp_childs = old_parent._NodeMixin__children
                node_root.parent = new_node
                new_node.parent = old_parent
                temp_childs[node_dir] = new_node
                old_parent._NodeMixin__children = temp_childs

                node_root.dir = "right"
                node_root.name = "leaf_" + node_root.dir + " " + node_root.name.split()[1]
                nodes.append(
                    Node('leaf_Left ' + str(max_id), parent=node_root.parent, dir="left", Airport_ID=max_id,
                         Name=ins_data[0], City=ins_data[1], Country=ins_data[2],
                         IATA=ins_data[3],
                         ICAO=ins_data[4],
                         Latitude=ins_data[5], Longitude=ins_data[6], Altitude=ins_data[7],
                         Timezone=ins_data[8],
                         DST=ins_data[9], Tz_database_time_zone=ins_data[10], Type=ins_data[11],
                         Source=ins_data[12]))

                temp = new_node._NodeMixin__children[1]
                new_node._NodeMixin__children[1] = new_node._NodeMixin__children[0]
                new_node._NodeMixin__children[0] = temp
                print()
            elif round(float(sibling_point[axis])) < round(point[axis]):

                new_node = Node('l' + str(len(nodes)), axis=p_axis, value=sibling_point[axis], dir=node_root.dir)
                nodes.append(new_node)
                old_parent = node_root.parent
                temp_childs = old_parent._NodeMixin__children
                node_root.parent = new_node
                new_node.parent = old_parent
                temp_childs[node_dir] = new_node
                old_parent._NodeMixin__children = temp_childs

                node_root.dir = "left"
                node_root.name = "leaf_" + node_root.dir + " " + node_root.name.split()[1]

                nodes.append(
                    Node('leaf_right ' + str(max_id), parent=node_root.parent, dir="right", Airport_ID=max_id,
                         Name=ins_data[0], City=ins_data[1], Country=ins_data[2],
                         IATA=ins_data[3],
                         ICAO=ins_data[4],
                         Latitude=ins_data[5], Longitude=ins_data[6], Altitude=ins_data[7],
                         Timezone=ins_data[8],
                         DST=ins_data[9], Tz_database_time_zone=ins_data[10], Type=ins_data[11],
                         Source=ins_data[12]))
                print()
            res = new_node
    else:
        axis = node_root.depth % 3
        if round(float(node_root.value), 4) >= round(float(point[axis]), 4):
            if len(node_root.children) == 0:
                node_root._NodeMixin__children[0] = nodes.append(
                    Node('leaf_Left ' + str(max_id), parent=node_root, dir="left", Airport_ID=max_id,
                         Name=ins_data[0], City=ins_data[1], Country=ins_data[2],
                         IATA=ins_data[3],
                         ICAO=ins_data[4],
                         Latitude=ins_data[5], Longitude=ins_data[6], Altitude=ins_data[7],
                         Timezone=ins_data[8],
                         DST=ins_data[9], Tz_database_time_zone=ins_data[10], Type=ins_data[11],
                         Source=ins_data[12]))
                return node_root._NodeMixin__children[0]
            child = node_root.children[0]
        elif round(float(node_root.value), 4) < round(float(point[axis]), 4):
            if len(node_root.children) == 1:
                node_root._NodeMixin__children[1] = nodes.append(
                    Node('leaf_Right ' + str(max_id), parent=node_root, dir="right", Airport_ID=max_id,
                         Name=ins_data[0], City=ins_data[1], Country=ins_data[2],
                         IATA=ins_data[3],
                         ICAO=ins_data[4],
                         Latitude=ins_data[5], Longitude=ins_data[6], Altitude=ins_data[7],
                         Timezone=ins_data[8],
                         DST=ins_data[9], Tz_database_time_zone=ins_data[10], Type=ins_data[11],
                         Source=ins_data[12]))
                return node_root._NodeMixin__children[1]
            child = node_root.children[1]

        res = insert_kd(child, point, ins_data, max_id)

    return res
