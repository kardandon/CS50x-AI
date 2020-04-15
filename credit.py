def digitsum(n):
    a = 0
    while n:
        a += n % 10
        n //= 10
    return a

n = input("Number: ")
i = False
sum = 0
for j in reversed(n):
    sum += digitsum(2**i * int(j))
    i = i == 0
if (sum % 10 != 0):
    print("INVALID\n")
elif ((n[0:2] == "34" or n[0:2] == "37") and len(n) == 15):
    print("AMEX\n")
elif ((n[0:2] == "51" or n[0:2] == "52" or n[0:1] == "53" or n[0:1] == "54" or n[0:1] == "55") and len(n) == 16):
    print("MASTERCARD\n")
elif ((n[0] == "4") and (len(n) == 13 or len(n) == 16)):
    print("VISA\n")
else:
    print("INVALID\n")