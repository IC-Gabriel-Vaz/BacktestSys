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

        self.simulationPrices = self.get_simulation_prices()

        self.alldates, self.inSampleDates, self.outOfSampleDates = self.get_simulation_dates()

        self.rebalanceDates = self.get_rebalance_dates()

        pass

    def get_dataBase_path(self):
        
        config_dir = Path(__file__).resolve().parent.parent / 'config'
        file_path = config_dir / 'marketDataBase.txt'
        
        with open(file_path,'r', encoding='utf-8') as file:
            
            dbPath = file.read()
            
        return dbPath 
    
    def get_simulation_prices(self):

        conn = sqlite3.connect(self.dbPath)

        try:
            query_dates = f"""
                SELECT DISTINCT ap.date
                FROM AssetPrice ap
                JOIN ApplicationAsset aa ON ap.asset = aa.asset
                WHERE aa.app = '{self.parameters.app}' AND ap.date < '{self.parameters.date1}'
                ORDER BY ap.date DESC
                LIMIT {self.parameters.inSample}
            """
            date_df = pd.read_sql_query(query_dates, conn)

            if not date_df.empty:
                
                start_date = date_df['date'].min()
            else:
                start_date = self.parameters.date1

            query = f"""
                SELECT 
                    ap.asset,
                    ap.date,
                    ap.close
                FROM 
                    AssetPrice ap
                JOIN 
                    ApplicationAsset aa ON ap.asset = aa.asset
                WHERE 
                    aa.app = '{self.parameters.app}' AND
                    ap.date BETWEEN '{start_date}' AND '{self.parameters.date2}'
                ORDER BY 
                    ap.asset, ap.date;
            """
            df = pd.read_sql_query(query, conn)

            df_pivot = df.pivot(index='date', columns='asset', values='close')
            df_pivot.index = pd.to_datetime(df_pivot.index)

            return df_pivot

        finally:
            conn.close()

    def get_simulation_returns(self,prices):
        
        returns = prices.pct_change().iloc[1:]

        return returns
    
    def get_simulation_dates(self):

        allDates = list(self.simulationPrices.index)
        inSampleDates = list(self.simulationPrices.index[:self.parameters.inSample])
        outOfSampleDates = list(self.simulationPrices.index[self.parameters.inSample:])

        # print(inSampleDates)
        # print(outOfSampleDates)

        return allDates, inSampleDates, outOfSampleDates
    
    def get_rebalance_dates(self):

        rebalanceDates = self.simulationPrices.index[self.parameters.inSample::self.parameters.rebalance]
        
        return rebalanceDates
    

    def print_dates(self):

        print(f'In Sample Dates (First {self.parameters.inSample} dates) \n')
        print(self.inSampleDates)

        print(f'Out of Sample Dates \n')
        print(self.outOfSampleDates)

        print(self.rebalanceDates)

        pass

    def print_data(self):

        print(f"Prices Data Frame: \n {self.simulationPrices}")

        pass

