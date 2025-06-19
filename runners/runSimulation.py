import pandas as pd
import numpy as np

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

