import sys


def counting(a, b):
    max = 0
    count = 0
    i = 0
    while (i < (len(b)-len(a)+1)):
        if (b[i:len(a)+i] == a):
            count += 1
            i = len(a)+i-1
        elif (max < count):
            max = count
            count = 0
        else:
            count = 0
        i += 1
    return max


def main():
    if (len(sys.argv) != 3):
        print("Usage: python dna.py data.csv sequence.txt")
        return 1
    if(sys.argv[1].split('.')[1] != "csv" or sys.argv[2].split('.')[1] != "txt"):
        print("Usage: python dna.py data.csv sequence.txt")
        return 1
    csvFile = open(sys.argv[1], "r")
    txtFile = open(sys.argv[2], "r")
    if (not csvFile.mode or not txtFile.mode):
        print("Unable to open files")
        return 1
    csvv = csvFile.read().split("\n")
    csv = list()
    for i in range(len(csvv)):
        csv.append(list(csvv[i].split(",")))

    txt = txtFile.read()
    count = list()
    csvFile.close()
    txtFile.close()
    for i in range(1, len(csv[0])):
        count.append(counting(csv[0][i], txt))
    for i in range(1, len(csv)):
        if(count == list(map(int, csv[i][1:len(csv[0])]))):
            print(csv[i][0])
            return 0
    print("No match")
    return 0


main()