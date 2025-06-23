import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from datetime import datetime , timedelta
from pathlib import Path


import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

config_dir = Path(__file__).resolve().parent.parent / 'config'
file_path = config_dir / 'parameters.txt'

from scripts.readTxt import read_txt

from dataManager.parameters import Parameters
from dataManager.data import Data

from simulationManager.simulation import Simulation


if __name__ == '__main__':

    txt = read_txt(file_path)

    parameters = Parameters(txt)
    
    data = Data(parameters)

    if parameters.transactionCosts == 0:


        simulation = Simulation(data)

        simulation.execute()

        performance_series = pd.Series(simulation.performance)

        performance_series.index = pd.to_datetime(performance_series.index)
        performance_series = performance_series.sort_index()

        plt.figure(figsize=(12, 6))
        plt.plot(performance_series.index, performance_series.values, label='Performance')
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.title('Simulation Performance Over Time')
        plt.grid(True)
        plt.legend()

        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.show()



