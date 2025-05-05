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

        return Path(dbPath) 
    
    def get_simulation_prices(self):

        conn = sqlite3.connect(self.dbPath)

        # SQL Query
        query = """
            SELECT 
                ap.asset,
                ap.date,
                ap.adjClose
            FROM 
                AssetPrice ap
            JOIN 
                ApplicationAsset aa ON ap.asset = aa.asset
            WHERE 
                aa.app = ? AND
                ap.date BETWEEN ? AND ?
            ORDER BY 
                ap.asset, ap.date;
        """

        df = pd.read_sql_query(query, conn, params=(app, date1, date2))

        print(df)
        conn.close()
        return None
    
    def get_simulation_returns():

        return None
    
    def get_simulation_dates():

        return None
    