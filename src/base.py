import pandas as pd
import numpy as np
import digisonde as dg
import FluxTube as ft

    
    
 
def add_drift_pre(df, apex = 300):
    pre = "database/Drift/PRE/SAA/2013.txt"
    
    ds = pd.read_csv(pre, index_col = 0)
    ds.index = pd.to_datetime(ds.index)
    
    for date in np.unique(df.index.date):
        vp = ds.loc[ds.index.date == date]
        vzp_fluxtube = vp["vp"].item() * ft.factor_height(apex)**3
        df.loc[df.index.date == date, "vzp"] =  vzp_fluxtube

    return df

def vertical_drift(df):

    drift_file = "database/Drift/SSA/PRO_2013.txt"

    drift = dg.load_drift(drift_file)

    df["vz"] = drift["vz"].copy()
    
    return add_drift_pre(df)

        
def set_data(infile = "02_11_north.txt", 
             alt = 300,
             
             ):
    
    df = pd.read_csv(infile, index_col=0)
    
    df = df.loc[(df.index == alt) ]
    
    df = df.set_index("dn")
    
    df.index = pd.to_datetime(df.index)
    
    return vertical_drift(df)


def load_process(infile, apex = 300):
    df = pd.read_csv(infile, index_col = 0).sort_index()

    df.index = pd.to_datetime(df.index)
    
    for vz in ["vz", "vzp"]:
        df[vz] = df[vz] * ft.factor_height(apex)**3
        
    return df


def separeting_times(df, freq = "5D"):
          
    ts = pd.date_range(
        df.index[0], df.index[-1], freq = freq
        )
    
    return [df[(df.index >= ts[i]) & 
               (df.index <= ts[i + 1])] for i in range(len(ts) - 1)]

