'''
Tests for reverse_words()
'''
from reverse import reverse_words

def test_example():
    assert reverse_words(["Hello World", "I am here"]) == ['World Hello', 'here am I']
    assert reverse_words([]) == []
    assert reverse_words(["Hello"]) == ["Hello"]
    assert reverse_words(["Hello Cara a"]) == ["a Cara Hello"]
    assert reverse_words(["a", "b"]) == ["a", "b"]
    assert reverse_words(["Hello a b", "a b Hello"]) == ["b a Hello", "Hello b a"]
    

