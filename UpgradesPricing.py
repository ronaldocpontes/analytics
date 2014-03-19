__author__ = 'Ronaldo'

import numpy as np
import pandas as pd
import tools.pandas.Dataframe as df_tools
from tools.pandas.SortingStore import SortingStore
import sys



class DemandSupply:

    def __init__(self, demand_dataframe):
        self.df = demand_dataframe
        self.prepared_df = demand_dataframe
        self.__sortingStore = SortingStore(demand_dataframe)

    def prepare_demand_dataframe(self, cheaper_column, cheaper_marginal_cost, expensive_column, expensive_marginal_cost, upgrades = [], q_multiplier=1):

        base_sorted = self.__sortingStore.get_sorted_view(cheaper_column,0)

        for u in upgrades:
            pass

        base_sorted[cheaper_column + '_qtd'] = [x * q_multiplier for x in range(1, len(base_sorted) + 1, 1)]
        base_sorted[cheaper_column+'_profits'] = (base_sorted[cheaper_column] - cheaper_marginal_cost )* base_sorted[cheaper_column+'_qtd']

        base_sorted[expensive_column + '_qtd'] = [x * q_multiplier for x in range(1, len(base_sorted) + 1, 1)]
        base_sorted[expensive_column+'_profits'] = (base_sorted[expensive_column] - expensive_marginal_cost)* base_sorted[expensive_column+'_qtd']

        up_marginal_cost = expensive_marginal_cost - cheaper_marginal_cost
        base_sorted['upgrade'] = base_sorted[expensive_column] - base_sorted[cheaper_column]
        base_sorted['upgrade_qtd'] = [x * q_multiplier for x in range(1, len(base_sorted) + 1, 1)]
        base_sorted['upgrade_profits'] = (base_sorted['upgrade'] - up_marginal_cost)* base_sorted['upgrade_qtd']

        self.__sortingStore.set_sorted_view(base_sorted,cheaper_column,0)

        return base_sorted


    def get_price(self,product,quantity):
        return self.__sortingStore.lookup(product+'_qtd',quantity,ascending=0,lookupMode=SortingStore.LookupModes.EXACT_OR_GREATER)[product]


    def get_q_max(self, base_column, base_marginal_cost):

        base_sorted = self.__sortingStore.get_sorted_view(base_column,0)
        demand_supply_dataframe = base_sorted[base_sorted[base_column] > base_marginal_cost]

        max_row = demand_supply_dataframe.irow(-1)
        star_row = demand_supply_dataframe.ix[demand_supply_dataframe[base_column+'_profits'].idxmax()]

        return {'column'        :base_column,
                'q_max'         :max_row[base_column+'_qtd'],
                'q_max_price'  :max_row[base_column],
                'q_*'          :star_row[base_column+'_qtd'],
                'q_*_price'    :star_row[base_column]
                }


    def get_best_product_offering(self, base_results,upgrade_results):
        base_star_results = {
                        'column'        :("Base Product: %s" % base_results['column']),
                        'q_max'         :base_results['q_max'] - upgrade_results['q_max'],
                        'q_max_price:'  :base_results['q_max_price'] + upgrade_results['q_max_price'],
                        'q_*:'          :base_results['q_*'] - upgrade_results['q_*'],
                        'q_*_price:'    :base_results['q_*_price'] + upgrade_results['q_*_price'],
                        }

        return {
                        'base'   :base_star_results,
                        'upgrade'    :upgrade_results,
                        }



class CournotCompetition:

    def __init__(self, demandSupply=None, product=None):

        if not isinstance(demandSupply,DemandSupply):
            if demandSupply != None:
                raise Exception('demandSupply must be an instance of %s class' % DemandSupply.__class__)

        self.demandSupply = demandSupply
        self.product = product


    def _calculate_profits(self, df, product=None):
        qt = df['q'].sum()

        if not isinstance(self.demandSupply,DemandSupply):
            df['p'] = 100-qt
        else:
            df['p'] = self.demandSupply.get_price(product,qt)


        df['unit_profit'] = df['p']-df['mc']
        df['profits'] = df['unit_profit'] * df['q'].T
        return df


    def _cournot_iteration(self, last_state, product=None):

        last_row = last_state.irow(-1)
        new_state = pd.DataFrame()

        for i in last_state.index:
            row = last_state.ix[i]

            it = pd.DataFrame({
                                'q_max':[row['q_max']],
                                'mc':[row['mc']]
                             })
            my_q_max = row['q_max']
            competitors = last_state['q'].count()
            competitors_output = last_row['q']

            upgrades = 0
            if 'upgrades' in last_state.columns:
                upgrades = row['upgrades']
                it['upgrades'] = upgrades

            it['q']=((my_q_max-competitors_output)/ competitors) - upgrades

            it['q'][it['q']<0] = 0 #no negative quantity

            new_state = new_state.append(it)
            last_row = it

        new_state.index = range(len(new_state))
        return self._calculate_profits(new_state, product=product )


    def cournout(self, initial_state, product=None, verbose=False):

        second_it = None
        last_it = self._calculate_profits(initial_state, product=product )
        if verbose: print initial_state
        equal = False
        while not equal:
            it = self._cournot_iteration(last_it, product=product )
            equal = df_tools.is_equal(last_it, it)

            if df_tools.is_equal(second_it, it):
                if verbose: print it.head()
                print "Infinite repetition..."
                print "Response between the 2 last iterations!"
                return it

            if verbose: print it.head()
            second_it = last_it
            last_it = it
        return it

    def get_best_product_offering(self, base_results,upgrade_results):

        business_results = upgrade_results.copy()
        business_results['p'] =  base_results['p'] +  upgrade_results['p']

        unit_profit = base_results['p']-base_results['mc']
        base_star_results = pd.DataFrame({
                            'q_max'       :base_results['q_max'],
                            'mc'          :base_results['mc'],
                            'q'         :base_results['q'] - upgrade_results['q'],
                            'p'         :base_results['p'],
                            'unit_profit' :unit_profit,
                            'profits'     :unit_profit*base_results['q']
                            })


        return {
                        'base'      :base_star_results,
                        'business'  :business_results,
                        'upgrade'   :upgrade_results,
                        }



