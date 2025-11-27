def first():
    with open("input") as fin:
        data = fin.read()
        positive = data.count("(")
        negative = data.count(")")
        total = positive - negative
        print(total)


def second():
    with open("input") as fin:
        data = fin.read()
        basement = False
        total = 0
        for i in range(len(data)):
            if data[i] == "(":
                total += 1
            elif data[i] == ")":
                total -= 1
            if total == -1:
                basement = True
            if basement:
                print(i)
                print(total)
                break


first()
second()
