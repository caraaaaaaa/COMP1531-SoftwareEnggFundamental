def prefix_search(dictionary, key_prefix):
    '''
    Given a dictionary (with strings for keys) and a string, returns a new dictionary containing only the keys (and their corresponding values) for which the string is a prefix.
    If the string is not a prefix for any key, a KeyError is raised.
    You can assume that you will not be given any empty strings in dictionary or as key_prefix

    For example,
    #>>> prefix_search({"ac": 1, "ba": 2, "ab": 3}, "a")
    {'ac': 1, 'ab': 3}
    '''
    error = 0
    new_dic = {}
    for key in dictionary.keys():
        if key_prefix == key[0:len(key_prefix)]:
            error = 1
            new_dic[key] = dictionary[key]
    if error == 0:
        raise KeyError
    return new_dic