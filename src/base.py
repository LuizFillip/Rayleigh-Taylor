import pandas as pd
import numpy as np
import digisonde as dg


def gamma_max_from_filter(df, date, alts = (250, 350)):
   
    cond_alt = ((df.index >= alts[0]) &
                (df.index <= alts[1]))
    
    cond_time = (df["date"] == date)
    
    return df.loc[cond_alt & cond_time, "g"].max()

def gamma_maximus(infile = "02_11_north.txt"):
    
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
   
    
    
 
def add_drift_pre(df):
    pre = "database/Drift/PRE/SAA/2013.txt"
    
    ds = pd.read_csv(pre, index_col = 0)
    ds.index = pd.to_datetime(ds.index)
    
    for date in np.unique(df.index.date):
        vp = ds.loc[ds.index.date == date]
        df.loc[df.index.date == date, "vzp"] = vp["vp"].item()

    return df

        
def set_data(infile = "02_11_north.txt", 
             hemisphere = "north",
             alt = 300
             ):
    
    df = pd.read_csv(infile, index_col=0)
    
    df = df.loc[(df.index == alt) & 
                (df["hem"] == hemisphere)]
    
    df = df.set_index("dn")
    
    df.index = pd.to_datetime(df.index)
    
    drift_file = "database/Drift/SSA/PRO_2013.txt"

    drift = dg.load_drift(drift_file)

    df["vz"] = drift["vz"].copy()
    df = add_drift_pre(df)
    return df

