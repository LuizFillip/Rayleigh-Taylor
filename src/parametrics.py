import base as b
import datetime as dt
import os
import FluxTube as ft
import RayleighTaylor as rt
import GEO as g
import pandas as pd 

PATH_PRE = "digisonde/data/PRE/"
PATH_FLUXTUBE = "FluxTube/data/reduced/"


def PRE(site = 'saa', alt=300):

    fname = "R2013_2021.txt"

    infile = os.path.join(PATH_PRE, site, fname)

    ds = b.load(infile)

    ds.rename(
        columns = {"vzp": "vp"}, 
        inplace=True
        )

    f_apex = ft.factor_height(alt) ** 3

    ds["vp"] = ds["vp"] * f_apex

    return ds


def FluxTube_dataset(
        year = 2013, 
        site = "saa"
        ):

    infile = os.path.join(
        PATH_FLUXTUBE, 
        site, 
        f"{year}.txt"
        )
    ds = b.load(infile)

    try:
        joined = ds.join(PRE(site))
    except:
        joined = ds.copy()
        
    return joined
    


def concat_years( 
        site = "saa"
        ):
  
    out = []
    
    for year in range(2013, 2023):
        
        infile = os.path.join(
            PATH_FLUXTUBE, 
            site, 
            f"{year}.txt"
            )
        ds = b.load(infile)
        
        try:
            joined = ds.join(PRE(site))
        except:
            joined = ds.copy()
            
            
        out.append(joined)
        
    df = pd.concat(out)
    
    save_in = f'database/Results/concat/{site}.txt'
    
    df.to_csv(save_in)
    
    return df


def run():

    site = "saa"
    path = f'database/Results/concat/{site}.txt'
    df = b.load(path)
    
    df = rt.add_gammas(df)
    
    # df.to_csv(path)
    