consumer_sample_csv = "flight-demand.csv"

multiplier = 5
econ = 'Economy'
club = 'Club'
upgrade = 'upgrade'
econ_mc = 500
club_mc = 1500
up_mc = club_mc - econ_mc


#
# Read the definition of the orders from a csv file
#
passenger_data = pd.read_csv(consumer_sample_csv,
                    sep=',',
                    header=0,
                    # index_col=[0,1,2],
                    # parse_dates = [['YYYY','MM','DD']],
                    parse_dates=True,
                    dtype=  {
                                econ: np.float64,
                                club: np.float64
                            }
                    )
print passenger_data.head()

print consumer_sample_csv, ": \n", passenger_data.describe()

demandSupply = DemandSupply(passenger_data)

prepared_data = demandSupply.prepare_demand_dataframe(econ,econ_mc,club,club_mc,q_multiplier=5)

print prepared_data.head()

econ_results =  demandSupply.get_q_max(econ,econ_mc)
club_results =  demandSupply.get_q_max(club,club_mc)
up_results =  demandSupply.get_q_max('upgrade',up_mc)

print demandSupply.get_best_product_offering(econ_results,up_results)




#print '161=884: %s' % demandSupply.get_price(econ,161)
#print '160=887: %s' % demandSupply.get_price(econ,160)
#print '171=876: %s' % demandSupply.get_price(econ,171)
#print '161=1466: %s' % demandSupply.get_price(club,161)
#print '160=1477: %s' % demandSupply.get_price(club,160)
#print '171=1433: %s' % demandSupply.get_price(club,171)
#sys.exit()

cournot_basic = CournotCompetition()
cournot = CournotCompetition(demandSupply)

initial_state = pd.DataFrame({
    'q_max': [33,33],
    'mc': [10,5],
    'q': [30,30]
    })
#cournot_basic.cournout(initial_state, verbose=True)
#sys.exit()

initial_state = pd.DataFrame({
    'q_max': [300,300],
    'mc': [500,500],
    'q': [30,30]
    })
#Cournot Results - Question 3 - Econ
#    mc  q_max    q    p  unit_profit  profits
#0  500    300  100  840          340    34000
#1  500    300  100  840          340    34000


initial_state = pd.DataFrame({
    'q_max': [140,140],
    'mc': [1000,1000],
    'q': [30,30]
    })
#Cournot Results - Question 3 - Upgrade
#     mc  q_max          q     p  unit_profit       profits
#0  1000    140  46.666603  1344          344  16053.311462
#1  1000    140  46.666603  1344          344  16053.311462


upgrade_cournot = cournot.cournout(initial_state,upgrade, verbose=False)
print "COURNOT: UPGRADE ...\n%s", upgrade_cournot.head()


initial_state = pd.DataFrame({
    'q_max': [300,300],
    'mc': [500,500],
    'q': [30,30]
    })
#ECONOMY ONLY COURNOT...
#    mc  q_max    q    p  unit_profit  profits
#0  500    300  100  840          340    34000
#1  500    300  100  840          340    34000

economy_only_cournot = cournot.cournout(initial_state,econ, verbose=False)
print "COURNOT: ECONOMY ONLY ...\n%s" % economy_only_cournot.head()

best_offering =  cournot.get_best_product_offering(economy_only_cournot,upgrade_cournot)
print "3i - COURNOT: ECONOMY AS BASE PRODUCT...\n%s" % best_offering['base']

print "3i - COURNOT: CLUB AS UPGRADE PRODUCT...\n%s" % best_offering['business']

###########################################################

initial_state = pd.DataFrame({
    'q_max': [300,300],
    'mc': [500,500],
    'q': [30,30],
    'upgrades': [0,40]
    })
#ECONOMY ONLY COURNOT...
#    mc  q_max    q    p  unit_profit  profits
#0  500    300  100  840          340    34000
#1  500    300  100  840          340    34000

economy_only_cournot = cournot.cournout(initial_state,econ, verbose=False)
print "3ii - COURNOT: ECONOMY ONLY ...\n%s" % economy_only_cournot.head()

