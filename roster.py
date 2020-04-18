# TODO
from cs50 import *
import sys,csv


if len(sys.argv) != 2:
    print("error")
    sys.exit()

db = SQL("sqlite:///students.db")

lib = db.execute("SELECT first,middle,last,birth FROM students WHERE house = ? ORDER BY last,first,middle", sys.argv[1])

for row in lib:
    name = " "
    if (row["middle"] == "\\N"):
        name = row["first"] + name + row["last"]
    else:
        name = row["first"] + name + row["middle"] + name + row["last"]
    print(name + ", born",row["birth"])