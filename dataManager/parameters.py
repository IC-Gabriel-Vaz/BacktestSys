import pandas as pd
from datetime import datetime , timedelta

class Parameters:

    def __init__(self,txt):
        self.app =  txt['app']
        # self.date1 = datetime.strptime(txt['date1'], "%Y-%m-%d")
        # self.date2 = datetime.strptime(txt['date2'], "%Y-%m-%d")
        self.date1 = txt['date1']
        self.date2 = txt['date2']
        self.inSample = int(txt['inSample'])
        self.rebalance = int(txt['rebalance'])
        self.investment = float(txt['investment'])
        self.transactionCosts  = float(txt['transactionCosts'])
        self.plugin = txt['plugin']

    def __repr__(self):
        return (f"Parameters: \n app={self.app},\n date1 = {self.date1}, date2 = {self.date2}, \n "
                f"Rebalance Frequency = {self.rebalance}, \n In sample period = {self.inSample},\n "
                f"Investment={self.investment}, \n "
                f"Transaction Costs = {self.transactionCosts}")
