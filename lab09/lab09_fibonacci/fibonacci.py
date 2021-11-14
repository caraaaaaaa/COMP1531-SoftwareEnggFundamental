def generate(n):
    if not isinstance(n, int):
        raise TypeError()
    if n < 0:
        raise ValueError()
    
    fibonacci_list = []
    first = 0
    second = 1
    new = 2
    for i in range(n):
        if i == 0:
            fibonacci_list.append(first)
            first = 1
        elif (i == 1) or (i == 2):
            fibonacci_list.append(second)
        else:
            new = first + second
            fibonacci_list.append(new)
            first = second
            second = new
        
    return fibonacci_list
