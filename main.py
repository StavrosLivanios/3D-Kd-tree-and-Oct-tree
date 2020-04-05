import pandas as pd
from anytree.exporter import DotExporter
import os
import ast
from build import build_kd, nodes
from search import search
from delete import delete_kd
from insert import insert_kd
from update import update_kd
from anytree.exporter import DictExporter
from anytree.importer import DictImporter

os.environ["PATH"] += os.pathsep + 'C:\Program Files (x86)\Graphviz2.38\\bin\\'
# sys.setrecursionlimit(13000)

max_id = 0
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
    print("8. EXIT")
    choice = input()

    # ===================================================================================================================

    if choice == "1":
        # take the data sheet from the file
        data = pd.read_csv("airports-extended1000.txt", sep=",", header=None)
        data.columns = ["Airport ID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", "Altitude",
                        "Timezone", "DST", "Tz database time zone", "Type", "Source"]

        # preprosesing of data by removing the duplicates
        data.drop_duplicates(subset=("Latitude", "Longitude", "Altitude"), keep='first', inplace=True,
                             ignore_index=True)
        build_kd(data, 6, 0, "root", "root")
        max_id = max(data.iloc[:, 0])

        # create files with the tree created
    #        DotExporter(nodes[0]).to_dotfile("root.dot")
    #        DotExporter(nodes[0]).to_picture("root.png")
    # ===================================================================================================================

    elif choice == "2":

        if len(nodes) == 0:
            print("THERE IS NO DATA")
        else:
            print("GIVE THE POINT YOU WANT TO SEARCH FOR as x,y,z")
            #x = "51.100799560546875,-100.052001953125,999"
            x = input()
            x = x.replace(" ", "")
            x = x.split(",")
            point = [float(x[0]), float(x[1]), float(x[2])]
            axis = point
            res = search(nodes[0], axis)
            if not res:
                print("The point doesn't exist")
            else:
                print(res.Name)
                DotExporter(res.parent.parent).to_picture("search.png")
        print()
    # ===================================================================================================================

    elif choice == "3":
        print("give the x,y,z of the point you want to delete")
        #x = "51.100799560546875,-100.052001953125,999"
        x = input()
        x = x.replace(" ", "")
        x = x.split(",")
        point = [float(x[0]), float(x[1]), float(x[2])]

        # point = [nodes[26].Latitude, nodes[26].Longitude, nodes[26].Altitude]
        # point = [-23.246700286865234,131.9029998779297,620]

        res = del_node = delete_kd(nodes[0], point)
        DotExporter(res.parent.parent).to_picture("delete.png")
    # ===================================================================================================================
    elif choice == "4":
        print("give the data of the insert separating them with  ,  (dont give id)")
        #pin = "Dauphin Barker Airport,Dauphin,Canada,YDN,CYDN,51.100799560546875,-100.052001953125,999,-6,A,America/Winnipeg,airport,OurAirports"
        pin = input()
        pin = pin.replace("\"", "")
        pin = pin.split(",")

        point = [float(pin[5]), float(pin[6]), float(pin[7])]

        # point = [nodes[26].Latitude, nodes[26].Longitude, nodes[26].Altitude]
        # pin = [1111111, "siouta diplomatikh", "patra", "ellda", "gr2", nodes[26].Latitude,  nodes[26].Longitude,  nodes[26].Altitude, 1, -2, "a", "geia", "af", "af", "af"]
        # point = [64.2833023071289, -14.401399612426758, 75]
        # point = [nodes[26].Latitude, nodes[26].Longitude, nodes[26].Altitude]

        res = insert_kd(nodes[0], point, pin, int(max_id))
        print(res.name)
        if not res == False:
            DotExporter(res.parent.parent).to_picture("insert.png")
        print()
    # ===================================================================================================================

    elif choice == "5":

        print("give the x,y,z of the point you want to update")
        x = input()
        x = x.replace(" ", "")
        x = x.split(",")
        point = [float(x[0]), float(x[1]), float(x[2])]

        print("give the data of the update separating them with  ,  with nthename of the datasheet names")
        pin = input()
        # point = [nodes[6].Latitude, nodes[6].Longitude, nodes[6].Altitude]
        # point = [51.444166,7.088929,222]
        # data = "Name = skata , Latitude=2, Longtitude = 2, Altitude = 2"

        res = update_kd(nodes[0], data, point, max_id)

        DotExporter(res.parent.parent).to_picture("update.png")

    # ===================================================================================================================

    elif choice == "6":
        exporter = DictExporter()
        data2 = exporter.export(nodes[0])
        importer = DictImporter()
        f = open("kd_export.txt", "w", encoding="utf-8")
        f.write(str(data2))
        f.close()

    # ===================================================================================================================

    elif choice == "7":

        dict = ast.literal_eval(open("kd_export.txt", encoding="utf-8").read())
        nodes[0] = importer.import_(dict)

    elif choice == "8":

        x = input()
        for i in range(len(nodes)):
            if (nodes[i].name == x):
                ans = nodes[i]
                ind = i
        print()
    # ===================================================================================================================
    else:
        break
