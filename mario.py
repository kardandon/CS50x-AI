def main():
        try:
            n = int(input("Height: "))
        except:
            main()
            return 0
        if (n > 8 or n < 1):
            main()
            return 0
        for i in range(n):
            string = ""
            for j in range(n - i - 1):
                string += " "
            for j in range(i + 1):
                string += "#"
            string += "  "
            for j in range(i + 1):
                string += "#"
            print(string)

if (__name__ == "__main__"):
    main()