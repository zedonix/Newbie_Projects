def first():
    with open("input") as fin:
        data = fin.readlines()
        total = 0
        for i in data:
            vowel = 0
            double = i[0]
            for j in i:
                if double == j:
                    double = True
                if j in "aeiou":
                    vowel += 1
            if vowel >= 3:
                vowel = True
