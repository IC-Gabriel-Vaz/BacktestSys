import pandas as pd
import numpy as np

from datetime import datetime , timedelta
from pathlib import Path

config_dir = Path(__file__).resolve().parent.parent / 'config'

if __name__ == '__main__':

    with open(config_dir / 'parameters.txt', 'r') as file:
        parameters = file.read()
        print(parameters)