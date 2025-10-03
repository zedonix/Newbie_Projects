import hashlib


def first(input):
    end = 0
    temp = input + str(end)
    md5 = hashlib.md5(temp.encode("utf-8")).hexdigest()
    while md5[0:5] != "00000":
        end += 1
        temp = input + str(end)
        md5 = hashlib.md5(temp.encode("utf-8")).hexdigest()
        print(md5, end)
    print(temp)


def second(input):
    end = 0
    temp = input + str(end)
    md5 = hashlib.md5(temp.encode("utf-8")).hexdigest()
    while md5[0:6] != "000000":
        end += 1
        temp = input + str(end)
        md5 = hashlib.md5(temp.encode("utf-8")).hexdigest()
        print(md5, end)
    print(temp)


first("iwrupvqb")
second("iwrupvqb")
