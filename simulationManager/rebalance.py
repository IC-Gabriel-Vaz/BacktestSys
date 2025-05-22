import importlib.util
import os
import sys

from datetime import timedelta



class Rebalance:

    def __init__(self, _data, _date):
        
        self. data = _data

        self.date = _date
        
        self.prices = self.get_rebalance_prices(_data)

        self.returns = self.get_rebalance_returns(_data)

        self.assets = list(self.returns.columns)

        pass


    def get_rebalance_prices(self,data):

        prices = data.simulationPrices.loc[self.date - timedelta(data.parameters.inSample): self.date]
        
        return prices
    
    def get_rebalance_returns(self,data, maxNan = 0.2):

        prices = self.prices.loc[:, data.simulationPrices.isnull().mean() <= maxNan]
        
        colunas_removidas = data.simulationPrices.shape[1] - prices.shape[1]

        # print(f"{colunas_removidas} colunas removidas.")

        prices = prices.ffill()
        prices = prices.bfill()

        returns = prices.pct_change(fill_method = None).dropna()

        return returns
    
    def load_plugin(class_name: str, config_file: str = 'config/plugins.txt'):
        
        with open(config_file, 'r') as f:
            plugin_dir = f.read().strip()

        if not os.path.isdir(plugin_dir):
            raise FileNotFoundError(f"Diretório de plugins não encontrado: {plugin_dir}")

        sys.path.insert(0, plugin_dir)

        for file in os.listdir(plugin_dir):
            if file.endswith('.py'):
                module_name = file[:-3]
                try:
                    module = importlib.import_module(module_name)
                    plugin_class = getattr(module, class_name, None)
                    if plugin_class:
                        return plugin_class()
                except Exception as e:
                    print(f"Erro ao importar {file}: {e}")

        raise ImportError(f"Classe {class_name} não encontrada em {plugin_dir}")


