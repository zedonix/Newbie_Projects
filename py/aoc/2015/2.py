def first():
    with open("input") as fin:
        data = fin.readlines()
        total = 0
        for i in data:
            values = list(map(int, i.split("x")))
            total += (
                2 * values[0] * values[1]
                + 2 * values[1] * values[2]
                + 2 * values[2] * values[0]
            )
            least1 = min(values)
            values.remove(least1)
            least2 = min(values)
            values.remove(least2)
            total += least1 * least2
        print(total)


def second():
    with open("input") as fin:
        data = fin.readlines()
        total = 0
        for i in data:
            values = list(map(int, i.split("x")))
            volume = values[0] * values[1] * values[2]
            least1 = min(values)
            values.remove(least1)
            least2 = min(values)
            values.remove(least2)
            wrapping = 2 * (least1 + least2)
            total += wrapping + volume
        print(total)


second()
