import pandas as pd
from base.neutral import eff_wind
from PlanetaryIndices.base import get_indices
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np


def get_pre(date):
    infile ="database/PRE/FZ_PRE_2014.txt"
    
    df = pd.read_csv(infile, index_col = 0)
    
    df.index = pd.to_datetime(df.index)
    
    ts = df.loc[df.index.date == date, "vz"]

    return ts.item()


def get_wind(date, 
             year = 2014, 
             site = "for"):    
    
    infile = f"database/pyglow/{site}_winds_{year}.txt"

    df = pd.read_csv(infile, index_col = "time")
    
    try:
        del df["Unnamed: 0"]
    except:
        pass
    
    df.index = pd.to_datetime(df.index)
    
    if isinstance(date, dt.datetime):
        date = date.date()
        
    return df.loc[df.index.date == date]

def plot_all(winds, u):
    winds.zon.plot(label = "zonal")
    winds.mer.plot(label = "meridional")
    u.Nogueira.plot(label = "Nogueira")
    u.Carrasco.plot(label = "Carrasco")
    u.Jonas.plot(label = "Jonas")
    plt.legend()
    
    
def main():
    date = dt.date(2014, 1, 1)
    winds = get_wind(date)
    vzp = get_pre(date)

    u = eff_wind(winds.zon, winds.mer)



from nrlmsise00 import msise_flat


def runMSISE( datetime, 
              hmin = 100, 
              hmax = 600, 
              step = 1, 
              glat = -3.73, 
              glon = -38.522):
    
    """Running models MSISE00"""
    
    alts = np.arange(hmin, hmax + step, step)
     
    t = get_indices(datetime.date())
    
    res = msise_flat(datetime, alts[None, :], 
                     glat, glon, t.get("F10.7a"), 
                     t.get("F10.7obs"), t.get("Ap"))
    
    columns = ["He", "O", "N2", "O2", "Ar", 
              "mass", "H", "N", "AnO", "Tex", "Tn"]
    
    print(res)
    df = pd.DataFrame(res[0], index = alts, 
                      columns = columns)
    
    df.drop(["He", "Ar", 
             "mass", "H", "N", "AnO", "Tex"], 
            axis = 1, 
            inplace = True)
    
    return df

date = dt.datetime(2014, 1, 1, 21, 20)
df = runMSISE(date)

print(df)