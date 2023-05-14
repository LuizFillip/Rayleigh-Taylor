import os
import pandas as pd
import RayleighTaylor as rt
from utils import datetime_from_fn
import FluxTube as ft
import datetime as dt


def run(infile, month):
    
    out = []
    
    for filename in os.listdir(infile):
        
        print("processing...", filename)
        
        for hem in ["south", "north"]:

            out.append(rt.load(
                infile, 
                filename, 
                hemisphere = hem)
                )

    df = pd.concat(out)
           
    save_in = "database/RayleighTaylor/process/"
    filename = f"{month}.txt"
    df.to_csv(os.path.join(save_in, filename))
    return df



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
    
for mon in os.listdir(infile):
    if int(mon) == 4:
        pass
    else:
        concat_save(os.path.join(infile, mon), mon)