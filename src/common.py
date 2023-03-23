import pandas as pd
from Digisonde.utils import smooth
from RayleighTaylor.base.iono import scale_gradient
import numpy as np
import datetime as dt
from RayleighTaylor.base.neutral import R, nui_1



class load(object):
    
    def __init__(self):
        pass
    
    @staticmethod
    def _load(infile):
        df = pd.read_csv(infile, index_col = 0)
        df.index = pd.to_datetime(df.index)
        return df
    
    @staticmethod
    def compute_gradient(df, alt = 350):
        out = []
        for time in np.unique(df.index):
        
            n = df.loc[df.index == time].copy()
            
            step = n["alt"][1] - n["alt"][0]
            
            n["L"] = scale_gradient(n["Ne"], dz = step)
            
            out.append(n.loc[n["alt"] == alt, ["Ne", "L"]])
            
        return pd.concat(out)
    
    def HWM(
            self, 
            infile = "database/HWM/HWM14/SAA3502013.txt"
            ):    
        return self._load(infile)
    
    def MSIS(
            self, 
            infile = "database/MSIS/msis_300_saa.txt",
            computed = True
            ):
        ts =  self._load(infile)
        if computed:
            
            ts["R"] = R(ts.O2,  ts.N2)
            ts["nu"] = nui_1(ts["T"], ts["O"], ts["O2"],  ts["N2"])
            return ts.loc[:, ["R", "nu"]]
        
        else:
            return ts
    
    
    def roti(
            self, 
            infile = "database/Results/maximus/salu_2013.txt"
            ):
        
        return self._load(infile).interpolate()
    
    
    def drift(
            self, 
            infile = "database/Drift/SSA/PRO_2013.txt",
            smoothed = True,
            cols = ["vz", "evz"]
            ):
        
        df = self._load(infile)
        if smoothed:
            df["vx"] = smooth(df["vx"], 3)
            df["vy"] = smooth(df["vy"], 3)
            df["vz"] = smooth(df["vz"], 3)
            
        df = df.resample("5min").last().interpolate()
        
        return df.loc[:, cols]
    
    def IRI(
        self, 
        infile = "database/IRI/SAA_2013_ne.txt", 
        alt = 300,
        L = True
        ):
        df = self._load(infile) 
        
        if L:
            return self.compute_gradient(df, alt = alt)
        else:
            return df
        


def get_pre(dn, df):
    
    b = dt.time(21, 0, 0)
    e = dt.time(22, 30, 0)
    
    df = df.loc[(df.index.time >= b) & 
                (df.index.time <= e) & 
                (df.index.date == dn), ["vz"]]
        
    return df.idxmax().item(), round(df.max().item(), 2)

