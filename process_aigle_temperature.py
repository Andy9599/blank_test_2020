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
from matplotlib import pyplot as plt

SOURCE_FILE = 'aigle_1980-12-31_2019-07-09.csv'
NB_DAYS_PER_MONTH = (0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
OBSERVED_YEARS = np.arange(1981, 2012, 10)
MONTHS = np.arange(1, 13)
MONTHS_LABELS = [
    'jan', 'feb', 'mar', 'apr', 'may', 'jun',
    'jul', 'aug', 'sep', 'oct', 'nov', 'dec'
]
COLORS = {
    1981: 'blue',
    1991: 'green',
    2001: 'orange',
    2011: 'red',
}
PNG_FILENAME = 'aigle_temperature_means.png'
GRAPH_TITLE = 'Aigle - Average temperature per month'
GRAPH_X_LABEL = 'months'
GRAPH_Y_LABEL = 'mean temperature'

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
    plt.figure(figsize=(8, 6), dpi=120)

    for year in OBSERVED_YEARS:
        year_temperatures = extract_temperatures(year)
        year_mean = np.nanmean(year_temperatures)
        label = '%s (mean = %.2f°C)' % (year, year_mean)

        monthly_mean_values = np.zeros_like(MONTHS, dtype=np.float64)
        for month in MONTHS:
            month_temperatures = extract_temperatures(year, month)
            monthly_mean_values[month-1] = np.nanmean(month_temperatures)

        plt.plot(
            MONTHS, monthly_mean_values,
            color=COLORS[year], label=label
        )

    ax = plt.gca()

    plt.title(GRAPH_TITLE)
    plt.legend()
    ax.set_xlabel(GRAPH_X_LABEL)
    ax.set_ylabel(GRAPH_Y_LABEL)

    plt.xticks(MONTHS, MONTHS_LABELS)
    plt.grid(b=True, which='major', axis='y')
    plt.savefig(PNG_FILENAME)
