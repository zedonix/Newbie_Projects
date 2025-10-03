def first():
    with open("input") as fin:
        data = fin.readlines()
        nice = 0
        for i in data:
            vowels = 0
            prev = i[0]
            twice = False
            exclude = False
            for j in i:
                if j in "aeiou":
                    vowels += 1
                if prev == j and not twice:
                    twice = True
                prev = j
            if "ab" in i or "cd" in i or "pq" in i or "xy" in i:
                exclude = True
            if not exclude:
                if vowels > 2 and twice:
                    nice += 1
        print(nice)


first()
