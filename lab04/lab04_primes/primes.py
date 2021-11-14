'''COMP1531 lab04 find factors of a number'''
#import math

def factors(num):
    '''
    Returns a list containing the prime factors of 'num'. The primes should be
    listed in ascending order.

    For example:
    >>> factors(16)
    [2, 2, 2, 2]
    >>> factors(21)
    [3, 7]
    '''
    if isinstance(num, int) is False:
        raise TypeError()
    if num < 2:
        raise ValueError()

    factor_list = []
    new_num = num
    i = 2
    while is_prime(new_num) is False:
        if is_prime(i):
            if new_num % i == 0:
                factor_list.append(i)
                new_num = int(new_num / i)
                i = 2
            else:
                i+=1
        else:
            i+=1

    factor_list.append(new_num)
    return factor_list

def is_prime(numb):
    '''Determine if a number is prime'''
    for i in range(2,numb):
        if (numb % i) == 0:
            return False
    return True
