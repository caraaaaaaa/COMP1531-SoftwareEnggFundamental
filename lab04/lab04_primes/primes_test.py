'''test primes.py'''
import primes
import pytest

def test_prime_factor():
    '''test find a factor of prime number'''
    assert primes.factors(2) == [2]

def test_factor():
    '''test find a factor'''
    assert primes.factors(16) == [2, 2, 2, 2]

def test_factor_asscending():
    '''test find a factor'''
    assert primes.factors(30) == [2, 3, 5]

def test_factor_square():
    '''test square number'''
    assert primes.factors(25) == [5, 5]

def test_one():
    '''test find prime factor of 1'''
    with pytest.raises(ValueError):
        primes.factors(1)

def test_zero():
    '''test find prime factor of 0'''
    with pytest.raises(ValueError):
        primes.factors(0)

def test_negative_num():
    '''test find prime factor of negative number'''
    with pytest.raises(ValueError):
        primes.factors(-10)

def test_non_int():
    '''test find prime factor of 0'''
    with pytest.raises(TypeError):
        primes.factors('a')
