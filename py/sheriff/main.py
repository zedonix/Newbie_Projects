import random
import mysql.connector as ms
import pickle

con = ms.connect(host="localhost", user="root", passwd="tiger")
cur = con.cursor()

map = [[0, 0, 0], [0, "#", 0], [0, 0, 0]]

left = ("#", 0, 0)
right = (0, 0, "#")
middle = (0, "#", 0)
zero = (0, 0, 0)

been = 0
beenBar = False
continueGame = False

nothing = []

columns = 1
length = 3

username = ""
kill = 0
hp = 10
money = 200
gun = 0
beer = 0


def showMap():
    counter = 0
    for i in range(len(map)):
        counter += 1
        for j in map[i]:
            print(j, end=" ")
        if counter == columns:
            counter = 0
            print()


def movement(way):
    x = y = z = 0
    for i in range(len(map)):
        x = i
        for j in range(len(map[i])):
            if map[i][j] == "#":
                y = j
                z = 1
                break
        if z == 1:
            break

    if way == "e":
        east(x, y)
    elif way == "w":
        west(x, y)
    elif way == "n":
        north(x, y)
    elif way == "s":
        south(x, y)


def east(x, y):
    global nothing, map, columns, length, been, beenBar

    if y == 0 or y == 1:
        if map[x][y + 1] == 1:
            been = 1
        elif map[x][y + 1] == "$":
            been = 2
        else:
            been = 0
        map[x][y + 1] = "#"
        if beenBar:
            map[x][y] = "$"
            beenBar = False
        else:
            map[x][y] = 1
    else:
        go = False
        for i in range(1, length + 1):
            if columns * i == x + 1:
                go = True
                break
        if go:
            been = 0
            counter = index = 0
            for i in range(len(map) + length):
                if counter == columns:
                    if map[index - 1][2] == "#":
                        nothing.insert(i, list(left))
                    else:
                        nothing.insert(i, list(zero))
                    counter = 0
                else:
                    counter += 1
                    if map[index][2] == "#":
                        if beenBar:
                            nothing.insert(i, [map[x][0], map[x][1], "$"])
                            beenBar = False
                        else:
                            nothing.insert(i, [map[x][0], map[x][1], 1])
                        index += 1
                    else:
                        nothing.insert(i, map[index])
                        index += 1
            columns += 1
            map = nothing
            nothing = []
        else:
            if map[x + 1][0] == 1:
                been = 1
            elif map[x + 1][0] == "$":
                been = 2
            else:
                been = 0
            map[x + 1][0] = "#"
            if beenBar:
                map[x][y] = "$"
                beenBar = False
            else:
                map[x][y] = 1


def west(x, y):
    global nothing, map, columns, length, been, beenBar

    if y == 2 or y == 1:
        if map[x][y - 1] == 1:
            been = 1
        elif map[x][y - 1] == "$":
            been = 2
        else:
            been = 0
        map[x][y - 1] = "#"
        if beenBar:
            map[x][y] = "$"
            beenBar = False
        else:
            map[x][y] = 1
    else:
        go = False
        for i in range(1, length + 1):
            if columns * i == x + columns:
                go = True
                break
        if go:
            been = 0
            index = 0
            counter = columns
            for i in range(len(map) + length):
                if counter == columns:
                    if index != len(map) and map[index][0] == "#":
                        nothing.insert(i, list(right))
                    else:
                        nothing.insert(i, list(zero))
                    counter = 0
                else:
                    counter += 1
                    if map[index][0] == "#":
                        if beenBar:
                            nothing.insert(i, ["$", map[x][1], map[x][2]])
                            beenBar = False
                        else:
                            nothing.insert(i, [1, map[x][1], map[x][2]])
                        index += 1
                    else:
                        nothing.insert(i, map[index])
                        index += 1
            columns += 1
            map = nothing
            nothing = []
        else:
            if map[x - 1][2] == 1:
                been = 1
            elif map[x - 1][2] == "$":
                been = 2
            else:
                been = 0
            map[x - 1][2] = "#"
            if beenBar:
                map[x][y] = "$"
                beenBar = False
            else:
                map[x][y] = 1


