import pandas as pd
from common import load_by_time
import datetime as dt
import digisonde as dg
import FluxTube as ft

def repeat_by_day(ds, dn):
    
    index = pd.date_range(
        dn, dn + dt.timedelta(
            hours = 23, 
            minutes = 50), 
        freq = "10min")
    
    values = [ds[ds.index == dn]["vp"].item()] * len(index)
    
    return pd.DataFrame({"vzp": values}, index = index)

def pre_drift(pre_file = "database/Drift/PRE/SAA/2013.txt"):
    
    pre = pd.read_csv(pre_file, index_col = 0)
    pre.index = pd.to_datetime(pre.index)
    
    dfs = [repeat_by_day(pre, dn) for dn in pre.index]
    
    return pd.concat(dfs)

def vertical_drift(
        drift_file = "database/Drift/REDUCED/2013_drift.txt"
        ):

    drift = dg.load_drift(drift_file)
    return drift.resample("10min").asfreq().bfill()


def add_pre(apex = 300):
    infile = "database/FluxTube/total/3003.txt"
    df = load_by_time(infile)
    
    
    drift_file = "database/Drift/REDUCED/2013_drift.txt"
    ds = load_by_time(drift_file)
    
    df["vz"] = ds["vz"].copy()
        
    pr = load_by_time('database/RayleighTaylor/drift.txt')
    
    df['vzp'] = pr['vp'].copy()
    
    for vz in ["vz", "vzp"]:
        df[vz] = df[vz] * ft.factor_height(apex)**3
            
    df.to_csv("database/FluxTube/total/3003.txt")
    
# add_pre()
