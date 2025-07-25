from plugin import Plugin

import pyomo as pyo

class BetaModel(Plugin):
    
    def __init__(self, rebalance):
        self.rebalance = rebalance
        

    def get_long_and_short_assets(self):

        windows = [21, 63, 252]

        long_assets = []
        short_assets = []

        prices = self.rebalance.data.simulationPrices.loc[:self.rebalance.date]
        prices = prices[self.rebalance.assets]

        for window in windows:

            returns = prices.pct_change(periods=window).iloc[-1]

            primeiro_decil = returns.sort_values().iloc[:int(0.1 * len(returns))]
            long_assets.extend(primeiro_decil.index)

            ultimo_decil = returns.sort_values(ascending=False).iloc[:int(0.1 * len(returns))]
            short_assets.extend(ultimo_decil.index)


        long_assets = list(set(long_assets))
        short_assets = list(set(short_assets))

        return long_assets, short_assets



    def get_weights(self):

        self.get_long_and_short_assets()

        return None