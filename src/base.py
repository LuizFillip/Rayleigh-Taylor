import pandas as pd
import digisonde as dg
import FluxTube as ft
import os
import datetime as dt

    
 

def repeat_by_day(ds, dn):
    
    index = pd.date_range(
        dn, dn + dt.timedelta(
            hours = 23, 
            minutes = 50), 
        freq = "10min")
    
    value = ds[ds.index == dn]["vp"].item()
    
    return pd.DataFrame(
        {"vzp": [value] * len(index)}, 
        index = index
        )

def pre_drift():
    
    pre_file = "database/Drift/PRE/SAA/2013.txt"
    
    pre = pd.read_csv(pre_file, index_col = 0)
    pre.index = pd.to_datetime(pre.index)
    
    out = [repeat_by_day(pre, dn) for dn in pre.index]
    
    return pd.concat(out)

def vertical_drift():
    drift_file = "database/Drift/SSA/PRO_2013.txt"
    
    drift = dg.load_drift(drift_file)
    return drift.resample("10min").asfreq().bfill()

        
def set_data(
        infile = "02_11_north.txt", 
        alt = 300
        ):
    
    df = pd.read_csv(infile, index_col=0)
    
    df = df.loc[df.index == alt]
    
    df = df.set_index("dn")
    
    df.index = pd.to_datetime(df.index)
    
    df["vz"] = vertical_drift()["vz"].copy()
     
    df["vzp"] = pre_drift()["vzp"].copy()
    
    return df


def load_process(infile, apex = 300):
    df = pd.read_csv(infile, index_col = 0).sort_index()

    df.index = pd.to_datetime(df.index)
    
    for vz in ["vz", "vzp"]:
        df[vz] = df[vz] * ft.factor_height(apex)**3
        
    return df

def remove_lowers(ds):
    return [i for i in ds if len(i) > 10]

def separeting_times(df, freq = "5D"):
          
    ts = pd.date_range(
        df.index[0], df.index[-1], freq = freq
        )
    
    return remove_lowers([df[(df.index >= ts[i]) & 
                             (df.index <= ts[i + 1])]
            for i in range(len(ts) - 1)])


def reduced_data_in_altitude(
        infile, altitude = 300
        ):
    out = []
    for filename in os.listdir(infile):
        print("processing...", filename)
        #if int(month) <= 6:
        out.append(set_data(
            infile + filename, alt = altitude)
            )
            
    df = pd.concat(out).sort_index()
    
    save_in = 'database/RayleighTaylor/reduced/'
    df.to_csv(f"{save_in}{altitude}.txt")
    return df


infile = "database/RayleighTaylor/process/"
reduced_data_in_altitude(infile)

