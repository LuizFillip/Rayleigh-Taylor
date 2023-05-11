import matplotlib.pyplot as plt
import datetime as dt
import settings as s
import numpy as np
import pandas as pd
import os
from results import plot_roti_maximus
from GEO import dawn_dusk






def date_under_axis(ax, dn, delta = 3.5):
    delta = dt.timedelta(hours = delta)
    
    text_date = dn.strftime("%d/%m/%Y")

    ax.text(dn - delta, -1.5, text_date, 
            transform = ax.transData)
    
def midnight_points(df):
    return df.loc[df.index.time == dt.time(0, 0)].index
    
    

def set_data(infile = "02_11_north.txt", alt = 300, month = 2):
    df = pd.read_csv(infile, index_col=0)
    
    df["dn"] = pd.to_datetime(df["dn"])
    
    df = df.loc[(df.index == alt) ]
    
    df = df.set_index("dn")
    
    df["nui"] = 9.81 / df["nui"]

    return df.loc[df.index.month == month]

df = set_data(alt = 300)

df = df[df.index <= dt.datetime(2013, 2, 3, 0)]

def plot_timeseries_parameters(df):
    fig, ax = plt.subplots(
        figsize = (8, 8), 
        sharex = True,
        nrows = 4, 
        dpi = 300
        )
    
    plt.subplots_adjust(hspace= 0.1)
    
    infile = "database/Results/maximus/2013.txt"
    
    ax[0].plot(df[['zon_ef', "zon"]])
    
    ax[0].set(ylim = [-150, 150], 
              title = "Norte",
              ylabel = "Velocidade\n zonal (m/s)")
    
    ax[0].legend(["Geográfico", "Efetivo"], 
                 loc = "upper right",
                 ncol = 2)
    
    ax[1].plot(df['gamma_g'] * 1e4)
    
    ax[1].set(ylim = [-17, 17], 
              ylabel = "$\gamma_{FT} ~(\\times 10^{-4}~s^{-1})$"
              )
    
    name = "$\gamma_{FT} = \\frac{\Sigma_P^F}{\Sigma_P^E + \Sigma_P^F}(\\frac{g_e}{\\nu_{eff}^{F}})K^F$"
    
    ax[1].text(0.05, 0.8, name, transform = ax[1].transAxes)
    
    
    ax[2].plot(df[['gamma_zon', 'gamma_zon_ef']] * 1e4)
    
    ax[2].legend(["Geográfico", "Efetivo"], 
                 loc = "upper right",
                 ncol = 2)
    
    name = "$\gamma_{FT} = \\frac{\Sigma_P^F}{\Sigma_P^E + \Sigma_P^F}(-U_L^P + \\frac{g_e}{\\nu_{eff}^{F}})K^F$"
    
    ax[2].text(0.05, 0.8, name, transform = ax[2].transAxes)
    
    ax[2].set(ylim = [-17, 17], 
              ylabel = "$\gamma_{FT} ~(\\times 10^{-4}~s^{-1})$"
              )
    
    
    plot_roti_maximus(
        ax[3], infile, 
        start = df.index[0], 
        delta_hours = df.index[-1]
        )
    
    s.format_axes_date(
        ax[3], time_scale = "hour", interval = 4
        )

    for dn in midnight_points(df):
        
        date_under_axis(ax[3], dn)
    
    ax[3].set_xlabel("Hora universal", 
                     rotation = 0, 
                     labelpad = 25)
    
    
    
    for ax in ax.flat:
        for dn in midnight_points(df)[:-1]:
            colors = ["r", "k"]
            for i, line in enumerate(dawn_dusk(dn)):
                ax.axvline(line, linestyle = "--", color = colors[i])
    
    
    plt.show()