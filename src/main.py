import os
import pandas as pd
import RayleighTaylor as rt
from utils import datetime_from_fn

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



infile = "D:\\TubeFlux\\02\\"
month = 2


for filename in os.listdir(infile):
    
    dn = datetime_from_fn(filename)
    
    if (dn == dt.datetime(2013, month, 6, 0, 20)):
        break
    else:
        run(infile, month)