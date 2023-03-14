import pandas as pd
import datetime as dt
from RayleighTaylor.base.neutral import eff_wind
import math

def get_ne(date_time, hmin = 200, hmax = 300):
    
    infile = "database/pyglow/density2014.txt"
        

    df = pd.read_csv(infile, index_col = 0)

    df["date"] = pd.to_datetime(df["date"])
    
    alt_cond = ((df.index >= hmin) & 
                (df.index <= hmax))
        
    return df.loc[(df["date"] == date_time) 
                  & alt_cond, "Ne"]

def get_pre(date):
    infile ="database/Digisonde/vzp/FZ_PRE_2014_2015.txt"
    
    df = pd.read_csv(infile, index_col = 0)
    
    df.index = pd.to_datetime(df.index)
    
    ts = df.loc[df.index.date == date, "vz"]

    return ts.item()


def get_wind(date, hmin = 200, hmax = 500, 
             func_wind = "U1"):    
    
    infile = "database/pyglow/winds2014.txt"

    df = pd.read_csv(infile, index_col = "time")

    df.rename(columns = {"Unnamed: 0":  "alts"},
              inplace = True)
    df.index = pd.to_datetime(df.index)

    if isinstance(date, dt.datetime):
        date = date.date()
        
    if func_wind == "U1":
        
        df["U"] = eff_wind(df.zon, df.mer).Nogueira
        
    elif func_wind == "U2":
        df["U"] = eff_wind(df.zon, df.mer).Jonas
        
    else:
        df["U"] = eff_wind(df.zon, df.mer).Carrasco
        
    alt_cond = ((df.alts >= hmin) & (df.alts <= hmax))
    return df.loc[(df.index.date == date) & alt_cond]



def split_time(time):
    frac, whole = math.modf(float(time))
    return int(whole), round(frac * 60)

def get_datetime_pre(dn):
    infile ="database/Digisonde/vzp/FZ_PRE_2014_2015.txt"
    
    df = pd.read_csv(infile, index_col = 0)
    
    df.index = pd.to_datetime(df.index)
   
    time_sel = df.loc[df.index == dn, "time"]
    
    hour, minute = split_time(time_sel.item())
    
    return dt.datetime(
        dn.year, dn.month, dn.day, 
                hour, minute)

