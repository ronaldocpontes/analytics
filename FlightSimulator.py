#!/usr/bin/python
# -*- coding: utf-8 -*-

'''


@author: Ronaldo Pontes
@contact: 
@summary: 
'''

import pandas
import numpy as np
import math
import copy
import datetime as dt
from pandas.io.parsers import ExcelWriter
from pandas.core.frame import DataFrame
from pandas.core import series
from pandas.core.series import Series
import pandas as pd

import scipy
from scipy.optimize import fsolve

# Get the data from the data store

print "hi"

consumer_sample_csv = "FlightSimulator.csv"


#
# Read the definition of the orders from a csv file
#
orders = pd.read_csv(consumer_sample_csv,
                    sep=',',
                    header=0,
                    # index_col=[0,1,2],
                    # parse_dates = [['YYYY','MM','DD']],
                    parse_dates=True)

print orders

print "lalala"

for c in orders:
    print c



def function_to_find_root_of(x, slope, yintercept):
    ''' x is a list of all the variables you need to minimize
        the other variables will be passed in as constants '''

    return slope*x + yintercept

m = 4
b = 7
print fsolve(function_to_find_root_of, x0=[10], args=(m, b), xtol=1e-10)
'''prints [-1.75], which is the root of y=4x+7 '''

print "finished"