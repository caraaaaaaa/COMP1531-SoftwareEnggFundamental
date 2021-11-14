from prefix import prefix_search
import pytest

def test_documentation():
    assert prefix_search({"ac": 1, "ba": 2, "ab": 3}, "a") == { "ac": 1, "ab": 3}

def test_exact_match():
    assert prefix_search({"category": "math", "cat": "animal"}, "cat") == {"category": "math", "cat": "animal"}

def test_no_mach():
    with pytest.raises(KeyError):
        prefix_search({"abc": 1, 'bcd': 2, 'def': 3}, "xyz")

def test_empty():
    with pytest.raises(KeyError):
        prefix_search({}, "xyz")