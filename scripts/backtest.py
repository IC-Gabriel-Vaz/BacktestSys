import pandas as pd
import numpy as np


import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from simulationManager.simulation import Simulation
from simulationManager.results import Results

def backtest(parameters,data):

    simulation = Simulation(parameters, data)

    results = Results()

    
    for date in data.outOfSampleDates:
        
        print('****** Simulation ****** \n')
        
        results.portfolioValue = parameters.investment

        
    return None