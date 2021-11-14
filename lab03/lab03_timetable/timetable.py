from datetime import date, time, datetime

def timetable(dates, times):
    '''
    Generates a list of datetimes given a list of dates and a list of times. All possible combinations of date and time are contained within the result. 
    The result is sorted in chronological order.

    For example,
    >>> timetable([date(2019,9,27), date(2019,9,30)], [time(14,10), time(10,30)])
    [datetime(2019,9,27,10,30), datetime(2019,9,27,14,10), datetime(2019,9,30,10,30), datetime(2019,9,30,14,10)]
    '''

    if len(dates) == 0:
        raise ValueError
    if len(times) == 0:
        raise ValueError

    dates_new = sorted(dates)
    times_new = sorted(times)
    
    datestime_list = []
    for i in dates_new:
        for j in times_new:
            datesTime = datetime.strptime(str(i) + ' ' + str(j),"%Y-%m-%d %H:%M:%S")
            datestime_list.append(datesTime)
            
    return datestime_list
