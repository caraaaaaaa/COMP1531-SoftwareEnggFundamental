'''to test circle.py'''
from circle import Circle

def test_small():
    '''test for a small value radius'''
    circle1 = Circle(3)
    assert round(circle1.circumference(), 1) == 18.8
    assert round(circle1.area(), 1) == 28.3

def test_float():
    '''test for a float radius'''
    circle2 = Circle(3.3)
    assert round(circle2.circumference(), 1) == 20.7
    assert round(circle2.area(), 1) == 34.2
