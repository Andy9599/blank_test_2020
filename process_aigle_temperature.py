#!/usr/bin/env python3

'''
This Python script will

+ Read and parse daily temperature from Aigle weather station
+ Extract monthly and yearly means for the following years :
  1981, 1991, 2001, 2011
+ Save a graph of those in the file `aigle_temperature_means.png`.
'''

import numpy as np
import pandas as pd

SOURCE_FILE = 'aigle_1980-12-31_2019-07-09.csv'
NB_DAYS_PER_MONTH = (0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

temperatures_aigle = pd.read_csv(
    SOURCE_FILE,
    sep=';', usecols=[1, 2], index_col=0,
    parse_dates=True, dtype={'t06200ds': np.float64},
    na_values='-'
)


def extract_temperatures(year, month=0):
    '''
    Will return a ndarray of all temperatures for the period given
    A) extract_temperatures(year)
       -> from year-01-01 - year-12-31
    B) extract_temperatures(year, month)
       -> from year-month-01 - year-month-last_day
    '''
    if month == 0:
        # all year
        start_date = '%s-01-01' % year
        end_date = '%s-12-31' % year
    else:
        # only one month
        start_date = '%s-%s-01' % (year, month)
        end_date = '%s-%s-%s' % (year, month, NB_DAYS_PER_MONTH[month])
        if month == 2 and year % 4 == 0:
            # it is leap year!
            end_date = '%s-%s-29' % (year, month)
    return temperatures_aigle[start_date:end_date].values


if __name__ == '__main__':
    year_1981 = extract_temperatures(1981)
    print('Year 1981 has %s values' % len(year_1981))

    jan_1981 = extract_temperatures(1981, 1)
    print('January 1981 has %s values' % len(jan_1981))

    feb_1981 = extract_temperatures(1981, 2)
    print('February 1981 has %s values' % len(feb_1981))

    year_1984 = extract_temperatures(1984)
    print('Year 1984 has %s values' % len(year_1984))

    feb_1984 = extract_temperatures(1984, 2)
    print('February 1984 has %s values' % len(feb_1984))

    apr_2001 = extract_temperatures(2001, 4)
    print('April 2001 has %s values' % len(apr_2001))
    print(apr_2001)
