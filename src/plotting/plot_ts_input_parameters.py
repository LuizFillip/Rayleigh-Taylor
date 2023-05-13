# ax[0, 0].plot(df["ratio"])
# ax[1, 0].plot(df["nui"])
# ax[2, 0].plot(df["N"])
# ax[3, 0].plot(df["K"])

def plot_winds(ax, df):
    ax.plot(df[['zon_ef', "zon"]])
    
    ax.set(ylim = [-150, 150], 
           ylabel = "Velocidade\n zonal (m/s)")
    
    ax.legend(["Geográfico", "Efetivo"], 
                 loc = "upper right",
                 ncol = 2)

import pandas as pd

infile = "database/RayleighTaylor/process/12.txt"
df = pd.read_csv(infile, index_col = 0)

df