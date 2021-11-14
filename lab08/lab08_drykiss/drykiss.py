from functools import reduce

def drykiss(my_list):
    # use python built-in function
    my_min = min(my_list)
    product_first = reduce((lambda x, y: x * y), my_list[0:4])
    product_last = reduce((lambda x, y: x * y), my_list[1:5])

    result = (my_min, product_first, product_last)
    return result

if __name__ == '__main__':
    # takes 5 numbers at one time,
    # trans string to list
    # trans to integer using map()
    my_list = list(map(int, input("Enter a b c d e: ").split(' ')))

    result = drykiss(my_list)
    print("Minimum:", result[0])
    # using f string and newline '\n'
    print(f"Product of first 4 numbers: \n  {result[1]}")
    print(f"Product of last 4 numbers\n  {result[2]}")
