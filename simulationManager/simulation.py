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

        pass

    def execute(self):

        for date in self.data.outOfSampleDates:
            
            if date == self.data.outOfSampleDates[0]:
                self.portfolioValue = self.data.parameters.investment
                print(f'{date}: {self.portfolioValue}')

            else:

                self.portfolioValue = self.get_portfolio_value(date,rebalance)
                print(f'{date}: {self.portfolioValue}')

            if date in self.data.rebalanceDates:
                
                print('******** Rebalance ********\n')

                rebalance = Rebalance(self.data, date)

                plugin = rebalance.load_plugin(class_name=self.data.parameters.plugin)

                weights = plugin.get_weights()

                capital_per_asset = {asset: weights[asset]*self.data.parameters.investment for asset in rebalance.assets}
                       
        pass
    
    def get_portfolio_value(self, date, rebalance):
        
        
        return pv

                



    