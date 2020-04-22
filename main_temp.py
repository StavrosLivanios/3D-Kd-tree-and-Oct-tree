import os
import pandas as pd
from anytree.exporter import DotExporter

from build import build_oct, nodes_oct
from delete import delete_oct
from search import search_oct
from insert import insert_oct

os.environ["PATH"] += os.pathsep + 'C:\Program Files (x86)\Graphviz2.38\\bin\\'
data = pd.read_csv("airports-extended20.txt", sep=",", header=None)
data.columns = ["Airport ID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", "Altitude",
                "Timezone", "DST", "Tz database time zone", "Type", "Source"]
data.drop_duplicates(subset=("Latitude", "Longitude", "Altitude"), keep='first', inplace=True, ignore_index=True)


build_oct(data, "root", 0, 0, 0)


DotExporter(nodes_oct[0]).to_dotfile("root_oct.dot")
DotExporter(nodes_oct[0]).to_picture("oct_tree.png")


point = [1, 1, 1]
pin = [1111111, "siouta diplomatikh", "patra", "ellda", "gr2", point[0], point[1], point[2], 1, -2, "a", "geia", "af",
       "af", "af"]
insert_oct(nodes_oct[0], point, pin, 1234567)

DotExporter(nodes_oct[0]).to_picture("oct_insert.png")
print()

point2 = [-5.826789855957031, 144.29600524902344, 5388]
delete_oct(nodes_oct[0], point2)
DotExporter(nodes_oct[0]).to_picture("oct_delete.png")