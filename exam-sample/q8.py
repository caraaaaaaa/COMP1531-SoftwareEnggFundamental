def reverse_words(string_list):
    new_list = []
    for string in string_list:
        y = reversed(string.split())
        print(y)
        new_list.append(" ".join(y))

    return new_list  
    

        
print(reverse_words(['Hello world', "i am cara"]))