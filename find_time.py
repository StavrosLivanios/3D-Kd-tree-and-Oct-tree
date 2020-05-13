import ast
import pandas as pd
from anytree.exporter import DotExporter
from anytree.importer import DictImporter
from timeit import default_timer as timer
from build import build_kd, nodes, build_oct, nodes_oct
from delete import delete_oct, delete_kd
from insert import insert_kd, insert_oct
from search import search, search_oct
from update import update_kd, update_oct

max_id = 0
max_id_oct = 0


#PRE-PROCESING OF THE DATA SHEET
data = pd.read_csv("airports-extendedall.txt", sep=",", header=None)
data.columns = ["Airport ID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", "Altitude",
                "Timezone", "DST", "Tz database time zone", "Type", "Source"]
data.drop_duplicates(subset=("Latitude", "Longitude", "Altitude"), keep='first', inplace=True,
                     ignore_index=True)

tree_choice = 2

importer = DictImporter()
if tree_choice == 1:
        dict = ast.literal_eval(open("tree_save/oct_export.txt", encoding="utf-8").read())
        nodes_oct = []
        nodes2 = []
        nodes2 = importer.import_(dict)
        nodes_oct.append(nodes2)
elif tree_choice == 2:
        dict = ast.literal_eval(open("tree_save/kd_export.txt", encoding="utf-8").read())
        nodes = []
        nodes2 = []
        nodes2 = importer.import_(dict)
        nodes.append(nodes2)
print("A file with the tree has been imported")
max_id = max(data.iloc[:, 0])
max_id_oct = max_id
pinx = data.iloc[:, 6]
piny = data.iloc[:, 7]
pinz = data.iloc[:, 8]
counter = 0
time_table = []
for i in range(len(pinx)):
    print(i)
    point = [pinx[i]+1000, piny[i]+1090, pinz[i]+30]

    pin = [1111111, "siouta diplomatikh", "patra", "ellda", "gr2", point[0], point[1], point[2], 1, -2, "a", "geia",
           "af",
           "af", "af"]

    start = timer()
    insert_kd(nodes[0], point, pin, int(max_id))
    end = timer()

    time_table.append(end - start)
sum_time = sum(time_table)
time = sum_time / len(pinx)
print(time)
'''
search(nodes[0], point)
search_oct(nodes_oct[0], point)

delete_oct(nodes_oct[0], point)
del_node = delete_kd(nodes[0], point)

point = [1, 1, 1]
pin = [1111111, "siouta diplomatikh", "patra", "ellda", "gr2", point[0], point[1], point[2], 1, -2, "a", "geia", "af",
       "af", "af"]
insert_oct(nodes_oct[0], point, pin, int(max_id_oct))
insert_kd(nodes[0], point, pin, int(max_id))

point3 = [76.5311965942,-68.7032012939,251]
data2 = "Name = skata, Latitude = 1 "
update_oct(nodes_oct[0], data_upt, point)
update_kd(nodes[0], data_upt, point)
'''
