import os
import FluxTube as ft
import ionosphere as io
import matplotlib.pyplot as plt
import pandas as pd
from utils import datetime_from_fn

def effects_due_to_gravity(ds):
    return  ds["ratio"] * ((9.81 / ds["nui"])) * ds["K"]

def effects_due_to_winds(ds, wind_type = "zon"):
    return ds["ratio"] * (- ds[wind_type] + (9.81 / ds["nui"])) * ds["K"]


def load(infile, hemisphere = "north"):
    
    base = io.load_calculate(infile)
    
    ds = ft.IntegratedParameters(
        base, 
        hemisphere = hemisphere
        )

    ds["ratio"] = ft.ratio(base).by_hemis(hemisphere).dropna()
        
    ds["K"] = ft.gradient_integrated(ds["N"], ds.index)

    return ds    

def build(infile, filename):
    
    df = load(os.path.join(infile, filename))
    
    df["gamma_g"] = effects_due_to_gravity(df)
    
    for wind in ["zon", "zon_ef"]:
        df[f"gamma_{wind}"] = effects_due_to_winds(
            df, wind_type = wind)
    
    df["dn"] = datetime_from_fn(filename)
    return df


infile = "D:\\TubeFlux\\"
infile = "F:\\FluxTube\\01\\"

out = []
files = os.listdir(infile)

for filename in files:
    

    print("processing", filename)
    out.append(build(infile, filename))
    
    
pd.concat(out).to_csv("01.txt")