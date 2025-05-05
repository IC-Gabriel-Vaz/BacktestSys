import pandas as pd
from datetime import timedelta
import sqlite3
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from adm.admin import Admin

class Data:

    def __init__(self,_parameters):
        
        self.parameters = _parameters

        print(self.parameters)
        self.dbPath = self.get_dataBase_path()

        
        print(f"[DEBUG] Caminho do banco de dados: {self.dbPath}")
        print(f"[DEBUG] Arquivo existe? {os.path.exists(self.dbPath)}")

        self.simulation_prices = self.get_simulation_prices()

        print(self.simulation_prices)

        pass

    def get_dataBase_path(self):
        
        config_dir = Path(__file__).resolve().parent.parent / 'config'
        file_path = config_dir / 'marketDataBase.txt'
        
        with open(file_path,'r', encoding='utf-8') as file:
            
            dbPath = file.read()
            # print(dbPath)
        return dbPath 
    
    def get_simulation_prices(self):
        
        conn = sqlite3.connect(self.dbPath)

        try:
            # SQL Query
            query = f'''
            SELECT ap.date, aa.asset, ap.close
            FROM AssetPrice ap
            JOIN ApplicationAsset aa ON ap.asset = aa.asset
            WHERE aa.app = '{self.parameters.app}'
            '''

            df = pd.read_sql_query(query, conn)

            print(df)
            conn.close()
        except Exception as e:
            print('The was an error with the market data database')
            print(f'Erro: {e}')
            conn.close()
        return None
    
    def get_simulation_returns():

        return None
    
    def get_simulation_dates():

        return None
    