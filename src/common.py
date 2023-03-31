import pandas as pd
from Digisonde.utils import smooth
from base.iono import scale_gradient
import numpy as np
import datetime as dt
#from base.src.neutral import R

def R(O2, N2):
    """Recombination coefficient"""
    return (4.0e-11 * O2) + (1.3e-12 * N2)    

def nui(Tn, O, O2, N2):
    """
    The ion-neutral collision frequency
    by Bailey and Balan (1996)
    """
    term_O = (4.45e-11 * O * np.sqrt(Tn) * 
              (1.04 - 0.067 * np.log10(Tn))**2)
    
    term_O2 = 6.64e-10 * O2
    term_N2 = 6.82e-10 * N2
        
    return term_O + term_O2 + term_N2



class load(object):
    
    def __init__(self):
        pass
    
    @staticmethod
    def _load(infile):
        df = pd.read_csv(infile, index_col = 0)
        df.index = pd.to_datetime(df.index)
        return df
    
    @staticmethod
    def timeseries_grad(df, alt = 350):
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
            ts["nu"] = nui(ts["T"], ts["O"], ts["O2"],  ts["N2"])
            return ts.loc[:, ["R", "nu"]]
        
        else:
            return ts

    
    def roti(
            self, 
            infile = "database/Results/maximus/salu_2013.txt"
            ):
        
        return self._load(infile).interpolate()
    
    def pre(
            self, 
            infile = "database/Results/maximus/salu_2013.txt"
            ):
        
        return self._load(infile)
    
    
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
            return self.timeseries_grad(df, alt = alt)
        else:
            return df
        

def SET(dn, df):
    end = dn + dt.timedelta(hours = 11)
    return df.loc[(df.index >= dn ) & 
                  (df.index <= end) , :]


def get_pre(dn, df):
    
    b = dt.time(21, 0, 0)
    e = dt.time(22, 30, 0)
    
    df = df.loc[(df.index.time >= b) & 
                (df.index.time <= e) & 
                (df.index.date == dn), ["vz"]]
        
    return df.idxmax().item(), round(df.max().item(), 2)

def get_pre_in_year():
        
    ts = load()
    dates = pd.date_range("2013-1-1", 
                          "2013-12-31", freq = "1D")
    out = {"vp": [], 
           "time": []}
    df = ts.drift()
    
    
    for dn in dates:
        
        try:
            df1 = df.loc[df.index.date == dn.date()]
            tpre, vpre = get_pre(dn.date(), df1)
            
            out["vp"].append(vpre)
            out["time"].append(tpre)
        except:
            out["vp"].append(np.nan)
            out["time"].append(np.nan)
            continue
        
        
    ds = pd.DataFrame(out, index = dates)
    
    
    ds.loc[(ds.index.month <= 4) 
           & (ds["vp"] < 10), "vp"] = np.nan
    
    ds.loc[ (ds.index.month > 9)
           & (ds["vp"] < 10), "vp"] = np.nan
    
    return ts


