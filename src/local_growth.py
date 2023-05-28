import ionosphere as io
import datetime as dt
import pandas as pd
import atmosphere as atm
from models import altrange_models, altrange_msis
from GEO import sites
import FabryPerot as fp
from utils import sampled



def join_hwm_fpi(
        hwm_file = "database/HWM/saa_250_2013.txt", 
        fpi_file = "database/FabryPerot/PRO/2013.txt"
        ):

    wd = fp.load_FPI(fpi_file)
    
    df = pd.read_csv(hwm_file, index_col = "time")
    df.index = pd.to_datetime(df.index)
    
    wd.drop_duplicates(inplace = True)
    wd = wd.reindex(df.index)
        
    filled_df = wd.copy()
    filled_df["zon"] = filled_df["zon"].fillna(df["zon"])
    filled_df["mer"] = filled_df["mer"].fillna(df["mer"])

    return filled_df






    

def compute_parameters2(ne, start):
    
    ds = ne.loc[ne.index == start
                ].set_index("alt").copy()
    
    nu = io.collision_frequencies()
    
    lat, lon = sites["saa"]["coords"]

    kwargs = dict(
         dn = start, 
         glat = lat, 
         glon = lon,
         hmin = 250,
         hmax = 350, 
         step = 50
         )

    
    msis = altrange_msis(**kwargs)


    ds["nui"] = nu.ion_neutrals(
        msis["Tn"], msis["O"], 
        msis["O2"], msis["N2"]
        ).to_frame("nui")
    
    ds["R"] = atm.recombination2(
        msis["O2"], msis["N2"]
        )
    
    wd = join_hwm_fpi()
    
    ds["alt"] = ds.index
    ds.index = [start] * len(ds)
    
    ds["U"] = wd[wd.index == start]["zon"] 
    ds["V"] = wd[wd.index == start]["mer"] 
    

    
    return ds


def run_from_pyglow():

    ne = pd.read_csv("scale_plasma.txt", index_col = 0)
    ne.index = pd.to_datetime(ne.index)
    
    out = []
    
    for time in ne.index.unique():
    
        out.append(compute_parameters2(ne, time))
            
    df = pd.concat(out)
    
    df.to_csv("gamma_parameters.txt")
    return df


    
def compute_parameters(dn, alt = 300):
    
    lat, lon = sites["saa"]["coords"]

    
    kwargs = dict(
         dn = dn, 
         glat = lat, 
         glon = lon,
         hmin = 200,
         hmax = 400
         )

    df = altrange_models(**kwargs)
    
    nu = io.collision_frequencies()
    
    nui = nu.ion_neutrals(
        df["Tn"], df["O"], 
        df["O2"], df["N2"]
        )
    
    ds = pd.DataFrame()
    
    ds["nui"] = nui
    ds["L"] = io.scale_gradient(ds["ne"])
    
    ds["R"] = atm.recombination2(df["O2"], df["N2"])
    ds["ne"] = df["ne"]
    
    
    ds["alt"] = ds.index
    ds.index = [dn] * len(ds)
    
    return ds




