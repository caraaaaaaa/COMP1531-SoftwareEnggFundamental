def roman(numerals):
    '''
    Given Roman numerals as a string, return their value as an integer. You may
    assume the Roman numerals are in the "standard" form, i.e. any digits
    involving 4 and 9 will always appear in the subtractive form.

    For example:
    >>> roman("II")
    2
    >>> roman("IV")
    4
    >>> roman("IX")
    9
    >>> roman("XIX")
    19
    >>> roman("XX")
    20
    >>> roman("MDCCLXXVI")
    1776
    >>> roman("MMXIX")
    2019
    '''
    error = 0
    for letter in numerals:
        if letter not in ('I', 'V', 'X', 'L', 'C', 'D', 'M'):
            error = 1
    if error == 1:
        raise ValueError        
    
    roman_letter = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    result = 0
    for i in range(len(numerals)):
        # add first straightly    
        if i == 0:
            result+=roman_letter[numerals[i]]
        # add together when [i] <= [i-1]
        # which means add straightly
        elif roman_letter[numerals[i]] <= roman_letter[numerals[i-1]]:
            result = result + roman_letter[numerals[i]]
        # [i] > [i-1]
        # need to minus 2* [i-1] (because already add one time before)
        else:
            result = result + roman_letter[numerals[i]] - 2 * roman_letter[numerals[i-1]]
    return result   