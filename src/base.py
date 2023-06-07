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
    
    values = [ds[ds.index == dn]["vp"].item()] * len(index)
    
    return pd.DataFrame({"vzp": values}, index = index)

def pre_drift(pre_file = "database/Drift/PRE/SAA/2013.txt"):
    
    pre = pd.read_csv(pre_file, index_col = 0)
    pre.index = pd.to_datetime(pre.index)
    
    dfs = [repeat_by_day(pre, dn) for dn in pre.index]
    
    return pd.concat(dfs)

def vertical_drift(
        drift_file = "database/Drift/SSA/PRO_2013.txt"
        ):

    drift = dg.load_drift(drift_file)
    return drift.resample("10min").asfreq().bfill()

        
def set_data(infile, alt = 300):
    
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
        
    return df[df.index.year == 2013]


def split_by_freq(df, freq_per_split = "5D"):
          
    groups = df.groupby(pd.Grouper(
        freq = freq_per_split)
        )
    split_dfs = []

    for group_key, group_df in groups:
        
        if len(group_df) != 0:
            split_dfs.append(group_df)
        
    return split_dfs

def reduced_data_in_altitude(
        infile, altitude = 300
        ):
    out = []
    for filename in os.listdir(infile):
        print("processing...", filename)
        out.append(set_data(
            infile + filename, alt = altitude)
            )
            
    df = pd.concat(out).sort_index()
    
    save_in = 'database/RayleighTaylor/reduced/'
    df.to_csv(f"{save_in}{altitude}.txt")
    return df

def main():
    infile = "database/RayleighTaylor/process/"
    reduced_data_in_altitude(infile)
    infile = "database/RayleighTaylor/reduced/300.txt"
    df =  load_process(infile, apex = 300)
    #df = df[df.index.month == 9]
    for ds in split_by_freq(df):
    
        if ds.index[0].month == 11:
            print(ds)

