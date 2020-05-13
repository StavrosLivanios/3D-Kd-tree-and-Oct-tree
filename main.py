import ast
import os
import sys
import pandas as pd
from anytree.exporter import DictExporter
from anytree.exporter import DotExporter
from anytree.importer import DictImporter
from timeit import default_timer as timer
# imports for KD and OCT trees
from build import build_kd, nodes, build_oct, nodes_oct
from delete import delete_kd, delete_oct
from insert import insert_kd, insert_oct
from search import search, search_oct
from update import update_kd, update_oct

os.environ["PATH"] += os.pathsep + 'C:\Program Files (x86)\Graphviz2.38\\bin\\'
sys.setrecursionlimit(13000)


max_id = 0
max_id_oct = 0

#THIS THE CHOISE MENU FOR THE TREE YOU WANT TO USE
print("THIS IS A MENU")
print("TYPE THE NUMBER OF THE CHOICE YOU WANT TO RUN")
print("1. OCT-TREE")
print("2. KD-TREE")
tree_choice = input()
tree_choice = int(tree_choice)

#THIS IS THE CHOISE FOR THE SIZE OF THE DATASHEET
print("Choose data sheet size (20 , 100 , 1000 , all) (all is 12666)")
print("type on of the choises (20 , 100 , 1000 , all) ")
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
print("Would you like to run build or import ")
print("1. build ")
print("2. import")
choise_2 = int(input())
if choise_2 == 1:
    if tree_choice == 1:
        start = timer()
        build_oct(data, "root", 0, 0, 0)
        end = timer()

    elif tree_choice == 2:
        start = timer()
        build_kd(data, 6, 0, "root", "root")
        end = timer()
    print("BUILD FOR THE SELECTED TREE HAS BEEN CALLED")
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
    print("A file with the tree has been imported")


while True:

    print("THIS IS A MENU")
    print("TYPE THE NUMBER OF THE CHOICE YOU WANT TO RUN")
    print("1. build tree (run this before the others)")
    print("2. search for a point (give x,y,z)")
    print("3. delete by giving the point")
    print("4. INSERT")
    print("5. UPDATE")
    print("6. EXPORT")
    print("7. INPORT")
    print("7. change tree (kd - oct)")
    print("9. EXIT")
    choice = input()

    # ===================================================================================================================

    if choice == "1":
        if tree_choice == 1:
            start = timer()
            build_oct(data, "root", 0, 0, 0)
            end = timer()
        elif tree_choice == 2:
            start = timer()
            build_kd(data, 6, 0, "root", "root")
            end = timer()
        print(end - start)
        #DotExporter(nodes[0]).to_picture("poly_screen/20treekd.png")
    # ===================================================================================================================

    elif choice == "2":
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
            DotExporter(res.parent.parent).to_picture("tree_png/search.png")

    # ===================================================================================================================

    elif choice == "3":
        print("give the x,y,z of the point you want to delete")
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
        elif tree_choice == 2:
            DotExporter(res.parent.parent).to_picture("tree_png/delete.png")
    # ===================================================================================================================
    elif choice == "4":
        print("give the data of the insert separating them with  ,  (dont give id)")
        pin = input()
        pin = pin.replace("\"", "")
        pin = pin.split(",")
        point = [float(pin[5]), float(pin[6]), float(pin[7])]

        if tree_choice == 1:
            start = timer()
            res = insert_oct(nodes_oct[0], point, pin, int(max_id_oct))
            end = timer()
        elif tree_choice == 2:
            start = timer()
            res = insert_kd(nodes[0], point, pin, int(max_id))
            end = timer()
        print(end - start)
        if not res:
            print("The point already exist")
        elif tree_choice == 2:
            DotExporter(res.parent.parent).to_picture("tree_png/insert.png")
    # ===================================================================================================================

    elif choice == "5":

        print("give the x,y,z of the point you want to update")
        x = input()
        x = x.replace(" ", "")
        x = x.split(",")
        point = [float(x[0]), float(x[1]), float(x[2])]
        print("give the data of the update separating them with  ,  (NAME = NEW_ , VALUE = NEW_)")
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
            print("The point DOENT EXIST exist")
        elif tree_choice == 2:
            DotExporter(res.parent.parent).to_picture("tree_png/update.png")
    # ===================================================================================================================

    elif choice == "6":
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

    elif choice == "7":
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
    # ===================================================================================================================
    elif choice == "8":
        if tree_choice == 1:
            tree_choice == 2
            if len(nodes_oct) == 0:
                build_oct(data, "root", 0, 0, 0)
                print("Tree changed to oct and build has been called")
            else:
                print("Tree changed to oct")
        elif tree_choice == 2:
            tree_choice == 1
            if len(nodes) == 0:
                build_oct(data, "root", 0, 0, 0)
                print("Tree changed to kd and build has been called")
            else:
                print("Tree changed to kd")
    # ===================================================================================================================
    else:
        break
