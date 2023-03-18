import pandas as pd
import numpy as np
from nrlmsise00 import msise_flat
from PlanetaryIndices.core import get_indices
import datetime as dt
from RayleighTaylor.base.neutral import R, nui_1, eff_wind
from RayleighTaylor.base.iono import scale_gradient
from build import paths as p
pd.options.mode.chained_assignment = None


def load_ROTI():
    infile = "database/Results/maximus/salu_2013.txt"
    df = pd.read_csv(infile, index_col = 0)
    df.index = pd.to_datetime(df.index)
    return df.interpolate()


def load_HWM():
    infile = "database/HWM/saa_250_2013.txt"
    
    df = pd.read_csv(infile, index_col = "time")
    df.index = pd.to_datetime(df.index)
    del df["Unnamed: 0"]
    
    df["U"] = eff_wind(df["zon"], 
             df["mer"], 
             year = 2013, 
             site = "saa").Nogueira
    return df



def filter_times(start, df):
    
    end = start + dt.timedelta(hours = 11)
    return df.loc[(df.index >= start) & 
                 (df.index <= end), :]

coords = {"car": (-7.38, -36.528), 
          "for": (-3.73, -38.522), 
          "saa": (-2.53, -44.296)}

def load_iri(date):
    infile = p("IRI").files
    
    df = pd.read_csv(infile, index_col = 0)
    
    df.index = pd.to_datetime(df.index)
    
    return df.loc[df.index == date]


def load_fpi(date):
    fpi = p("FabryPerot").get_files_in_dir("processed")
    
    df = pd.read_csv(fpi, index_col = 0)
    
    df.index = pd.to_datetime(df.index)
    
    df["u"] = eff_wind(df.zon, 
                       df.mer, 
                       year = 2013, 
                       site = "saa").Nogueira
    
    df["u"].plot()
    
    return df.loc[df.index == date, "u"].item()


    
def run_msise(datetime, 
          hmin = 200, 
          hmax = 500, 
          step = 1, 
          site = "saa"):
    
    glat, glon = coords[site]
    
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

def get_pre(dn, df):
    
    b = dt.time(21, 0, 0)
    e = dt.time(22, 30, 0)
    
    df = df.loc[(df.index.time >= b) & 
                (df.index.time <= e) & 
                (df.index.date == dn.date()), ["vz"]]
        
    return round(df.max().item(), 2), df.idxmax().item()

def timerange_msise(start):
    
    end = start + dt.timedelta(hours = 30)
    
    out = []
    for dn in pd.date_range(start, end, freq = "10min"):
        
        ts = run_msise(dn, hmin = 300, hmax = 300)
        
        ts.index = [dn]
        ts["R"] = R(ts.O2,  ts.N2)
        ts["nu"] = nui_1(ts.Tn, ts.O, ts.O2,  ts.N2)
        out.append(ts)
    
    return pd.concat(out)

def timerange_iri(alt = 300):
    
    infile = "database/IRI/SAA_2013_ne.txt"
    
    df = pd.read_csv(infile, index_col = 0)
    df.index = pd.to_datetime(df.index)
    
    out = []
    for time in np.unique(df.index):
    
        n = df.loc[df.index == time].copy()
        
        step = n["alt"][1] - n["alt"][0]
        
        n["L"] = scale_gradient(n["Ne"], dz = step)
        
        out.append(n.loc[n["alt"] == alt, ["Ne", "L"]])
        
    return pd.concat(out)

def main():
    start = dt.datetime(2013, 1, 1, 21)


