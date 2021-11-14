from fibonacci import generate
import pytest

def test_fibonacci():
    assert generate(10) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

def test_fibonacci_input_less_zero():
    with pytest.raises(ValueError):
        generate(-1)

def test_fibonacci_input_not_integer():
    with pytest.raises(TypeError):
        generate('a')