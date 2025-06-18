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

from scripts.backtest import backtest as bt

from dataManage.parameters import Parameters
from dataManage.data import Data


if __name__ == '__main__':

    txt = read_txt(file_path)

    parameters = Parameters(txt)
    
    data = Data(parameters)

    