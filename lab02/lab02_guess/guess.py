import random
print("Pick a number between 1 and 100 (inclusive)")
ran = random.randint(1,100)
print("My guess is:", ran)
print("Is my guess too low (L), too high (H), or correct (C)?")
get = input()

mini = 1
maxi = 100
while get != "C":
    if get == "L":
        if ran > mini:
            mini = ran
    if get == "H":
        if ran < maxi:
            maxi = ran
    new = random.randint(mini,maxi)
    ran = new
    print("My guess is:", ran)
    print("Is my guess too low (L), too high (H), or correct (C)?")
    get = input()

print("Got it!")    