def north(x, y):
    global nothing, map, columns, length, been, beenBar

    if x in range(columns):
        been = 0
        for i in range(columns):
            if i == x:
                nothing.insert(
                    i,
                    [
                        "#" if y == 0 else 0,
                        "#" if y == 1 else 0,
                        "#" if y == 2 else 0,
                    ],
                )
                if beenBar:
                    map[x][y] = "$"
                    beenBar = False
                else:
                    map[x][y] = 1
            else:
                nothing.insert(i, list(zero))
        for i in range(len(nothing)):
            map.insert(i, nothing[i])
        nothing = []
        length += 1
    else:
        if map[x - columns][y] == 1:
            been = 1
        elif map[x - columns][y] == "$":
            been = 2
        else:
            been = 0
        map[x - columns][y] = "#"
        if beenBar:
            map[x][y] = "$"
            beenBar = False
        else:
            map[x][y] = 1


def south(x, y):
    global nothing, map, columns, length, been, beenBar

    if x in range(len(map) - 1, len(map) - columns - 1, -1):
        been = 0
        for i in range(columns):
            if i + len(map) - columns == x:
                nothing.insert(
                    i,
                    [
                        "#" if y == 0 else 0,
                        "#" if y == 1 else 0,
                        "#" if y == 2 else 0,
                    ],
                )
                if beenBar:
                    map[x][y] = "$"
                    beenBar = False
                else:
                    map[x][y] = 1
            else:
                nothing.insert(len(map) - 1, list(zero))
        map.extend(nothing)
        nothing = []
        length += 1
    else:
        if map[x + columns][y] == 1:
            been = 1
        elif map[x + columns][y] == "$":
            been = 2
        else:
            been = 0
        map[x + columns][y] = "#"
        if beenBar:
            map[x][y] = "$"
            beenBar = False
        else:
            map[x][y] = 1


def event():
    global beer, gun

    rand = random.randint(0, 100)

    if been == 1:
        print("You have been here, nothings here mate")
    elif been == 2:
        print("You came across the same ol'bar")
        bar()
    elif rand == 0:
        print("- Seems like you were lucky,")
        print("- you found an old frind of yours")
        print("- a Sheriff like you but not like you")
        print("- you spent some time with him")
        print("- just when you were about to leave")
        rare = random.randint(0, 25)
        if gun == 0 and rare == 0:
            print("- he gave you a gift - 'Desert Eagle'")
            gun = 1
        elif gun == 1 and rare == 0:
            print("- he gave you a gift - 'The Peacemaker'")
            gun = 2
        else:
            print("- he gave you some beer")
            beer += 5
    elif rand in range(4, 28):
        bar()
    elif rand in range(29, 70):
        fight()
    else:
        print("Seem like you are in a bad luck, nothings here")


def bar():
    global hp, money, beer, beenBar

    can = beenBar = True

    print("- Welcome to the bar!")
    rand = random.randint(0, 10)

    if rand == 0:
        print("- A wild sheriff appeared!")
        print("- he paid for your drink")
        print("- you had a good time and")
        print("- replenished 10 hp")
        hp += 10
    elif rand in range(1, 4):
        print("- Some punks wants to fight ya")
        print("- seems like someone is gonna die tonight")
        fight()
        can = False

    if can:
        print("- The bartender looks at ya")
        print("- says 1 beer for 100")
        print("- enter 0 for nothing")
        choice = input("you want something?(y/n) ")

        while choice in "yY":
            number = None
            while not isinstance(number, int):
                try:
                    number = int(input("How much you want(0 for nothing): "))
                except:
                    print("Say a number!!!")
            amount = number * 100
            if amount > money:
                print("- You are too poor for it man")
            else:
                print(f"- Here take it, you got {number} beer")
                beer += number
                money -= amount
            choice = input("you want something?(y/n): ")


