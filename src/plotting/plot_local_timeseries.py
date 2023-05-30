import matplotlib.pyplot as plt
from common import plot_roti, plot_terminators
import RayleighTaylor as rt
import pandas as pd
import datetime as dt
import settings as s


def plot_local_timeseries(df, alt = 250, station = "salu"):
        
    

    return fig

# dn = dt.datetime(2013, 9, 19, 20)
infile = "database/FluxTube/temp.txt"

df = pd.read_csv(infile, index_col=0)

df["dn"] = pd.to_datetime(df["dn"])


ts = pd.pivot_table(
    df, 
    columns = "dn", 
    index = df.index, 
    values = "ratio"
    )

fig, ax = plt.subplots(
            sharex = True,
            dpi = 300
            )

plt.subplots_adjust(hspace = 0.3)


df = df.loc[df.index == 300]

ax.plot(df["dn"], df["ratio"])

s.format_time_axes(ax)
#for ax in ax.flat:
plot_terminators(ax, df.set_index("dn"))
    
    