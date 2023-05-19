import pandas as pd
import settings as s
import matplotlib.pyplot as plt
import numpy as np
import RayleighTaylor as rt
import matplotlib.dates as dates
from labels import Labels
from utils import save_but_not_show
import os

def plot_gamma_climatology(
        infile, wind = "mer", drift = "vzp", recom = True
        ):
    
    df = rt.load_process(infile, apex = 300)
    df = df.loc[df["hem"] == "north"]
    
    df["gamma"] = rt.all_effects(
            df, 
            wind = wind,
            drift = drift,
            sign_wd = 1, 
            recom = recom)
    
    df = df[~df.index.duplicated()]
    df = df.resample("20min").asfreq()
    
    df["date"] = df.index.date
    df["time"] = df.index.hour + df.index.minute / 60
     
    df1 = pd.pivot_table(df, 
                         columns = "date", 
                         index = "time", 
                         values = "gamma")#.interpolate()
        
    fig, ax = plt.subplots(
        figsize = (12, 4), 
        dpi = 300)
    vmax = np.nanmax(df1.values)
    vmin = np.nanmin(df1.values)
    cs = plt.contourf(df1.columns , 
                     df1.index, 
                     df1.values*1e4, 30, 
                     cmap = "rainbow",)
    
    ticks = np.linspace(vmin, vmax, 10)
    
    s.colorbar_setting(cs, ax, #ticks, 
                       label = "$\gamma_{RT} ~(\\times 10^{-4}~s^{-1})$")
    
    ax.set(ylabel = "Hora (UT)", 
           yticks = np.arange(0, 26, 2),
           xlabel = "Meses")
    
    
    major_formatter = dates.DateFormatter("%b")
    major_locator = dates.MonthLocator(interval = 1)
    
    ax.xaxis.set_major_locator(major_locator)
    ax.xaxis.set_major_formatter(major_formatter)
    
    wd = Labels().infos[wind]['name'].lower()
    
    if recom:
        w = "com"
    else:
        w = "sem"
    
    eq = rt.EquationsFT()
    eq = eq.complete(
        wind_sign = 1, 
        recom = recom
        )
    
    ax.set(title = f"{eq} \n Efeitos: vento {wd}, {drift} e {w} recombinação")
    return fig

def save_plots():
    infile = "database/RayleighTaylor/reduced/300.txt"
    
    for wind in ["zon", "zon_ef", "mer", "mer_ef"]:
        for rc in [True, False]:
            for dr in ["vzp", "vz"]:
                fig = plot_gamma_climatology(
                    infile, wind = wind, drift = dr, recom = rc)
                
                if rc:
                    w = "com"
                else:
                    w = "sem"
                
                fname = f"{wind}_{dr}_{w}_recom.png"
                save_it = os.path.join("D:\\plots\\climatology\\", 
                                       fname)
                
                print("saving...", fname)
                save_but_not_show(fig, save_it)
