import pandas as pd
import numpy as np
from nrlmsise00 import msise_flat
from PlanetaryIndices.core import get_indices
import datetime as dt
from RayleighTaylor.base.neutral import R, nui_1
from build import paths as p

coords = {"car": (-7.38, -36.528), 
          "for": (-3.73, -38.522), 
          "saa": (-2.53, -44.296)}

 
def filter_times(start, df):
    
    end = start + dt.timedelta(hours = 11)
    return df.loc[(df.index >= start) & 
                  (df.index <= end), :]

def load_IRI(date):
    infile = p("IRI").files
    
    df = pd.read_csv(infile, index_col = 0)
    
    df.index = pd.to_datetime(df.index)
    
    return df.loc[df.index == date]


def load_FPI(date):
    fpi = p("FabryPerot").get_files_in_dir("processed")
    
    df = pd.read_csv(fpi, index_col = 0)
    
    df.index = pd.to_datetime(df.index)
      
    return df.loc[df.index == date, "u"].item()


    
def run_msise(
        datetime, 
        hmin = 200, 
        hmax = 500, 
        step = 1, 
        site = "saa"
        ):
    
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



def timerange_MSISE(dn, fixed_alt = 300):
        
    out = []
    for dn in pd.date_range(
            dn, 
            periods = 67, 
            freq = "10min"
            ):
        
        ts = run_msise(dn, hmin = fixed_alt, hmax = fixed_alt)
        
        ts.index = [dn]
        ts["R"] = R(ts.O2,  ts.N2)
        ts["nu"] = nui_1(ts.Tn, ts.O, ts.O2,  ts.N2)
        out.append(ts)
    
    return pd.concat(out)




