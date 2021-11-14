import pytest
from timetable import timetable
from datetime import date, time, datetime

def test_timetable():
    assert timetable([date(2019,9,27), date(2019,9,30)], [time(14,10), time(10,30)]) == [datetime(2019,9,27,10,30), datetime(2019,9,27,14,10), datetime(2019,9,30,10,30), datetime(2019,9,30,14,10)]

def test_empty():
    with pytest.raises(ValueError):
        timetable([], []) == []

def test_no_date():
    with pytest.raises(ValueError):
        timetable([], [time(14,10), time(10,30)])

def test_no_time():
    with pytest.raises(ValueError):
        timetable([date(2019,9,27), date(2019,9,30)],[])