def fight():
    global gun, hp, kill, money

    ehp = 5
    flee = legHit = False
    handHit = 0

    print("- Finally someone to kill")
    rand = random.randint(0, 4)

    if rand == 0:
        ename = "Outlaw"
    elif rand == 1:
        ename = "Desparadas"
    elif rand == 2:
        ename = "Bandit"
    elif rand == 3:
        ename = "Ruffian"
    else:
        ename = "Scoundrels"
    print(f"A wild {ename} appeared!!")

    while hp > 0 and ehp > 0 and flee == False:
        print()
        input("Press something to continue: ")
        print()
        print("------------------------------------------------")
        print(f"Your hp = {hp}")
        print(f"His hp = {ehp}")

        if gun == 0:
            head = random.randint(1, 15)
        elif gun == 1:
            head = random.randint(1, 20)
        else:
            head = random.randint(1, 25)
        torso = random.randint(1, 100)
        hands = random.randint(1, 90)
        legs = random.randint(1, 60)

        print("Where you want to shoot -")
        print(f"- 1) head - {head}% chance of hitting")
        print(f"- 2) torso - {torso}% chance of hitting")
        print(f"- 3) hands - {hands}% chance of hitting")
        print(f"- 4) legs - {legs}% chance of hitting")

        aim = ""
        while not (aim == "1" or aim == "2" or aim == "3" or aim == "4"):
            aim = input("Enter the number: ")
        rand = random.randint(1, 100)

        print("------------------------------------------------")
        if aim == "1":
            if rand in range(1, head + 1):
                print("Gottcha! right between the forehead")
                ehp = 0
            else:
                print("Missed it!!")
        elif aim == "2":
            if rand in range(1, torso + 1):
                print(f"Got that bullet inside the {ename}!")
                ehp -= 2
            else:
                print("Missed it!!")
        elif aim == "3":
            if rand in range(1, hands + 1):
                print("Nice aim, now he will miss one chance")
                handHit = 1
                ehp -= 1
            else:
                print("Missed it!!")
        else:
            if rand in range(1, legs + 1):
                print("Now he wont be able to flee")
                legHit = True
                ehp -= 1
            else:
                print("Missed it!!")

        rand = random.randint(1, 100)
        if handHit == 2:
            handHit = 3
        elif handHit == 3:
            handHit = 0

        if rand in range(1, 80) and handHit != 3 and ehp > 0:
            if handHit == 1:
                handHit = 2
                rand = random.randint(1, 100)
                if rand in (1, 2):
                    print("Seems like he got lucky!")
                    print("your bullet to his hand!")
                    print("made his shot towards your head")
                    hp = 0
                elif rand in range(3, 50):
                    print("Seems like he got lucky!")
                    print("your bullet to his hand!")
                    print("made his shot towards your torso")
                    hp -= 2
                print("Now he is immobile for next turn")
            else:
                print("Holy moly, he hit ya hard!")
                hp -= 1
        elif rand == 100 and not (legHit):
            print("He ran away")
            flee == True
        elif handHit == 3:
            print("He is unable to shoot")
        else:
            print("Seems like you fighting a newbie!")
            print("He missed")

    print(f"Your hp = {hp}")
    print(f"His hp = {ehp}")

    if hp > 0 and not flee:
        print("Seems like you killed him")
        print("Seems like he dropped 50 dollars for ya!")
        money += 50
        kill += 1
        print(f"Total kills: {kill}")
    elif flee:
        print("Seems like he flew away")


