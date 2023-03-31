import pandas as pd
import setup as s
import matplotlib.pyplot as plt
import numpy as np


infile = "database/growthRates/reco_and_vp_alltimes.txt"

def GammaRTContourf(infile):
    
    df = pd.read_csv(infile, index_col = 0)
    
    df.index = pd.to_datetime(df.index)
    
    df["date"] = df.index.date
    df["time"] = df.index.hour + df.index.minute / 60
    
    df1 = pd.pivot_table(df, 
                         columns = "date", 
                         index = "time", 
                         values = "gVp_max")
    
    fig, ax = plt.subplots(figsize = (10, 8))
    
    cs = plt.contourf(df1.columns , 
                     df1.index, 
                     df1.values*1e3, 50, 
                     cmap = "Blues")
    
    plt.colorbar(cs)
    
    ax.set(ylabel = "Hora (UT)", 
           yticks = np.arange(0, 26, 2),
           xlabel = "Dia do ano")
    
    s.format_axes_date(ax)