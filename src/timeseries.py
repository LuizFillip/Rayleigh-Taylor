import FluxTube as ft
import ionosphere as io
import matplotlib.pyplot as plt

def effects_due_to_winds(ds, 
        wind_type = "zon",
        ):
    
    alts = ds.index
    
    K = ft.gradient_integrated(ds["N"], alts)
    
    gamma = ds["ratio"] * (- ds[wind_type] + (9.81 / ds["nui"])) * K 
    return alts, gamma

infile = "database/FluxTube/201301012100.txt"

hemisphere = "north"

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
from tqdm import tqdm
import os 
import pandas as pd
infile = "D:\\venv\\venv\\ress\\"

files = os.listdir(infile)

gmax = {"north_zon_ef" : [], 
        "south_zon_ef" : [], 
        "north_zon": [], 
        "south_zon": []}
idx = []

for filename in tqdm(files):

    path = os.path.join(infile, filename)
    
    idx.append(datetime_from_fn(filename))
    
    for hm in ["north", "south"]:
        
        ds = compute_parameters(path, hm)
        
        for wd in ["zon", "zon_ef"]:
            alts, gamma = effects_due_to_winds(ds, 
                    wind_type = wd,
                )
            
            gmax[f"{hm}_{wd}"].append(gamma[alts == 300])
            
    
    
df = pd.DataFrame(gmax, index = idx)

print(df)
