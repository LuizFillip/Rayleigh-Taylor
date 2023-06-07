import pandas as pd
import atmosphere as atm
import digisonde as dg
from utils import sampled
from GEO import sites 
from models import point_msis
import ionosphere as io
import numpy as np

pd.options.mode.chained_assignment = None 



def load_drift(dn = None, freq = "2min"):
    drift_file = "database/Drift/SSA/PRO_2013.txt"
    df = dg.load_drift(drift_file, freq = freq)["vz"]
    
    if dn is not None:
        return df.loc[df.index == dn]
    else:
        return df


def load_winds(site = "caj", dn  = None):

    vnu_file = f"database/FabryPerot/{site}_vnu_2013.txt"
    
    wd = pd.read_csv(vnu_file, index_col = 0)
    
    wd.index = pd.to_datetime(wd.index)
    
    if dn is not None:
        return wd.loc[wd.index == dn]
    else:
        return wd
    
    


def sep_by_altitudes(
        infile, 
        alt_min = 200, 
        alt_max = 500
        ):
    
    df = dg.load_profilogram(infile)
    
    times = df.index.unique()
    out = []
    for dn in times:
        ds = df[df.index == dn]
        
        out.append(ds.loc[
            (ds["alt"] >= alt_min) & 
            (ds["alt"] <= alt_max)]
            )
      
    return pd.concat(out)


def add_neutros(ds):
    
    lat, lon = sites["saa"]["coords"]
    nu = io.collision_frequencies()
    nui = []
    R = []
    
    for i in range(len(ds)):
        
        print("processing...", ds.index[i])
        
        msi = point_msis(
            ds.index[i], ds.iloc[i, 0],
            lat, lon
            )
        
        nui.append(
            nu.ion_neutrals(
            msi["Tn"], msi["O"], msi["O2"], msi["N2"]
            ))
        
        R.append(atm.recombination2(
            msi["O2"], msi["N2"])
            )
        
    ds["nui"] = nui
    
    ds["R"] = R
    
    return ds



def add_winds_vz(df, site = "car"):
    
    times = df.index.unique()
    out = []
    for dn in times:
        print(dn)
        ds = df.loc[df.index == dn]
        
        ds["vz"] = load_drift(dn).copy()
        
        ds['vzp'] = dg.add_vzp(dn)
            
        ds[["zon", "mer"]] = load_winds(
            site = site, dn = dn).copy()
        
        out.append(atm.local_eff_wind(ds))
        
    return pd.concat(out)


def interpolated_by_times(ds):
    out = []
    for alt in ds.alt.unique():
        out.append(sampled(ds[ds["alt"] == alt]))
    
    return pd.concat(out)


def process_sites(infile):
    
    ds = interpolated_by_times(
        add_neutros(
            sep_by_altitudes(infile)
            )
        )
    
    for site in ["car", "caj"]:
        r = add_winds_vz(ds, site = site)
        
        r.to_csv(f"parameters_{site}.txt")
        
infile = "parameters_car.txt"
# process_sites(infile)

ds = load_winds(site = "car", dn  = None)
ds["alt"] = 300
df = atm.local_eff_wind(ds)
df.to_csv("perp_winds.txt")
