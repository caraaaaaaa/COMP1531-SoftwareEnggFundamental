def reverse_words(string_list):
    '''
    Given a list of strings, return a new list where the order of the words is
    reversed
    '''
    for string in range(len(string_list)):
        y = string_list[string].split()
        string_list[string] = " ".join(reversed(y))

    return string_list   
    #pass

if __name__ == "__main__":
    print(reverse_words(["Hello World", "I am here"]))
    # it should print ['World Hello', 'here am I']