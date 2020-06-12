import ast
import pandas as pd
from anytree.importer import DictImporter
from timeit import default_timer as timer
from search import search, search_oct

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
