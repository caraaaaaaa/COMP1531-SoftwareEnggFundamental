def cipher(key, message):
    # new list
    key_list = []
    for i in range(50):
        key_list.append([])
        for j in range(50):
            key_list[i].append("")
            
    key_num = 0
    index = 0
    for char in range(len(key)):
        key_num+=1
        
        key_list[char][0] = key[char]
        if index < 10:
            key_list[char][1] = " " + str(index)
        else:
            key_list[char][1] = str(index)
        index+=1

    # store message in    
    index = 0
    j = 2
    i = 0
    for char in message:
        if char.isalpha():
            key_list[i][j] = char
            if index % key_num == (key_num-1):
                j+=1
                i = 0
            else:
                i+=1    
            index+=1

    # fill abcde        
    if i != 0:
        fill_n = 0
        fill = ["a", "b", "c", "d", "e", "f", "g", "h", "i","j","k","l","m","n","o","p","q","r","s","t","u", "v","w","x", "y","z"]
        for ind in range(i,key_num):
            key_list[ind][j] = fill[fill_n%26]
            fill_n+=1

    encrypt = []

    # join list together
    listall = []
    for i in range(50):
        listall.append("")

    for i in range(50):
        for j in range(50):
            if len(key_list[i][j]) > 0:
                encrypt.append(key_list[i][j])
        listall[i] = "".join(encrypt)
        encrypt = []
    listall.sort()
   
    result = []
    for element in listall:
        if len(element) > 0:
            result.append(element[3:])

    return "".join(result)

#print(cipher('Supercalafagialisticexpialadotious', 'Hello there'))

# == 'H        hradoqtjrlkebcfinueepsvl         m o g x h te w l'
    #H0a3d4o6qhr9jt7r0kle1b2c5f8i3n0u4e5pe8s1v2mlo6g3x7h9te2w1l