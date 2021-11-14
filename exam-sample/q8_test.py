from q8 import reverse_words

def test_two_multiple():
	assert reverse_words(["Hello World", "I am here"]) == ['World Hello', 'here am I']

def test_empty():
	assert reverse_words([]) == []
	assert reverse_words(["Hello"]) == ["Hello"]
	assert reverse_words(["Hello Cara a"]) == ["a Cara Hello"]
	assert reverse_words(["a", "b"]) == ["a", "b"]
	assert reverse_words(["Hello a b", "a b Hello"]) == ["b a Hello", "Hello b a"]