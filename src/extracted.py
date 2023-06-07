import os
import ionosphere as io
import datetime as dt
import pandas as pd
import atmosphere as atm


infile = "database/RayleighTaylor/process/3.txt"


ds = pd.read_csv(infile, index_col = 0)
ds