import matplotlib.pyplot as plt
from common import plot_roti, plot_terminators
import RayleighTaylor as rt
import pandas as pd
import datetime as dt
import settings as s
import os

infile = "database/MSIS/sites/"

files = os.listdir(infile)


out = []
for filename in files:
    
    
    out.append(pd.read_csv(infile + filename, index_col = 0))
    
df = pd.concat(out)
df.index = pd.to_datetime(df.index)

#for site in ["saa", 'car', 'caj']:
site = 'car'   
ds = df[df['site'] == site]
ds['O'].plot()
