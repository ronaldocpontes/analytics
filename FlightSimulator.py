#!/usr/bin/python
# -*- coding: utf-8 -*-

'''


@author: Ronaldo Pontes
@contact: 
@summary: 
'''

import sys

import numpy as np
import pandas as pd

import projects.flight.Flight as fl
from tools import charting as charting


print "hi"

import logging
logging.basicConfig()
log = logging.getLogger("Flight")
log.setLevel(logging.INFO)


consumer_sample_csv = "flight-demand.csv"


#
# Read the definition of the orders from a csv file
#
passenger_data = pd.read_csv(consumer_sample_csv,
                    sep=',',
                    header=0,
                    # index_col=[0,1,2],
                    # parse_dates = [['YYYY','MM','DD']],
                    parse_dates=True)

print consumer_sample_csv, ": ", passenger_data

passengers = passenger_data
def runSimulation(economy_fare, business_fare,check_seats=True, check_space=True):
    flight = fl.Flight()

    flight.plane_space = 60
    flight.economy_seat_space = 0.5
    flight.business_seat_space = 1.5


    flight.business_seats = 30
    flight.economy_seats = 30
    flight.business_fare = business_fare
    flight.economy_fare = economy_fare
    flight.business_cost = 1500
    flight.economy_cost = 500


    for i, passenger in passengers.iterrows():
        try:
            flight.addPassenger(passenger[0],passenger[1], check_seats=check_seats, check_space=check_space)
        except:
            break


    log.info("=======================")
    log.info( "Flight Simulation Results...")
    log.info("=======================")

    log.info( "Total demand = %s passengers", len(passengers))
    log.info( flight.stats())

    log.info( flight.total_profits())
    log.info( flight.total_profits() - 132130)

    #return flight.total_profits()
    return flight


def bootstrap_simulation():
    n=3
    profits=[]
    b_seats=[]
    e_seats=[]

    for i in range(0, n):
        bootstraped_passengers = bt.resample_pandas(passenger_data,400)
        total_bootstraped_passengers = pd.concat([passenger_data, bootstraped_passengers])
        passengers =  total_bootstraped_passengers
        flight = runSimulation(863, 3442)

        profits.append(flight.total_profits())
        b_seats.append(flight.business_seats)
        e_seats.append(flight.economy_seats)

    sys.exit(1)

    print bootstraped_passengers


def scalarSimulation(economy_fare, business_fare ):
    return runSimulation(economy_fare, business_fare).total_profits()


log.setLevel(logging.ERROR)
def findMaximum(psg, Xa,Ya):

    X, Y = np.meshgrid(Xa, Ya)
    vecfunc = np.vectorize(scalarSimulation)
    Z = vecfunc(X, Y)

    results = np.unravel_index(Z.argmax(),Z.shape)
    print "Results: ", Z.max()
    print "Results: ", Z.argmax()
    print "Results: ", results
    print "Results: ", Z[results[0],results[1]]
    print "Results: ", Xa[results[1]]
    print "Results: ", Ya[results[0]]
    charting.plotChart(X,Y,Z)
    charting.plot.show()

    return Xa[results[1]], Ya[results[0]]

log.setLevel(logging.WARN)
passengers = pd.concat([passenger_data, passenger_data,passenger_data,passenger_data,passenger_data])
#print runSimulation(863, 3442).stats()

log.setLevel(logging.WARN)
print passengers
#print runSimulation(5000, 3770,check_seats=True).stats()
#print runSimulation(1134, 3959,check_seats=True).stats()
print runSimulation(1149, 2009,check_seats=True).stats()
sys.exit()


steps = 10

Xa = np.arange(753, 1103, steps)
Ya = np.arange(2502, 4002, steps)

Xa = np.arange(500, 1300, steps)
Ya = np.arange(2500, 4200, steps)


steps = 1
Xa = np.arange(1050, 1200, steps)
Ya = np.arange(3700, 3800, steps)
#Results:  1191
#Results:  3770
#('Total Profits:', 90800, 'Economy Fare: ', 1191, 'Business Fare: ', 3770, 'Business Passengers:', 40, 'Economy Passengers:', 0, 'Business Profits: ', 90800, 'Economy Profits:', 0, 'Used Space:', 60.0, 'Space Left:', 0.0)

steps = 10
Xa = np.arange(950, 1400, steps)
Ya = np.arange(3270, 4900, steps)


results = findMaximum(passenger_data,Xa,Ya)
print runSimulation(results[0],results[1]).stats()

#Results:  132130
#Results:  863
#Results:  3442



print "finished"