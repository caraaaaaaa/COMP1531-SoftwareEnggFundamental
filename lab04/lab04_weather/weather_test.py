'''test weather.py '''
from weather import weather

def test_weather():
    '''test for a valid date and location'''
    assert weather('08-08-2010', 'Albury') == (10.8, 10)

def test_no_date():
    '''test when input date is not in csv'''
    assert weather('08-08-2030', 'Albury') == (None, None)

def test_no_location():
    '''test when input location is not in csv'''
    assert weather('08-08-2020', 'Guozixuan') == (None, None)

def test_empty_date():
    '''test when input date is empty'''
    assert weather('', 'Albury') == (None, None)

def test_empty_location():
    '''test when input location is empty'''
    assert weather('08-08-2020', '') == (None, None)
