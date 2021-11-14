import pytest
from roman import roman

def test_roman():
    assert roman("II") == 2

def test_roman():
    assert roman("IV") == 4

def test_roman():
    assert roman("IX") == 9

def test_roman():
    assert roman("XIX") == 19

def test_roman():
    assert roman("MDCCLXXVI") == 1776

def test_roman():
    assert roman("MMXIX") == 2019

def test_error():
    with pytest.raises(ValueError):
        roman("A")    

def test_zero():
    with pytest.raises(ValueError):
        roman("0")
     