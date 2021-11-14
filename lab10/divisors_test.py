from divisors import divisors
from hypothesis import given, strategies
import pytest

def test_12():
    assert divisors(12) == {1,2,3,4,6,12}

def test_str():
    with pytest.raises(ValueError):
        divisors("aa")

@given(strategies.integers(min_value=1, max_value=10000))
def test_divisible(n):
    for d in divisors(n):
        assert n % d == 0

@given(strategies.integers(max_value=0))
def test_nonpositive(n):
    with pytest.raises(ValueError):
        divisors(n)