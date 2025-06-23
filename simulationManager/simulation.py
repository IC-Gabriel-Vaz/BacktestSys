import datetime as dt

import pandas as pd
import sqlite3
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from simulationManager.rebalance import Rebalance

class Simulation():

    def __init__(self,_data):

        self.data = _data

        self.portfolioValue = 0

        self.weights = {date: {} for date in self.data.rebalanceDates}

        self.capital_per_asset = {date: {} for date in self.data.rebalanceDates}

        self.shares_per_asset = {date: {} for date in self.data.rebalanceDates}

        self.performance = {date: {} for date in self.data.rebalanceDates}

        self.last_rebalance_date = None

        pass

    def execute(self):

        for date in self.data.outOfSampleDates:
            
            if date == self.data.outOfSampleDates[0]:
                self.portfolioValue = self.data.parameters.investment
                self.performance[date] = self.portfolioValue
                print(f'{date}: {self.portfolioValue}')

            else:

                self.portfolioValue = self.get_portfolio_value(date,rebalance)
                self.performance[date] = self.portfolioValue
                print(f'{date}: {self.portfolioValue}')

            if date in self.data.rebalanceDates:
                
                print('******** Rebalance ********\n')

                self.last_rebalance_date = date

                rebalance = Rebalance(self.data, date)

                # print(rebalance.inSamplePrices)
                
                # print(rebalance.outOfSamplePrices)

                # print(rebalance.rebalance_prices)

                plugin = rebalance.load_plugin(class_name=self.data.parameters.plugin)

                self.weights[date] = plugin.get_weights()

                self.capital_per_asset[date] = {asset: self.weights[date][asset]*self.portfolioValue for asset in rebalance.assets}

                self.shares_per_asset[date] = {asset: self.capital_per_asset[date][asset]/rebalance.rebalance_prices.loc[date][asset] for asset in rebalance.assets}
                
        pass
    
    def get_portfolio_value(self, date, rebalance):
        
        pv = 0

        for asset in rebalance.assets:

            pv += self.shares_per_asset[self.last_rebalance_date][asset]*rebalance.rebalance_prices.loc[date][asset]
        
        print(f'{date}: {pv}')

        return pv 

                



    