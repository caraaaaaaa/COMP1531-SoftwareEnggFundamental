def magic(square):
    n = len(square)
    print(set(range(1, n ** 2 + 1)))
    print(set(i for r in square for i in r))
    if set(range(1, n ** 2 + 1)) != set(i for r in square for i in r):
        return 'Invalid data: missing or repeated number' 

    magic = 1
    k = 1
    for i in range(len(square)):
        for j in range(len(square)):
            if k != square[i][j]:
                magic = 3
            k+=1 
    if magic == 3:
        return 'Magic square'  
    elif magic == 1:
        return 'Not a magic square'