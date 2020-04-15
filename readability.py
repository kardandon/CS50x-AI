string = input("Text: ")
W = 0
L = 0
S = 0
for i in range(len(string)):
    if (string[i].isalpha()):
        L += 1
    elif (string[i].ispace()):
        W += 1
        while(string[i].ispace()):
            i += 1
        i -= 1
    elif (string[i] == '!' or string[i] == '?' or string[i] == '.'):
        S += 1
W += 1
z = round(0.0588 * L / W * 100 - 0.296 * S / W * 100 - 15.8)
if (z > 16):
    print("Grade 16+")
elif (z < 1):
    print("Before Grade 1")
else:
    print("Grade" + str(z))