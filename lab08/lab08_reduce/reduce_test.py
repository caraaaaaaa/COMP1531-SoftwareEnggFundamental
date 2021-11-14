from reduce import reduce

def test_empty_list():
    assert reduce(lambda x, y: x + y, []) == None

def test_one_element():
    assert reduce(lambda x, y: x + y, [1]) == 1

def test_string():
    assert reduce(lambda x, y: x + y, 'abcdefg') == 'abcdefg'

def test_char():
    assert reduce(lambda x, y: x + y, 'a') == 'a'

def test_multiplication():
    assert reduce(lambda x, y: x * y, [1,2,3,4,5]) == 120