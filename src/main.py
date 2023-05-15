import os
import pandas as pd
from utils import datetime_from_fn
import FluxTube as ft
import datetime as dt


infile = "D:\\FluxTube\\"


def concat_save(infile, mon):
    out = []
    mon = int(mon)
    for filename in os.listdir(infile):
        
        dn = datetime_from_fn(filename)
        
        if dn < dt.datetime(2013, mon, 6, 0, 20):
            print("processing...", filename)
            out.append(ft.IntegratedParameters(
                os.path.join(infile, filename))
                )
        
    df = pd.concat(out)
           
    save_in = "database/RayleighTaylor/process2/"
    filename = f"{mon}.txt"
    
    df.to_csv(os.path.join(save_in, filename))
    
infile = "D:\\FluxTube\\"    

mons = ["01", "02", "03"]
mons = ["04", "05", "06"]
mons = ["07", "08", "09"]
mons = ["10", "11", "12"]


mon = "07"
#for mon in mons:
concat_save(os.path.join(infile, str(mon)), mon)