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
from pandas.core.frame import DataFrame
from pandas.core import series
from pandas.core.series import Series
import pandas as pd

import scipy
from scipy.optimize import fsolve

# Get the data from the data store

print "hi"


class Plane:
    business_seats = 0
    economy_seats = 0
    business_fare = 0
    economy_fare = 0
    business_cost = 0
    economy_cost = 0

    business_passengers = 0
    economy_passengers = 0
    business_profits = 0
    economy_profits = 0

    def f(self,business_seats,business_fare,business_cost,economy_seats,economy_fare,economy_cost):
        self.business_fare = business_fare
        self.business_seats = business_seats
        self.business_cost = business_cost
        self.economy_seats = economy_seats
        self.economy_fare=economy_fare
        self.economy_cost = economy_cost
        return 'hello world'

plane = Plane()

plane.business_seats = 40
plane.economy_seats = 150
plane.business_fare = 900
plane.economy_fare = 1600
plane.business_cost = 1500
plane.economy_cost = 500

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


import scipy.optimize as optimize

def f(c):
    return math.sqrt(c[0]**2 + c[1]**2 + c[2]**2)

result = optimize.minimize(f, [1,1,1])
print(result)

print "finished"