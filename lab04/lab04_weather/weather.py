'''COMP1531 lab04 '''
import datetime
import csv


def weather(date, location):
    '''given a date and location,
    return the difference between average temperate and date temperate'''
    if date == '' or location == '':
        return (None, None)

    csvfile = open('weatherAUS.csv', 'r')
    reader = csv.DictReader(csvfile)

    mean_mintemp_l = []
    mean_maxtemp_l = []
    mean_mintemp = 0
    mean_maxtemp = 0
    min_temp = 1111
    max_temp = -1111

    newdate = datetime.datetime.strptime(date, "%d-%m-%Y")
    for row in reader:
        if row['Location'] == location:
            mean_mintemp_l.append(str(row['MinTemp']))
            mean_maxtemp_l.append(str(row['MaxTemp']))

            if datetime.datetime.strptime(row['Date'], "%Y-%m-%d") == newdate:
                min_temp = float(row['MinTemp'])
                max_temp = float(row['MaxTemp'])
    if len(mean_mintemp_l) == 0:
        return (None, None)
    if min_temp == 1111 or max_temp == -1111:
        return (None, None)
    mean_mintemp = sum([float(res)
                            for res in mean_mintemp_l if res != 'NA']) / len([float(res)
                            for res in mean_mintemp_l if res != 'NA'])
    mean_maxtemp = sum([float(res)
                            for res in mean_maxtemp_l if res != 'NA']) / len([float(res)
                            for res in mean_maxtemp_l if res != 'NA'])
    #print(mean_mintemp, mean_maxtemp)
    #print(min_temp, max_temp)
    return (round(mean_mintemp - min_temp, 1), round(mean_maxtemp - max_temp, 1))
