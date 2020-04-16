import sys
import pandas as pd


def main():
    if (len(sys.argv) != 3 ):
        print("Usage: python dna.py data.csv sequence.txt")
        return 1
    if(sys.argv[1].split('.')[1] != "csv" or sys.argv[2].split('.')[1] != "txt"):
        print("Usage: python dna.py data.csv sequence.txt")
        return 1
    csvFile = open(sys.argv[1],"r")
    txtFile = open(sys.argv[2],"r")
    if (not csvFile.mode or not txtFile.mode):
        print("Unable to open files")
        return 1
    csvv = csvFile.read().split("\n")
    print(csvv)
    csv = list()
    for i in range(len(csvv)):
        csv.append(list(csvv[i].split(",")))

    txt = txtFile.read()
    count = list()
    csvFile.close()
    txtFile.close()
    for i in range(1,len(csv[0])):
        count.append(txt.count(csv[0][i]))
    for i in range(1, len(csv)):
        if(count == list(map(int,csv[i][1:len(csv[0])]))):
            print(csv[i][0])
            return 0
    print("No match")
    return 0


main()