def save(username):
    cur.execute(f"select * from sheriffs where username = %s;", (username,))
    fetch = cur.fetchall()

    if fetch is None or len(fetch) == 0:
        cur.execute(
            f"insert into sheriffs values (%s, '%s', '%s', %s, '%s', '%s');",
            (username, money, kill, gun, hp, beer),
        )
        con.commit()
        mapSave = [username, map, length, columns]
        with open("saves.dat", "ab+") as fout:
            pickle.dump(mapSave, fout)
        print("Successfully saved")
    else:
        cur.execute(
            f"update sheriffs set money = '%s', kills = '%s', gun = %s, hp = '%s', beer = '%s' where username = %s;",
            (money, kill, gun, hp, beer, username),
        )
        con.commit()
        data = []
        with open("saves.dat", "rb") as fin:
            try:
                while True:
                    data.append(pickle.load(fin))
            except:
                for i in range(len(data)):
                    if data[i][0] == username:
                        data[i][1] = map
                        data[i][2] = length
                        data[i][3] = columns
        with open("saves.dat", "wb") as fout:
            for i in data:
                pickle.dump(i, fout)
        print("Successfully updated")

    print()
    input("Press something to continue: ")
    print()


def load():
    global username, money, kill, gun, hp, beer
    global continueGame, map, length, columns

    username = input("Enter username: ").strip()
    try:
        cur.execute(f"select * from sheriffs where username = %s;", (username,))
        fetch = cur.fetchall()
        if fetch is None or len(fetch) == 0:
            print("A save with that username dosen't exist")
        else:
            username = fetch[0][0]
            money = int(fetch[0][1])
            kill = int(fetch[0][2])
            gun = fetch[0][3]
            hp = int(fetch[0][4])
            beer = int(fetch[0][5])
            continueGame = True
            with open("saves.dat", "rb") as fin:
                try:
                    while True:
                        data = pickle.load(fin)
                        if data[0] == username:
                            map = data[1]
                            length = data[2]
                            columns = data[3]
                            break
                except:
                    pass
                print("Successfully loded")
    except:
        print("A save with that username dosen't exist")

    print()
    input("Press something to continue: ")
    print()


def score():
    cur.execute(f"select username from sheriffs where username = %s;", (username,))
    fetch = cur.fetchall()
    if fetch is None or len(fetch) == 0:
        cur.execute(f"insert into leaderboards values(%s, %s);", (username, kill))
    else:
        cur.execute(f"delete from sheriffs where username = %s;", (username,))
        cur.execute(f"insert into leaderboards values(%s, %s);", (username, kill))
    con.commit()


def how():
    print()
    print("================== How to play ====================")
    print("===== Roam the world like a boss =====")
    print("- You have 10hp, you can lose if")
    print("- it went to 0 but can replenish it too!")
    print("===== kill the bad guys in fight! =====")
    print("- In a fight you have 4 options,")
    print("- shoot the head, torso, legs or hands.")
    print("- head gives 100% kill but has a less chance to hit")
    print("- torso, lowers the enemies hp by 2")
    print("- legs lowers by 1 but makes enemy unable to flee")
    print("- hands lowers by 1 but make complex stuff to happen -")
    print("- it gives the enemy a high chance hit on your head and torso,")
    print("- but makes the enemy skip their next chance")
    print("===== you are not alone =====")
    print("- meet other sheriffs, go to bars, have fun")
    print("======== HAPPY HUNTING ========")

    print()
    input("Press something to continue: ")
    print()


def controls():
    print()
    print("These controls only work when game")
    print("has started, ie press 3 in Main Menu")
    print("========== Controls ==========")
    print("Press n | N to go north|up")
    print("Press e | E to go east|left")
    print("Press w | W to go west|right")
    print("Press s | S to go south|down")
    print("-----------------------------")
    print("Enter 'save' to save the progress")
    print("Press q | Q to quit")
    print("-----------------------------")
    print("Press d | D to drink beer and replenish 1 hp")
    print("Press h | H to see controls")
    print("Press i | I to see inventory")

    print()
    input("Press something to continue: ")
    print()


