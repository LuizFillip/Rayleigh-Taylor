import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import plotConfig
import matplotlib.dates as dates

infile = "database/growthRates/reco_and_vp_alltimes.txt"


df = pd.read_csv(infile, index_col = 0)

df.index = pd.to_datetime(df.index)

df["date"] = df.index.date
df["time"] = df.index.hour + df.index.minute / 60

df1 = pd.pivot_table(df, 
                     columns = "date", 
                     index = "time", 
                     values = "gVp_max")




fig, ax = plt.subplots(figsize = (25, 10))

cs = plt.contourf(df1.columns , 
                 df1.index, 
                 df1.values*1e3, 50, 
                 cmap = "Blues")

plt.colorbar(cs)
ax.set(ylabel = "Hora (UT)", 
       yticks = np.arange(0, 26, 2),
       xlabel = "Dia do ano")

    
ax.xaxis.set_major_formatter(dates.DateFormatter('%b'))
ax.xaxis.set_major_locator(dates.MonthLocator(interval = 1))