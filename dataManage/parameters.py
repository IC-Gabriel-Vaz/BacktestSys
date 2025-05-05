import pandas as pd
from datetime import datetime , timedelta

class Parameters:

    def __init__(self,txt):
        self.app =  txt['app']
        self.date1 = datetime.strptime(txt['date1'], "%Y%m%d")
        self.date2 = datetime.strptime(txt['date2'], "%Y%m%d")
        self.inSample = int(txt['inSample'])
        self.rebalance = int(txt['rebalance'])
        self.investment = int(txt['investment'])
        self.transactionCosts  = float(txt['transactionCosts'])

    def __repr__(self):
        return (f"Parameters(app={self.app}, date1={self.date1}, date2={self.date2}, "
                f"rebalance={self.rebalance}, in_sample={self.inSample})")
