import FluxTube as ft
import ionosphere as io
from utils import datetime_from_fn
from utils import smooth2
import os
import pandas as pd



def load(infile, filename, hemisphere = "north"):
    
    base = io.load_calculate(
        os.path.join(infile, filename)
        )
    
    ds = ft.IntegratedParameters(
        base, 
        hemisphere = hemisphere
        )

    ds["ratio"] = ft.ratio(base).by_hemis(hemisphere).dropna()
        
    ds["K"] = ft.gradient_integrated(ds["N"], ds.index)
    ds["dn"] = datetime_from_fn(filename)
    
    ds["nui"] = 9.81 / ds["nui"]

    return ds    



