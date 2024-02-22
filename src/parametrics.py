import base as b
import os
import FluxTube as ft
import pandas as pd 
from tqdm import tqdm 

PATH_PRE = "digisonde/data/PRE/"
PATH_FLUXTUBE = "FluxTube/data/reduced/"
PATH_GAMMA = 'database/gamma/'


def add_gammas(df, wind_col = "mer_perp"):

    df["drift"] = df["ratio"] * df["K"] * df["vp"]
    
    df["gravity"] = df["ratio"] * df["K"] * (
        -df[wind_col] + df["ge"] / df["nui"]
        )
        
    df["gamma"] = (
        df["ratio"] * df["K"] * 
        (df["vp"] - df[wind_col] + 
        (df["ge"] / df["nui"]))
    )


    return df

def PRE(site = 'saa', alt=300):
    """
    Adding PRE value
    """
    fname = "R2013_2021.txt"

    infile = os.path.join(PATH_PRE, site, fname)

    ds = b.load(infile)

    ds.rename(
        columns = {"vzp": "vp"}, 
        inplace = True
        )

    f_apex = ft.factor_height(alt) ** 3

    ds["vp"] = ds["vp"] * f_apex

    return ds



def GammaData(
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
        ds = ds.join(PRE(site))
    except:
        ds = ds.copy()
    
    return add_gammas(ds)




def concat_years( 
        site = "saa"
        ):
    '''
    Concat all processed files of gamma 
    parameters and save-it
    
    '''
    if site == 'saa':
        end_yr = 2023
    else:
        end_yr = 2022
        
        
    year_list = [GammaData(year, site) 
                 for year in tqdm(range(2013, end_yr))]
    
    df = pd.concat(year_list)
        
    df.to_csv(
        os.path.join(
        PATH_GAMMA, 
        f'p_{site}.txt')
        )
    
    return df



def load_gamma(site):
    
    infile = os.path.join(
        PATH_GAMMA, 
        f'{site}.txt'
        )
    
    return b.load(infile)
    


# concat_years(site = "jic")