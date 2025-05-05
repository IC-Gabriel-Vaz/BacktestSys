import pandas as pd







class Parameters:

    def __init__(self, _app, _date1, _date2, _rebalance, _inSample):
        self.app = _app
        self.date1 = _date1
        self.date2 = _date2
        self.rebalance = _rebalance
        self.in_sample = _inSample

    def __repr__(self):
        return (f"Parameters(app={self.app}, date1={self.date1}, date2={self.date2}, "
                f"rebalance={self.rebalance}, in_sample={self.in_sample})")
