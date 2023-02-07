import pandas as pd
from PlanetaryIndices.base import get_indices
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
from nrlmsise00 import msise_flat
import os
from base.neutral import eff_wind

def get_ne(date_time, root = "database/density/"):
    
    filename = date_time.strftime('%Y%m%d') + ".txt"
    
    infile = os.path.join(root, filename)
    
    df = pd.read_csv(infile, index_col = 0)
    
    df["date"] = pd.to_datetime(df["date"])
    
    return df.loc[df["date"] == date_time, "Ne"]

def get_pre(date):
    infile ="database/PRE/FZ_PRE_2014.txt"
    
    df = pd.read_csv(infile, index_col = 0)
    
    df.index = pd.to_datetime(df.index)
    
    ts = df.loc[df.index.date == date, "vz"]

    return ts.item()


def get_wind(date, 
             func_wind = "Nogueira"):    
    
    infile = f"database/pyglow/winds2014.txt"

    df = pd.read_csv(infile, index_col = "time")

    df.rename(columns = {"Unnamed: 0":  "alts"},
              inplace = True)
    df.index = pd.to_datetime(df.index)

    if isinstance(date, dt.datetime):
        date = date.date()
        
    if func_wind == "Nogueira":
        df["U"] = eff_wind(df.zon, df.mer).Nogueira
    elif func_wind == "Jonas":
        df["U"] = eff_wind(df.zon, df.mer).Jonas
    else:
        df["U"] = eff_wind(df.zon, df.mer).Carrasco
        
    #date = dt.datetime(2014, 1, 1)
    return df.loc[df.index.date == date]

def plot_all(winds, u):
    winds.zon.plot(label = "zonal")
    winds.mer.plot(label = "meridional")
    u.Nogueira.plot(label = "Nogueira")
    u.Carrasco.plot(label = "Carrasco")
    u.Jonas.plot(label = "Jonas")
    plt.legend()
    
    
def run_msise(datetime, 
          hmin = 100, 
          hmax = 600, 
          step = 1, 
          glat = -3.73, 
          glon = -38.522):
    
    """Running models MSISE00"""
    
    alts = np.arange(hmin, hmax + step, step)
     
    t = get_indices(datetime.date())
    
    res = msise_flat(datetime, alts[None, :], 
                     glat, glon, 
                     t.get("F10.7a"), 
                     t.get("F10.7obs"), 
                     t.get("Ap"))
    
    columns = ["He", "O", "N2", "O2", "Ar", 
              "mass", "H", "N", "AnO", "Tex", "Tn"]
    
    df = pd.DataFrame(res[0], index = alts, 
                      columns = columns)
    
    df.drop(["He", "Ar", 
             "mass", "H", "N", "AnO", "Tex"], 
            axis = 1, 
            inplace = True)
    
    return df

