import pandas as pd
from anytree.exporter import DotExporter
import os
from build import build_kn, nodes
from search import search_kn
from delete import delete

os.environ["PATH"] += os.pathsep + 'C:\Program Files (x86)\Graphviz2.38\\bin\\'
# sys.setrecursionlimit(13000)


while True:
    print("THIS IS A MENU")
    print("TYPE THE NUMBER OF THE CHOICE YOU WANT TO RUN")
    print("1. build tree (run this before the others)")
    print("2. search for a point (give x,y,z)")
    print("3. delete by giving the point")
    print("4. EXIT")
    choice = input()

    # ===================================================================================================================

    if choice == "1":
        # take the data sheet from the file
        data = pd.read_csv("airports-extended20.txt", sep=",", header=None)
        data.columns = ["Airport ID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", "Altitude",
                        "Timezone", "DST", "Tz database time zone", "Type", "Source"]
        # preprosesing of data by removing the duplicates
        data.drop_duplicates(subset=("Latitude", "Longitude", "Altitude"), keep='first', inplace=True,
                             ignore_index=True)
        build_kn(data, 6, 0, "root", "root")
        # create files with the tree created
        DotExporter(nodes[0]).to_dotfile("root.dot")

        DotExporter(nodes[0]).to_picture("root.png")

    # ===================================================================================================================

    elif choice == "2":

        if len(nodes) == 0:
            print("THERE IS NO DATA")
        else:
            print("GIVE THE POINT YOU WANT TO SEARCH FOR")
            x = input()
            y = input()
            z = input()
            axis = [x, y, z]
            res = search_kn(nodes[0], axis)
            if not res:
                print("The point doesn't exist")
            else:
                print(res.Name)
    # ===================================================================================================================

    elif choice == "3":
        #x = input()
        #y = input()
        #z = input()
        #point = [x, y, z]
        point = [nodes[6].Latitude, nodes[6].Longitude, nodes[6].Altitude]
        del_node = delete(nodes[0], point)
        DotExporter(nodes[0]).to_dotfile("delroot.dot")
        DotExporter(nodes[0]).to_picture("delroot.png")

    else:
        break


'''
from graphviz import Source
Source.from_file('root.dot')
from graphviz import render
render('dot', 'png', 'root.dot')
'''
