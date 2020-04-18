# TODO
from cs50 import *
import sys,csv


if len(sys.argv) != 2:
    print("error")
    sys.exit()

db = SQL("sqlite:///students.db")

with open(sys.argv[1],'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        name = row["name"].split(" ")
        if (len(name)!= 3):
            name.append(name[1])
            name[1] = "\\N"
        house = row["house"]
        birth = row["birth"]
        db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)", name[0], name[1], name[2], house, birth)



