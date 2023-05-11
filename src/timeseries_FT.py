import FluxTube as ft
import ionosphere as io
from utils import datetime_from_fn
import os 
import pandas as pd






infile = "D:\\FluxTube\\"


def run_each_hemisphere(infile):
    files = os.listdir(infile)

    gmax = {
            "north": [], 
            "south": []
            }
    idx = []
    
    for filename in files:
        
        print(filename)
        
        path = os.path.join(infile, filename)
        
        idx.append(datetime_from_fn(filename))
        
        for hm in ["north", "south"]:
            
            ds = compute_parameters(path, hm)
            
            alts, gamma = effects_due_to_gravity(ds)
            
            gmax[f"{hm}"].append(gamma[alts == 300].item())
                
    return pd.DataFrame(gmax, index = idx)
