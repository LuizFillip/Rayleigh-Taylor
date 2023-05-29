import matplotlib.pyplot as plt
from common import plot_roti, plot_terminators
import RayleighTaylor as rt
import pandas as pd
import datetime as dt
import numpy as np



def load_by_alt_time(infile, dn):
    
    df = pd.read_csv(infile, index_col = 0)
    df.index = pd.to_datetime(df.index)
    
    delta = dt.timedelta(seconds = 43200)

    return df.loc[(df.index >= dn) & (df.index <= dn + delta)]

def plot_gamma(
        ax, df, alt, 
        sign = 1,
        wind = "zon"
        ):

    df = df[df["alt"] == alt]

    gamma = ( sign * df[wind] + 
             (9.81 / df["nui"])) * df["L"] 
    
    ax.plot(gamma *1e4, label = f"{alt} km")
    
    
    ax.axhline(0, linestyle = "--")
    
    
    return ax




def plot_local_winds_effects(df,  sign = 1):
   
    
    fig, ax = plt.subplots(
                figsize = (14, 10),
                sharex = True,
                sharey = "row",
                nrows = 3,
                ncols = 2,
                dpi = 300
                )
    
    plt.subplots_adjust(
        hspace = 0.05, 
        wspace = 0.05
                )
    
    lbs = rt.EquationsRT()
    
    for row, wd in enumerate(["zon", "mer"]):
        
        ax[row, 0].set(ylabel = lbs.label,
                       ylim = [-30, 30])
        
        plot_roti(ax[2, row], 
                  df, 
                  hour_locator = 1,
                  station = "ceeu")
        
        ax[0, row].set(title = lbs.complete(
            sign = sign, rc = False)
            )
        
        for alt in np.arange(250, 400, 50):
            
            if wd == "zon":
                name = "Zonal"

            else:
                name = "Meridional"
                
            y = 0.1
            x = 0.6
            ax[row, 0].text(x, y , 
                            name + " geográfico", 
                            transform = ax[row, 0].transAxes)
                
            ax[row, 1].text(x, y, 
                            name + " efetivo", 
                            transform = ax[row, 1].transAxes)
            
            plot_gamma(ax[row, 0], df, alt, sign = sign, wind = wd)
            plot_gamma(ax[row, 1], df, alt, sign = sign, wind = wd + "_ef")

    
    ax[0, 0].legend(
        bbox_to_anchor = (.5, 1.1), 
        ncol = 3, 
        loc = "lower left", 
        title = "Altitudes de $\gamma_{RT}$"
        )
    
    
    ax[2, 1].set(ylabel = "")
    for ax in ax.flat:    
        plot_terminators(ax, df)
        
  
    
    return fig

from utils import  save_but_not_show

def save_plots():

    save_in = "D:\\plots2\\temp_0317\\"
    
    for dn in [dt.datetime(2013, 3, 16, 20), 
               dt.datetime(2013, 3, 17, 20), 
               dt.datetime(2013, 3, 18, 20)]:
        
        for sign in [1, -1]:
            
            for site in ["car", "caj"]:
                infile = f"gamma_1620_{site}.txt"
                
                df = load_by_alt_time(infile, dn)
                fig = plot_local_winds_effects(df, sign = sign)
                
                if "car" in infile:
                    fig.suptitle("Ventos observados em Cariri", y = 1.)
                else:
                    fig.suptitle("Ventos observados em Cajazeiras", y = 1.)
                
                if sign == 1:
                    s = "positive"
                else:
                    s = "negative"
                    
                FigureName = f"{dn.strftime('%Y%m%d')}_{s}_{site}.png"
                
                print("saving...", dn)
                
                save_but_not_show(
                       fig, 
                       save_in + FigureName,
                       dpi = 300
                       )