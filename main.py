import pandas as pd
import numpy as np 
from build import paths as p 
import matplotlib.pyplot as plt
import setup as s

infile = p('RayleighTaylor').files

df = pd.read_csv(infile, index_col = 0)



def get_max(df, date, alts = (250, 350)):
   
    cond_alt = ((df.index >= alts[0]) &
                (df.index <= alts[1]))
    
    cond_time = (df["date"] == date)
    
    return df.loc[cond_alt & cond_time, "g"].max()


def run(df):
    dates = np.unique(df.date)
    
    out = []
    for date in dates:
        out.append(get_max(df, date))
        
    return pd.to_datetime(dates), np.array(out, dtype = np.float64)
    

fig, ax = plt.subplots(figsize = (8, 5), 
                       sharex = True)
dates, out = run(df)  

ax.plot(dates, out * 1.0e3, lw = 2)

ax.axhline(0, color = "r")
s.format_axes_date(ax)

ax.set(ylabel = "$\gamma_{RT} ~(10^{-3}~s^{-1})$",
       xlabel = "Meses", 
       title = "São Luis - 2013")