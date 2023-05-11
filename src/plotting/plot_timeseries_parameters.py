import matplotlib.pyplot as plt
import datetime as dt
import settings as s
import numpy as np
import pandas as pd
import os
from results import plot_roti_maximus


def plot_terminators(ax, dn):

    ax[0].text(0.03, 1.03, "0 km", 
               transform = ax[0].transAxes)
    ax[0].text(0.13, 1.03, "300 km", 
               transform = ax[0].transAxes)
    
    for ax in ax.flat:
        
        sunset, dusk = get_dusk(dn.date())
        args = dict(lw = 2,  color = "k")
        ax.axvline(sunset, **args)
        ax.axvline(dusk, linestyle = "--", **args)
        
        ax.grid()


def plot_gamma_part(
        ax,
        df
        ):

    df = df * 1e4
    ax.plot(df.index, df)
    
    gmax = 10
    ax.set(ylim = [-gmax, gmax], 
           ylabel = "$\gamma_{RT} ~ (10^{-4} ~s^{-1})$")
    
    ax.axhline(0, 
               color = "r", 
               linestyle = "--")
    
    
    ax.legend(["$U_{ef}^N$", "$U_{ef}^S$", 
               "$U_{y}^N$", "$U_{y}^S$"], 
              ncols = 2, loc = "upper right")
    
    name = "$\gamma_{FT} = \\frac{\Sigma_P^F}{\Sigma_P^E + \Sigma_P^F}(-U_L^P + \\frac{g_e}{\\nu_{eff}^{F}})K^F$"    
    
    ax.text(0.02, 0.85, name, transform = ax.transAxes)      



def plot_timeseries_parameters():
    
    ...
    

def set_data(infile = "02_11.txt", alt = 300, month = 2):
    df = pd.read_csv(infile, index_col=0)
    
    df["dn"] = pd.to_datetime(df["dn"])
    
    df = df.loc[(df.index == alt) ]
    
    df = df.set_index("dn")
    
    df["nui"] = 9.81 / df["nui"]

    return df.loc[df.index.month == month]


fig, ax = plt.subplots(
    figsize = (12, 6), 
    sharex = True,
    nrows = 4, 
    ncols = 2,
    dpi = 300
    )


df = set_data(alt = 250)

df = df[df.index < dt.datetime(2013, 2, 3, 0)]

new_index = pd.date_range(
    df.index[0] - dt.timedelta(minutes = 10), 
    df.index[-1], freq = "10min"
    )

df = df.reindex(new_index).interpolate()

s.set_mi_ma_axis(ax[3, 0])
s.set_mi_ma_axis(ax[3, 1])

ax[0, 0].plot(df["ratio"])
ax[1, 0].plot(df["nui"])
ax[2, 0].plot(df["N"])
ax[3, 0].plot(df["K"])

infile = "database/Results/maximus/2013.txt"

#plot_roti_maximus(ax[1], infile, df.index[0], delta_hours = df.index[-1])

ax[0, 1].plot(df[['zon_ef', "zon"]])
ax[1, 1].plot(df['gamma_g'])
ax[2, 1].plot(df[['gamma_zon', 'gamma_zon_ef']])


