import pandas as pd
import numpy as np
from datetime import datetime
from nrlmsise00 import msise_flat
import os

def postdamData(date):
    infile = "G:\\My Drive\\Python\\data-analysis\\PlanetaryIndices\\database\\postdam.txt"
    """Read data from GFZ postdam"""
    df = pd.read_csv(infile, 
                     header = 39, 
                     delim_whitespace = True)
    
    
    df.index  = pd.to_datetime(dict(year = df['#YYY'], 
                                    month = df['MM'], 
                                    day = df['DD']))
    
    df = df.drop(columns = ["#YYY", "MM", "DD", 
                            "days", "days_m", 
                            "Bsr", "dB"])
    
    df["F10.7a"] = df["F10.7obs"].rolling(window = 81).mean()
    df = df.loc[df["D"] == 2]
    return df.loc[df.index == date, ["F10.7obs", "F10.7a", "Ap"]].values


def runMSISE(date, 
              hmin = 100, 
              hmax = 600, 
              step = 1, 
              glat = -3.73, 
              glon = -38.522):
    
    """Running models MSISE00"""
    
    alts = np.arange(hmin, hmax + step, step)
    
    f107, f107a, ap = tuple(postdamData(date).ravel())
    
    
    res = msise_flat(date, alts[None, :], glat, glon, f107a, 
                     f107, ap)
    
    columns = ["He", "O", "N2", "O2", "Ar", 
              "mass", "H", "N", "AnO", "Tex", "Tn"]
    
    df = pd.DataFrame(res[0], 
                      index = alts, 
                      columns = columns)
    
    df.drop(["He", "Ar", 
             "mass", "H", "N", "AnO", "Tex"], 
            axis = 1, 
            inplace = True)
    
    return df


    
def read_all():
    
    infile = "database/density/"
    _, _, files = next(os.walk(infile))
    
    
    filename = files[0]
    


class loadNe(object):
    
    def __init__(self, filename):
        df = pd.read_csv(filename, index_col = 0)
        
        df["date"] = pd.to_datetime(df["date"])
        
        self.times = np.unique(df.date)
        self.df  = df
      
    @property
    def pivot(self):
        self.df["alts"] = self.df.index
        return pd.pivot_table(self.df, 
                              columns = "date", 
                              index = "alts", 
                              values = "Ne")
    
    def sel_time(self, date):
        return self.df.loc[self.df["date"] == date, "Ne"]
                              
filename = "20140101.txt"
date = datetime(2014, 1, 1, 20, 10)    
df = loadNe(filename).sel_time(date)

print(df)