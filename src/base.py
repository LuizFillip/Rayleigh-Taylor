import pandas as pd
import FluxTube as ft
import os

    

def set_data(infile, alt = 300):
    
    df = pd.read_csv(infile, index_col=0)
    
    df = df.loc[df.index == alt]
    
    df = df.set_index("dn")
    
    df.index = pd.to_datetime(df.index)
    
    # df["vz"] = vertical_drift()["vz"].copy()
     
    # df["vzp"] = pre_drift()["vzp"].copy()
    
    return df


def load_process(infile, apex = 300):
    df = pd.read_csv(infile, index_col = 0).sort_index()

    df.index = pd.to_datetime(df.index)
    
    for vz in ["vz", "vzp"]:
        df[vz] = df[vz] * ft.factor_height(apex)**3
        
    return df[df.index.year == 2013]


def split_by_freq(
        df, 
        freq_per_split = "5D"
        ):
          
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
            os.path.join(infile, filename), 
            alt = altitude)
            )
            
    df = pd.concat(out).sort_index()
    
    save_in = 'database/RayleighTaylor/reduced/'
    df.to_csv(f"{save_in}{altitude}2.txt")
    return df

def main():
    infile = "database/RayleighTaylor/process2/"
    reduced_data_in_altitude(infile)
    # infile = "database/RayleighTaylor/reduced/300.txt"
    # df =  load_process(infile, apex = 300)

    