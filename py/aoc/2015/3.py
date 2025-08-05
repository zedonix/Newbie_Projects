def first():
    with open("input") as fin:
        data = fin.read()
        locations = set()
        x = y = 0
        locations.add((x, y))
        for i in data:
            if i == "^":
                y += 1
            elif i == ">":
                x += 1
            elif i == "<":
                x -= 1
            elif i == "v":
                y -= 1
            locations.add((x, y))
        total = len(locations)
        print(total)

def second():
    with open("input") as fin:
        data = fin.read()
        santa = {(0,0)}
        robo = set()
        x1 = y1 = 0
        x2 = y2 = 0
        alternate = True
        for i in data:
            if alternate:
                if i == "^":
                    y1 += 1
                elif i == ">":
                    x1 += 1
                elif i == "<":
                    x1 -= 1
                elif i == "v":
                    y1 -= 1
                santa.add((x1, y1))
                alternate = False
            else:
                if i == "^":
                    y2 += 1
                elif i == ">":
                    x2 += 1
                elif i == "<":
                    x2 -= 1
                elif i == "v":
                    y2 -= 1
                santa.add((x2, y2))
                alternate = True
        locations = santa | robo
        total = len(locations)
        print(total)

first()
second()
