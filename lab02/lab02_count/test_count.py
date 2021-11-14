from count import count_char

def test_empty():
    assert count_char("") == {}

def test_simple():
    assert count_char("abc") == {"a": 1, "b": 1, "c": 1}

def test_double():
    assert count_char("aa") == {"a": 2}

def test_complex():    
    assert count_char("aabc") == {"a": 2, "b": 1, "c": 1}
    assert count_char("abbccc") == {"a": 1, "b": 2, "c": 3}
