from inverse import inverse
from hypothesis import given, strategies

def test():
    assert inverse({1: 'A', 2: 'B', 3: 'A'}) == {'A': [1, 3], 'B': [2]}

@given(strategies.dictionaries(keys=strategies.integers(), values=strategies.characters()))
def test_inverse(d):
    new_d = inverse(d)
    for v in d.values():
        assert v in new_d.keys()
