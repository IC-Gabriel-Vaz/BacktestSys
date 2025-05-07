import pandas as pd
import numpy as np





class Simulation:

    def __init__(self, _parameters, _data):
        
        self.parameters = _parameters
        self.data = _data

        return None
    
    def get_rebalance_data(self, date):

        if date not in self.data.rebalanceDates:

            print(f'{date} is not a rebalance date: ')

        else:

            