def game():
    global beer, hp, username

    if not continueGame:
        username = ""
        while username.strip() in "'\"":
            username = input("Enter username: ")

        data = data2 = []
        while True:
            cur.execute(
                f"select username from sheriffs where username = %s;", (username,)
            )
            data = cur.fetchall()
            cur.execute(
                f"select username from leaderboards where username = %s;", (username,)
            )
            data2 = cur.fetchall()

            if not (data == data2 == []):
                print("Already in use or in the leaderboards")
                username = input("Enter another: ")
                while username.strip() in "'\"":
                    print("Username is illegal")
                    username = input("Enter another: ")
            else:
                break
    print()
    print("A lone sheriff in the search for criminals")
    print("Or is he, thirsty of a promotion wreking havoc")
    print("kills every criminal in sight nonstop")
    print("meeting people and drinking beer.")
    print("This is the story of the legend,")
    print(f"THE LEGEND OF THE SHERIFF {username}")

    print()
    input("Press something to continue: ")
    print()

    print("Press 'h' for controls")
    while hp > 0:
        print("--------------------------------------------------")
        choice = input("What you want to do: ")

        while choice.isupper():
            try:
                choice = choice.lower()
            except:
                choice = input("Enter h to see the controls: ")

        if choice == "e" or choice == "w" or choice == "n" or choice == "s":
            movement(choice)
            showMap()
            event()
        elif choice == "i":
            print(f"HP = {hp}")
            print(f"kill = {kill}")
            print(f"Money = {money}")
            print(f"Beer = {beer}")
            if gun == 0:
                print("Gun = Colt buntline")
            elif gun == 2:
                print("Gun = Desert Eagle")
            else:
                print("Gun = The Peacemaker")
        elif choice == "h":
            controls()
        elif choice == "d":
            if beer > 0:
                print(f"You drink the beer you had and felt great")
                hp += 1
                beer -= 1
            else:
                print("Too bad for ya, no beer")
        elif choice == "save":
            save(username)
        elif choice == "q":
            choice = input("Do you want to save your progress(y/n): ")
            if choice in "yY":
                save(username)
            break
        else:
            print("Enter h to see the controls!")


def main():
    while True:
        print("========== THE 2D SHERIFF ==========")
        print("Enter '1' to see how to play")
        print("Enter '2' to see the controls")
        print("Enter '3' to start the game")
        print("Enter '4' to load a saved progress")
        print("Enter '5' to see the leaderbords")
        print("Enter '6' to quit")
        choice = input("Enter your choice: ")

        while type(choice) is str:
            try:
                choice = int(choice)
            except:
                choice = input("Enter a numeric choice(between 1 to 5): ")

        if choice == 1:
            how()
        elif choice == 2:
            controls()
        elif choice == 3:
            game()
            break
        elif choice == 4:
            load()
            if continueGame:
                game()
                break
        elif choice == 5:
            print()
            cur.execute("select * from leaderboards order by kills;")
            data = cur.fetchall()
            print("Username: Kills")
            for i in data:
                print(f"{i[0]}: {i[1]}")
            print()
            input("Press something to continue: ")
            print()
        elif choice == 6:
            break
        else:
            choice = input("Enter a valid choice: ")

    print("----------------------------------------------------")
    if hp <= 0 and choice != 5:
        print(f"Total kills: {kill}")
        print("Seems Like You are Dead!")
        score()
    print("Byeeeeee!")


def database():
    try:
        cur.execute("create database game;")
        cur.execute("use game;")
    except:
        cur.execute("use game;")

    try:
        code = """create table sheriffs
(username varchar(10) primary key, money varchar(5), kills varchar(5), gun int(1), hp varchar(2), beer varchar(2));"""
        cur.execute(code)
    except:
        pass

    try:
        cur.execute(
            "create table leaderboards (username varchar(10) primary key, kills varchar(5));"
        )
    except:
        pass


database()
main()
