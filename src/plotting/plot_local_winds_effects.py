import matplotlib.pyplot as plt
from common import plot_roti, plot_terminators
import RayleighTaylor as rt
import pandas as pd
import datetime as dt
import numpy as np



def load_by_alt_time(dn):
    
    df = pd.read_csv("gamma_parameters.txt", index_col = 0)
    df.index = pd.to_datetime(df.index)
    
    delta = dt.timedelta(seconds = 43200)

    return df.loc[(df.index >= dn) & (df.index <= dn + delta)]

def plot_gamma(
        ax, df, alt, 
        sign = 1,
        wind = "U"
        ):
    
    if wind == "U":
        name = "Zonal"
    else:
        name = "Meridional"
        
    lbs = rt.EquationsRT()

    df = df[df["alt"] == alt]

    gamma = (df["vz"] + sign * df[wind] + 
             (9.81 / df["nui"])) * df["L"] 
    
    ax.plot(gamma *1e4, label = f"{alt} km")
    
    ax.text(0.05, 0.8, name, transform = ax.transAxes)
    plot_terminators(ax, df)
    ax.axhline(0, linestyle = "--")
    ax.set(ylabel = lbs.label, ylim = [-30, 30])
    ax.legend(ncol = 3, loc = "lower left")
    return ax




def plot_local_winds_effects(dn):
    df = load_by_alt_time(dn)
    
    fig, ax = plt.subplots(
                figsize = (10, 8),
                sharex = True,
                nrows = 3,
                dpi = 300
                )
    
    plt.subplots_adjust(hspace = 0.05)
    
    lbs = rt.EquationsRT()
    
    sign = -1
    ax[0].set(title = lbs.complete(sign = sign, rc = False))
    
    for alt in np.arange(250, 400, 50):
        plot_gamma(ax[0], df, alt, sign = sign, wind = "U")
        plot_gamma(ax[1], df, alt, sign = sign, wind = "V")
    
    
    plot_roti(ax[2], df, hour_locator = 1, station = "ceeu")
    
    return fig

dn = dt.datetime(2013, 3, 17, 20)

fig = plot_local_winds_effects(dn)