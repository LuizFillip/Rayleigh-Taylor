import pandas as pd
import numpy as np
from nrlmsise00 import msise_flat
import os
import pyIGRF
from geomagnetic_parameters import toYearFraction

#infile = "G:\\My Drive\\Python\\data-analysis\\PlanetaryIndices\\database\\postdam.txt"
infile = "G:/Meu Drive/Python/data-analysis/PlanetaryIndices/database/postdam.txt"

def postdamData(infile, date):
    
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
    
    _date_ = pd.to_datetime(date.date())
    return df.loc[df.index == _date_, 
                  ["F10.7obs", "F10.7a", "Ap"]].values


def runMSISE( 
             date, 
              hmin = 100, 
              hmax = 600, 
              step = 1, 
              glat = -3.73, 
              glon = -38.522, infile = infile):
    
    """Running models MSISE00"""
    
    alts = np.arange(hmin, hmax + step, step)
    
    f107, f107a, ap = tuple(postdamData(infile, date).ravel())
    
    
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

class getPyglow(object):
    
    def __init__(self, 
                 date, 
                 infile =  "database/pyglow/" ):
        self.infile = infile
        self.date = date

    @staticmethod
    def read(infile):
        
        df = pd.read_csv(infile, index_col = 0)
        df["date"] = pd.to_datetime(df["date"])
        return df

    
    def winds(self, 
              filename = "winds2014_2015.txt", 
              glat = -3.73, 
              glon = -38.522, 
              component = "U"):
        
        df = self.read(self.infile + filename)
        
        d, i, h, x, y, z, f = pyIGRF.igrf_value(glat, glon, 
                                                year = toYearFraction(self.date))

        df["U"] = (df.zon * np.cos(np.radians(d)) + 
                   df.mer * np.sin(np.radians(d)))
        return df.loc[(df["date"] == self.date), component].values
        
    
    def density(self,
                filename = "density2014_2015.txt"):
        
        df = self.read(self.infile + filename)
        
        return df.loc[(df["date"] == self.date), "Ne"].values
    
    


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
                              
