import pandas as pd
import datetime as dt
import sqlite3
import os
import sys
from pathlib import Path
import importlib

sys.path.append(str(Path(__file__).resolve().parent.parent))


class Rebalance:

    def __init__(self,_data,_date):
        
        self.data = _data
        self.date = _date
        
        self.rebalance_prices = self.get_rebalance_prices()

        self.inSamplePrices = self.get_in_sample_prices()

        self.outOfSamplePrices = self.get_out_of_sample_prices()
        
        pass

    def load_plugin(self,class_name:str, config_file: str = None):

        if config_file is None:
            current_dir = os.path.dirname(__file__)
            config_file = os.path.join(current_dir, '..', 'config', 'plugins.txt')
            config_file = os.path.abspath(config_file) 

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
                        return plugin_class(self)
                except Exception as e:
                    print(f"Erro ao importar {file}: {e}")

        raise ImportError(f"Classe {class_name} não encontrada em {plugin_dir}")


    def get_rebalance_prices(self):

        index = self.data.simulationPrices.index.sort_values()

        def get_valid_date(target_date):
            return index[index <= target_date].max() if not index[index <= target_date].empty else index[0]

        start_date = get_valid_date(self.date - dt.timedelta(self.data.parameters.inSample))
        end_date = get_valid_date(self.date + dt.timedelta(self.data.parameters.rebalance))

        df = self.data.simulationPrices.loc[start_date:end_date]

        return df







