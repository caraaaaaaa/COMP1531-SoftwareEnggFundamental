from factors import factors, is_prime
from hypothesis import given, strategies
import inspect
import pytest

def test_generator():
    '''
    Ensure it is generator function
    '''
    assert inspect.isgeneratorfunction(factors), "factors does not appear to be a generator"


def test_factor():
    assert list(factors(12)) == [2,2,3]