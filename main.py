import ast
import os
import sys

import pandas as pd
from anytree.exporter import DictExporter, DotExporter
from anytree.importer import DictImporter
from timeit import default_timer as timer
# imports for KD and OCT trees
from build import build_kd, nodes, build_oct, nodes_oct
from delete import delete_kd, delete_oct
from find_time import compare_times
from insert import insert_kd, insert_oct
from search import search, search_oct
from update import update_kd, update_oct

sys.setrecursionlimit(20000)
os.environ["PATH"] += os.pathsep + 'C:\Program Files (x86)\Graphviz2.38\\bin\\'

max_id = 0
max_id_oct = 0
tree_choice = 3
#THIS THE CHOISE MENU FOR THE TREE YOU WANT TO USE
#print("THIS IS A MENU")
while tree_choice == 3 :
    print("==================================================")
    print("Choose the data structure by typing one of  the numbers showed below:")
    print("1. OCT-TREE")
    print("2. KD-TREE")
    print("3. Compare times for search and Delete")
    print("==================================================")
    tree_choice = input()
    tree_choice = int(tree_choice)
    if tree_choice == 3:
        compare_times()

#THIS IS THE CHOISE FOR THE SIZE OF THE DATASHEET
print("==================================================")
print("Choose the dataset size by inserting one of the followings: 20 , 100 , 1000 , all ")
print("(all is 12666)")
print("==================================================")
data_size = input()
sheet_name = "airports-extended" + str(data_size) + ".txt"

#PRE-PROCESING OF THE DATA SHEET
data = pd.read_csv(sheet_name, sep=",", header=None)
data.columns = ["Airport ID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", "Altitude",
                "Timezone", "DST", "Tz database time zone", "Type", "Source"]
data.drop_duplicates(subset=("Latitude", "Longitude", "Altitude"), keep='first', inplace=True,
                     ignore_index=True)
max_id = max(data.iloc[:, 0])
max_id_oct = max_id

#CHOICE FOR IMPORT OR BUILD AT THE START
print("==================================================")
print("Choose  one of the following actions  by typing one of  the numbers showed below:")
print("1. build the tree anew ")
print("2. import the tree from a file")
print("==================================================")
choise_2 = int(input())
if choise_2 == 1:
    if tree_choice == 1:
        start = timer()
        build_oct(data, "root", 0, 0, 0, 0, 0, 0, 0 ,0,0,0)
        DotExporter(nodes_oct[0]).to_picture("oct_tree.png")
        end = timer()
    elif tree_choice == 2:
        start = timer()
        build_kd(data, 6, 0, "root", "root")
        DotExporter(nodes[0]).to_picture("kd_tree.png")
        end = timer()
    print("The tree has been built successfully.")
    print(end - start)
elif choise_2 == 2:
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
    print(" The tree has been imported successfully")


while True:

    print("==================================================")
    print("Type the number of the  action you want to execute")
    print("1. Search")
    print("2. Delete")
    print("3. Insert")
    print("4. Update")
    print("5. Export")
    print("6. Import")
    print("7. Exit")
    print("==================================================")
    choice = input()

    if choice == "1":
        print("GIVE THE POINT YOU WANT TO SEARCH FOR as x,y,z")
        x = input()
        x = x.replace(" ", "")
        x = x.split(",")
        point = [float(x[0]), float(x[1]), float(x[2])]
        if tree_choice == 1:
            start = timer()
            res = search_oct(nodes_oct[0], point)
            end = timer()
        elif tree_choice == 2:
            start = timer()
            res = search(nodes[0], point)
            end = timer()
        print(end - start)
        if not res:
            print("The point doesn't exist")
        else:
            print(res)

    # ===================================================================================================================

    elif choice == "2":
        print("Give the x,y,z of the point you want to delete")
        x = input()
        x = x.replace(" ", "")
        x = x.split(",")
        point = [float(x[0]), float(x[1]), float(x[2])]

        if tree_choice == 1:
            start = timer()
            res = delete_oct(nodes_oct[0], point)
            end = timer()
        elif tree_choice == 2:
            start = timer()
            res = delete_kd(nodes[0], point)
            end = timer()
        print(end - start)
        if not res:
            print("The point doesn't exist")

    # ===================================================================================================================
    elif choice == "3":
        print("Give the data of the node you want to insert separated by ',' (don't give id)")
        pin = input()
        pin = pin.replace("\"", "")
        pin = pin.split(",")
        point = [float(pin[5]), float(pin[6]), float(pin[7])]

        if tree_choice == 1:
            start = timer()
            res = insert_oct(nodes_oct[0], point, pin, int(max_id_oct))
            print(res)
            end = timer()
            max_id_oct=int(max_id_oct)+1
        elif tree_choice == 2:
            start = timer()
            res = insert_kd(nodes[0], point, pin, int(max_id))
            end = timer()
            max_id=int(max_id)+1
        print(end - start)
        if not res:
            print("The point already exist")
        #DotExporter(nodes_oct[0]).to_picture("insert.png")

    # ===================================================================================================================

    elif choice == "4":

        print("Give the x,y,z of the point you want to update")
        x = input()
        x = x.replace(" ", "")
        x = x.split(",")
        point = [float(x[0]), float(x[1]), float(x[2])]
        print("Give the new data that are going to be updated  on the node  separated by ','  (E.g NAME = 'Benizelos'_, Longtitude = 34,454353,..._)")
        data_upt = input()

        if tree_choice == 1:
            start = timer()
            res = update_oct(nodes_oct[0], data_upt, point)
            end = timer()
        elif tree_choice == 2:
            start = timer()
            res = update_kd(nodes[0], data_upt, point)
            end = timer()
        print(end - start)
        if not res:
            print("The point doesn't exist")

    # ===================================================================================================================

    elif choice == "5":
        exporter = DictExporter()
        if tree_choice == 1:
            data2 = exporter.export(nodes_oct[0])
            importer = DictImporter()
            f = open("tree_save/oct_export.txt", "w", encoding="utf-8")
        elif tree_choice == 2:
            data2 = exporter.export(nodes[0])
            importer = DictImporter()
            f = open("tree_save/kd_export.txt", "w", encoding="utf-8")
        f.write(str(data2))
        f.close()
        print("A file with the tree has been created")

    # ===================================================================================================================

    elif choice == "6":
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
    elif choice == "9":
        if tree_choice == 1:
            DotExporter(nodes_oct[0]).to_picture("oct_tree_protype.png")
        elif tree_choice == 2:
            DotExporter(nodes[0]).to_picture("kd_tree_prototype.png")
    # ===================================================================================================================
    else:
        break
