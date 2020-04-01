from search import search_kn
from delete import delete_kn
from insert import insert_kn

def update_kn(node_root, data, point, max_id):

    data = data.replace(" ", "").split(",")
    for i in range(len(data)):
        data[i]=data[i].split("=")

    node = search_kn(node_root, point)
    if node == False:
        return False
    temp_point = point.copy()
    change = 0
    for i in range(len(data)):
        atribute = data[i][0]
        value = data[i][1]
        if atribute == "Latitude":
            change = 1
            temp_point[0] = int(value)
        elif atribute == "Longitude":
            change = 1
            temp_point[1] = int(value)
        elif atribute == "Altitude":
            change = 1
            temp_point[2] = int(value)
        else:
            strr = "node." + atribute + " = " + "\"" + value + "\""
            exec(strr)

    if change == 1:
        temp = node
        delete_kn(node_root, point)
        res = insert_kn(node_root, temp_point, [temp.Airport_ID , temp.Name , temp.City, temp.Country, temp.IATA, temp.ICAO, temp_point[0] , temp_point[1], temp_point[2],
                                     temp.Timezone, temp.DST, temp.Tz_database_time_zone, temp.Type, temp.Source], max_id)
        return res

    return node







