import ast
import pandas as pd
from anytree.importer import DictImporter
from timeit import default_timer as timer
from delete import delete_oct, delete_kd
from insert import insert_oct, insert_kd
from search import search, search_oct
from update import update_oct, update_kd


def compare_times():
    max_id = 0
    max_id_oct = 0

    # PRE-PROCESING OF THE DATA SHEET
    data = pd.read_csv("airports-extendedall.txt", sep=",", header=None)
    data.columns = ["Airport ID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", "Altitude",
                    "Timezone", "DST", "Tz database time zone", "Type", "Source"]
    data.drop_duplicates(subset=("Latitude", "Longitude", "Altitude"), keep='first', inplace=True,
                         ignore_index=True)

    max_id = max(data.iloc[:, 0])
    max_id_oct = max_id
    importer = DictImporter()

    dict = ast.literal_eval(open("tree_save/oct_export.txt", encoding="utf-8").read())
    nodes_oct = []
    nodes2 = []
    nodes2 = importer.import_(dict)
    nodes_oct.append(nodes2)

    dict = ast.literal_eval(open("tree_save/kd_export.txt", encoding="utf-8").read())
    nodes = []
    nodes2 = []
    nodes2 = importer.import_(dict)
    nodes.append(nodes2)

    pinx = data.iloc[:, 6]
    piny = data.iloc[:, 7]
    pinz = data.iloc[:, 8]

    #===============================================
    print("For the kd tree measured in seconds")

    time_table = []
    for i in range(len(pinx)):
        point = [pinx[i], piny[i], pinz[i]]
        start = timer()
        search(nodes[0], point)
        end = timer()

        time_table.append(end - start)

    sum_time = sum(time_table)
    time = sum_time / len(pinx)
    print("Search : " + str(time) + " | max - " + str(max(time_table)) + " | min - " + str(min(time_table)))

    #===============================================

    # ===============================================
    # =================OCT=====================
    #===============================================
    print("-------------------------")
    print("For the oct tree measured in seconds")
    time_table = []
    for i in range(len(pinx)):
        point = [pinx[i], piny[i], pinz[i]]
        start = timer()
        search_oct(nodes_oct[0], point)
        end = timer()

        time_table.append(end - start)

    sum_time = sum(time_table)
    time = sum_time / len(pinx)
    print("Search : " + str(time) + " | max - " + str(max(time_table)) + " | min - " + str(min(time_table)))




'''

    time_table = []
    for i in range(len(pinx)):
        point = [pinx[i], piny[i], pinz[i]]
        start = timer()
        delete_oct(nodes_oct[0], point)
        end = timer()

        time_table.append(end - start)

    sum_time = sum(time_table)
    time = sum_time / len(pinx)
    print("oct - Delete : " + str(time) + " | max - " + str(max(time_table)) + " | min - " + str(min(time_table)))

    time_table = []
    for i in range(978):
        print(i)
        point = [pinx[i], piny[i], pinz[i]]
        start = timer()
        delete_kd(nodes[0], point)
        end = timer()

        time_table.append(end - start)

    sum_time = sum(time_table)
    time = sum_time / 978
    print("kd - Delete : " + str(time) + " | max - " + str(max(time_table)) + " | min - " + str(min(time_table)))



    time_table = []
    for i in range(366):
        point = [pinx[i]+10, piny[i]+10, pinz[i]+20]
        pin = "Wewak International Airport\",\"Wewak\",\"Papua New Guinea\",\"WWK\",\"AYWK\", " + str(point[0]) +","+ str(point[1]) +","+ str(point[2]) + ",10,\"U\",\"Pacific/Port_Moresby\",\"airport\",\"OurAirports"
        pin = pin.replace("\"", "")
        pin = pin.split(",")
        start = timer()
        insert_oct(nodes_oct[0], point, pin, int(max_id_oct))
        end = timer()

        time_table.append(end - start)

    sum_time = sum(time_table)
    time = sum_time / 366
    print("oct - insert : " + str(time) + " | max - " + str(max(time_table)) + " | min - " + str(min(time_table)))

    time_table = []
    for i in range(len(pinx)):
        point = [pinx[i], piny[i], pinz[i]]
        data_upt="Country=hello"
        start = timer()
        update_oct(nodes_oct[0], data_upt, point)
        end = timer()

        time_table.append(end - start)

    sum_time = sum(time_table)
    time = sum_time / len(pinx)
    print("oct - update : " + str(time) + " | max - " + str(max(time_table)) + " | min - " + str(min(time_table)))

    time_table = []
    for i in range(len(pinx)):
        point = [pinx[i], piny[i], pinz[i]]
        point = [pinx[i] + 10, piny[i] + 10, pinz[i] + 20]

        pin = "Wewak International Airport\",\"Wewak\",\"Papua New Guinea\",\"WWK\",\"AYWK\", " + str(point[0]) +","+ str(point[1]) +","+ str(point[2]) + ",10,\"U\",\"Pacific/Port_Moresby\",\"airport\",\"OurAirports"

        pin = pin.replace("\"", "")
        pin = pin.split(",")
        start = timer()
        insert_kd(nodes[0], point, pin, int(max_id))
        end = timer()

        time_table.append(end - start)

    sum_time = sum(time_table)
    time = sum_time / len(pinx)
    print("KD - insert : " + str(time) + " | max - " + str(max(time_table)) + " | min - " + str(min(time_table)))

    time_table = []
    for i in range(len(pinx)):
        point = [pinx[i], piny[i], pinz[i]]
        data_upt = "Country=hello"
        start = timer()
        update_kd(nodes[0], data_upt, point)
        end = timer()

        time_table.append(end - start)

    sum_time = sum(time_table)
    time = sum_time / len(pinx)
    print("kd - update : " + str(time) + " | max - " + str(max(time_table)) + " | min - " + str(min(time_table)))
'''