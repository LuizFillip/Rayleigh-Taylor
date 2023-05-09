import FluxTube as ft
import ionosphere as io
import matplotlib.pyplot as plt

def effects_due_to_gravity(ds):
    
    alts = ds.index
    
    K = ft.gradient_integrated(ds["N"], alts)
    
    gamma = ds["ratio"] * ((9.81 / ds["nui"])) * K 
    return alts, gamma

def compute_parameters(infile, hemisphere):
    base = io.load_calculate(infile)
    ds = ft.IntegratedParameters(
        base, 
        hemisphere = hemisphere
        )

    r = ft.ratio(base)
    
    if  hemisphere == "north":
        ds["ratio"] =  r.north.dropna()
    else:
        ds["ratio"] =  r.south.dropna()

    return ds    


from utils import datetime_from_fn
import os 
import pandas as pd

infile = "D:\\FluxTube\\"

files = os.listdir(infile)

gmax = {
        "north": [], 
        "south": []}
idx = []

for filename in files:
    print(filename)
    path = os.path.join(infile, filename)
    
    idx.append(datetime_from_fn(filename))
    
    for hm in ["north", "south"]:
        
        ds = compute_parameters(path, hm)
        
        alts, gamma = effects_due_to_gravity(ds)
        
        gmax[f"{hm}"].append(gamma[alts == 300])
            
df = pd.DataFrame(gmax, index = idx)

print(df)
