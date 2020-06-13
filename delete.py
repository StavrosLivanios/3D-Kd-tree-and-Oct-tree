from search import search, search_oct

# We use the function findmax in the case that we want to change the dir of a subtree from right to left after we delete a node in order to correct the structure of the tree.
# Recursive function that gathers all the values(x,y,z) of the subtree. 
# The name find_max is used because after the function we find the max value of the list of values that is returned
def find_max(node, axis_list, axis): # For kd only
    #check if the node is actually a leaf in order to procced 
    if node.is_leaf:
        if axis == 6: # 6 ==> axis x
            axis_list.append(node.Latitude)
        elif axis == 7: # 7 ==> axis y
            axis_list.append(node.Longitude)
        elif axis == 8: # 8 ==> axis z
            axis_list.append(node.Altitude)
    else:

        if len(node.children) == 1:
            find_max(node.children[0], axis_list, axis)
        elif len(node.children) == 2:
            find_max(node.children[0], axis_list, axis)
            find_max(node.children[1], axis_list, axis)

# Explicit case of delete, we used big names in order the code is easier to read.
def delete_me_and_make_my_brother_the_father(node, direction):# For kd only
    # find direction of node(brother of deleted node)
    if direction == "left":
        temp_direction = 1
    elif direction == "right":
        temp_direction = 0
    # change position of a children node depending on its direction and whether it's parent has a brother node or not

    node.parent.children[temp_direction].dir = node.parent.dir
    temp_name = node.parent.children[temp_direction].name.split()
    if len(temp_name) == 2:
        node.parent.children[temp_direction].name = "leaf_" + node.parent.children[temp_direction].dir + " " + temp_name[1] # we preserve the new name of the node(brother) that will change direction
    if node.parent.dir == 'left':
        temp_child = node.parent.parent._NodeMixin__children # access the list of grandparent's children 
        temp_child[0] = node.parent._NodeMixin__children[temp_direction]  
        node.parent.parent._NodeMixin__children = [] # empty  the  children's list  on the grandparent of the node(brother)
        node.parent._NodeMixin__children[temp_direction].parent = node.parent.parent #change the parent of the node(brother) to his grandparent 
        node.parent.parent._NodeMixin__children = temp_child # save the updated list

    else:
        temp_child = node.parent.parent._NodeMixin__children # access the list of grandparent's children 
        if len(temp_child) == 2:
            temp_child[1] = node.parent._NodeMixin__children[temp_direction]
            node.parent.parent._NodeMixin__children = []
            node.parent._NodeMixin__children[temp_direction].parent = node.parent.parent #change the parent of the node(brother) to his grandparent
            node.parent.parent._NodeMixin__children = temp_child  # save the updated list
        
        else:
            axis_list = []
            find_max(node.siblings[0], axis_list, node.parent.parent.axis) #gathers all the values(x,y,z) of the correspoding branch
            node.parent.parent.value = max(axis_list) # save the max from axis_list 
            node.siblings[0].dir = "left"
            temp_child = []
            temp_child.append(node.siblings[0]) # add the node that is going to be the new child
            node.parent.parent._NodeMixin__children = []
            node.siblings[0].parent = node.parent.parent
            node.parent.parent._NodeMixin__children = temp_child

def delete_left_and_transfer_the_right_subtree_to_the_left_side(node): # For kd only
    axis_list = []
    find_max(node.siblings[0], axis_list, node.parent.axis)
    node.parent.value = max(axis_list)
    node.parent._NodeMixin__children[1].dir = "left" # change the direction of the node from right to left  
    del node.parent._NodeMixin__children[0]


def delete_kd(node_root, point):

    node = search(node_root, point)
    if not node:
        return False
    # check if node have a brother and make his brother a parent node after node's deletion
    if len(node.siblings) == 0:
        node_to_delete = node.parent  # The parent of the deleted node doesn't have children anymore so it is neccesery to be deleted as well
        node.parent._NodeMixin__children = []
        while len(node_to_delete.children) == 0: # We are correcting the structure of the tree using a while loop untill we reach a node that has children  
            if len(node_to_delete.siblings) == 0: # if the node doesn't have sublings then we have to delete his parent too
                node_to_delete_temp = node_to_delete
                node_to_delete = node_to_delete.parent 
                node_to_delete_temp.parent._NodeMixin__children = []
            else:
                if node_to_delete.dir == "left":
                    delete_left_and_transfer_the_right_subtree_to_the_left_side(node_to_delete)  
                else:
                    del node_to_delete.parent._NodeMixin__children[1] # The structure of the tree don't have to change 
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
    # If there are two points in a subspace make the brother node a parent node after the node's deletion
    if len(node.parent._NodeMixin__children) == 2:

        node.siblings[0].position = node.parent.position
        ind = 0 # counter used for indexing the childrens of the grandparent
        for i in node.parent.parent._NodeMixin__children:
            if node.parent.position == i.position: # The parent of the deleted node isn't a leaf so he will not have the same position his siblings
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


    else: # If you have more than 2 children we just delete the selected node 
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

