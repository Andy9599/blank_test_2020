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

temperatures_aigle = pd.read_csv(
    SOURCE_FILE,
    sep=';', usecols=[1, 2], index_col=0,
    parse_dates=True, dtype={'t06200ds': np.float64},
    na_values='-'
)


if __name__ == '__main__':

    start_date = '1981-01-01'
    end_date = '1981-12-31'
    temperatures = temperatures_aigle[start_date:end_date].values

    print(temperatures)
