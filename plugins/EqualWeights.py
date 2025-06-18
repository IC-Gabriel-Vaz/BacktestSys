from plugin import Plugin



class EqualWeights(Plugin):
    
    def __init__(self, rebalance):
        self.rebalance = rebalance

    def get_weights(self):
        return {asset: 1/len(self.rebalance.assets) for asset in self.rebalance.assets}
