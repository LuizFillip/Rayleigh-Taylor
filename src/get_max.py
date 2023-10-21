import pandas as pd
import datetime as dt
import GEO as g
import RayleighTaylor as rt
from tqdm import tqdm
import os
import numpy as np


PATH_GAMMA = "database/Results/gamma/"


def terminators(dn, site="saa"):
    D = g.sun_terminator(dn, site, twilight_angle=0)
    E = g.sun_terminator(dn, site, twilight_angle=12)
    F = g.sun_terminator(dn, site, twilight_angle=18)

    return (D, E, F)


def get_maximus(ds, dn, site="saa", col="all"):

    """
    Getting gamma maximus between D or F an
    region E and F, or for whole night
    terminators :
    Parameters:

    """

    D, E, F = terminators(dn, site)

    conds = [
        ((ds.index >= D) & (ds.index <= F)),
        ((ds.index >= E) & (ds.index <= F)),
        slice(None, None),
    ]

    names = ["d_f", "e_f", "night"]

    out = {}

    for i, cond in enumerate(conds):

        out[names[i]] = ds.loc[cond, col].max()

    return pd.DataFrame(out, index=[dn.date()])


def empty(dn):
    out = {
        "d_f": np.nan, 
        "e_f": np.nan, 
        "night": np.nan
        }
    return pd.DataFrame(out, index=[dn.date()])


def get_parameters_maxs(dn, site):
    
    ds = rt.FluxTube_dataset(dn, site)
        
    
    D, E, F = terminators(dn, site)
    
    conds = [
        ((ds.index >= D) & (ds.index <= F)),
        ((ds.index >= E) & (ds.index <= F)),
        slice(None, None),
    ]
    
    names = ["d_f", "e_f", "night"]
    
        
    out_w = []
    
    for n, cond in enumerate(conds):
        
        out = {}
        
        for col in ds.columns:
            out[col] = ds.loc[cond, col].max()
        
        
        out_w.append(
            pd.DataFrame(out, index = [names[n]]))
        
    df = pd.concat(out_w)
    df['period'] =  df.index 
    df.index = [dn.date()] * 3

    return df


def gamma_maximus(
        year = 2013, 
        site = "saa", 
        col = "all"
        ):

    """
    Get gamma maximus for whole year,
    try for local and integrated quantities
    """
    out = []
    for day in tqdm(range(365), str(year)):

        delta = dt.timedelta(days = day)

        dn = dt.datetime(year, 1, 1, 21, 0) + delta

        # df = rt.gammas_integrated(
        #     rt.FluxTube_dataset(dn, site)
        #     )
        

        # try:
            # out.append(
            #     get_maximus(df, dn, site, col)
            #     )
            
        out.append(
            get_parameters_maxs(dn, site)
            )
        
        # except:
        #     out.append(empty(dn))

    return pd.concat(out)


def run_years(site = "saa"):
    
    print('[processing_gamma]', site)
    
    out = []

    for year in range(2013, 2023):

        out.append(gamma_maximus(year, site))

    return pd.concat(out)


def main(site):
    

    for site in ['saa', 'jic']:
     

        save_in = os.path.join(
            PATH_GAMMA, 
            f"p_{site}.txt"
            )
    
        ds = run_years(site)
    
        ds.to_csv(save_in)

year = 2013
site = 'saa'
dn = dt.datetime(year, 1, 1, 21, 0)

df = rt.FluxTube_dataset(dn, site)
    

# df.loc[df.index.time == dt.time(22, 0)]

