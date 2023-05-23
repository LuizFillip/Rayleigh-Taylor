import os
import pandas as pd
from utils import datetime_from_fn
import FluxTube as ft
import datetime as dt



def concat_save(infile, mon):
    out = []
    mon = int(mon)
    for filename in os.listdir(infile):
        
        dn = datetime_from_fn(filename)
        
        print("processing...", dn)
        out.append(ft.IntegratedParameters(
            os.path.join(infile, filename))
            )
        
    df = pd.concat(out)
           
    save_in = "database/RayleighTaylor/process/"
    filename = f"{mon}.txt"
    
    df.to_csv(os.path.join(save_in, filename))
    
infile = "D:\\TubeFlux\\"    

mons = ["01", "02", "03", "04", "05", "06"]
mons = ["07", "08", "09", "10", "11", "12"]

#for mon in mons:
mon = "12"
concat_save(os.path.join(infile, str(mon)), mon)