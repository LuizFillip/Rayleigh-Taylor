import pandas as pd
import numpy as np
import digisonde as dg
import datetime as dt


    
    
 
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
             alt = 300,
             delta = dt.timedelta(days = 5, minutes = 20)
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
    
    return df[df.index < df.index[0] +  delta]


