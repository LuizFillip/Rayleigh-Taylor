import pandas as pd
import numpy as np 
import os 
import datetime as dt
import matplotlib.pyplot as plt
import settings as s

def get_max(df, date, alts = (250, 350)):
   
    cond_alt = ((df.index >= alts[0]) &
                (df.index <= alts[1]))
    
    cond_time = (df["date"] == date)
    
    return df.loc[cond_alt & cond_time, "g"].max()

        
def set_data(infile = "02_11_north.txt", alt = 300, month = 2):
    
    df = pd.read_csv(infile, index_col=0)
    
    df["dn"] = pd.to_datetime(df["dn"])
    
    df = df.loc[(df.index == alt) ]
    
    df = df.set_index("dn")
    
    df["nui"] = 9.81 / df["nui"]

    return df.loc[df.index.month == month]


def maximus():
    infile = "02_11_north.txt"
    df = pd.read_csv(infile, index_col=0)
    dat = {
           "gamma_zon" : [], 
           "gamma_zon_ef" : [], 
           "gamma_g" : [], 
           "z_gamma_zon": [], 
           "z_gamma_zon_ef" : [], 
           "z_gamma_g" : [], 
           }
    times  = df["dn"].unique()
    for time in times:
    
        ds = df.loc[df["dn"] == time]
        
        for col in ['gamma_g', 'gamma_zon', 'gamma_zon_ef']:
            dat[col].append(ds[col].max())
            dat[f"z_{col}"].append(ds[col].idxmax())
            
    
    ts = pd.DataFrame(dat, index = times)
    
    ts.index = pd.to_datetime(ts.index)
    ts = ts.loc[ts.index.month == 2]
   
    
    
    fig, ax = plt.subplots(
        figsize = (12, 4), 
        
                           dpi = 300)
    
    g = "gamma_g"
    img = plt.scatter(ts.index, 
                      ts[f"z_{g}"], 
                      c = ts[g]*1e4)
    
    
    cb = plt.colorbar(img)
    cb.set_label("$\gamma_{FT} ~(\\times 10^{-4}~s^{-1})$")
    
    
    s.format_axes_date(
        ax, time_scale = "hour", interval = 4
        )
    
    
    ax.set(title = "gravidade", ylabel = "Altura de Apex (km)")
    
    
    ax.set_xlabel("Hora universal", 
                     rotation = 0, 
                     labelpad = 25)
    
def date_under_axis(ax, dn, miny = 210, delta = 3.5):
    delta = dt.timedelta(hours = delta)
    
    text_date = dn.strftime("%d/%m/%Y")

    ax.text(dn - delta, miny, text_date, 
            transform = ax.transData)
    
def midnight_points(df):
    return df.loc[df.index.time == dt.time(0, 0)].index
    
for dn in midnight_points(ts):
    
    date_under_axis(ax, dn)