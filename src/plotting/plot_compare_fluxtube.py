import matplotlib.pyplot as plt
from common import plot_roti, plot_terminators, load_by_alt_time
import RayleighTaylor as rt
import pandas as pd
import datetime as dt
import numpy as np
import digisonde as dg





def set_data(dn, hem = 'south', alt = 300):
    infile = 'wind_perp.txt'
    
    df = pd.read_csv(infile, index_col=0)
    
    df = df.loc[(df.index ==  alt) & 
                (df['hem'] == hem)]
    
    df = df.set_index('dn')


    df.index = pd.to_datetime(df.index)
    
    delta = dt.timedelta(seconds = 43200)

    return df.loc[(df.index >= dn) & (df.index <= dn + delta)]


vz = dg.add_vzp()

dn = dt.datetime(2013, 3, 16, 20, 0)

df = set_data(dn, hem = 'south')


vzp = vz[vz.index == dn.date()]["vzp"].item()

base = df["ratio"] * df["K"]

gammas = [base * (df["ge"] / df["nui"]), 
         base * (- df['mer_ef']),
         base * (vzp)]



fig, ax = plt.subplots()

for gamma in gammas:
    ax.plot(gamma * 1e4)