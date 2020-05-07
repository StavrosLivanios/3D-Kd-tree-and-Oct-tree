from search import search, search_oct
from delete import delete_kd, delete_oct
from insert import insert_kd, insert_oct


def update_kd(node_root, data, point):
    data = data.replace(" ", "").split(",")
    for i in range(len(data)):
        data[i] = data[i].split("=")

    node = search(node_root, point)
    if node == False:
        return False
    temp_point = point.copy()
    change = 0
    for i in range(len(data)):
        atribute = data[i][0]
        value = data[i][1]
        if atribute == "Latitude":
            change = 1
            temp_point[0] = float(value)
        elif atribute == "Longitude":
            change = 1
            temp_point[1] = float(value)
        elif atribute == "Altitude":
            change = 1
            temp_point[2] = float(value)
        else:
            #print(atribute + "=" + value)
            strr = "node." + atribute + " = " + "\"" + value + "\""
            exec(strr)

    if change == 1:
        temp = node
        delete_kd(node_root, point)
        res = insert_kd(node_root, temp_point,
                        [temp.Name, temp.City, temp.Country, temp.IATA, temp.ICAO, temp_point[0], temp_point[1],
                         temp_point[2], temp.Timezone, temp.DST, temp.Tz_database_time_zone, temp.Type, temp.Source]
                        , temp.Airport_ID)
        return res

    return node


def update_oct(node_root, data, point):
    data = data.replace(" ", "").split(",")
    for i in range(len(data)):
        data[i] = data[i].split("=")

    node = search_oct(node_root, point)
    if node == False:
        return False
    temp_point = point.copy()
    change = 0
    for i in range(len(data)):
        atribute = data[i][0]
        value = data[i][1]
        if atribute == "Latitude":
            change = 1
            temp_point[0] = float(value)
        elif atribute == "Longitude":
            change = 1
            temp_point[1] = float(value)
        elif atribute == "Altitude":
            change = 1
            temp_point[2] = float(value)
        else:
            #print(atribute + "=" + value)
            strr = "node." + atribute + " = " + "\"" + value + "\""
            exec(strr)

    if change == 1:
        temp = node
        delete_oct(node_root, point)
        res = insert_oct(node_root, temp_point,
                         [temp.Name, temp.City, temp.Country, temp.IATA, temp.ICAO, temp_point[0], temp_point[1],
                          temp_point[2], temp.Timezone, temp.DST, temp.Tz_database_time_zone, temp.Type, temp.Source]
                         , int(temp.Airport_ID) - 1)
        if res.is_root == False :
            res.parent._NodeMixin__children.sort(key=lambda x: x.position)
        return res

    return node
